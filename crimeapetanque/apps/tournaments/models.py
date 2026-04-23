from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from crimeapetanque import settings


class Tournament(models.Model):
    FORMAT_CATEGORIES = {
        'singles': [
            ('S_M', 'Одиночные мужчины'),
            ('S_F', 'Одиночные женщины'),
            ('S_MX', 'Одиночные смешанные'),
        ],
        'doubles': [
            ('D_MM', 'Дуплеты мужчины'),
            ('D_FF', 'Дуплеты женщины'),
            ('D_MF', 'Дуплеты смешанные'),
        ],
        'triples': [
            ('T_MMM', 'Триплеты мужчины'),
            ('T_FFF', 'Триплеты женщины'),
            ('T_MIX', 'Триплеты смешанные'),
        ]
    }
    FORMAT_CHOICES = [item for sublist in FORMAT_CATEGORIES.values() for item in sublist]

    SYSTEM_CHOICES = [
        ('ROUND_ROBIN', 'Круговая система'),
        ('GROUP_PLAYOFF', 'Группа + Кубки А/Б'),
        ('SWISS', 'Швейцарская система'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_deadline = models.DateTimeField()
    max_participants = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(80)])
    current_round = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    total_rounds = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    system = models.CharField(max_length=20, choices=SYSTEM_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    allow_technical = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.system and self.pk:
            participant_count = self.participants.count()
            if 5 <= participant_count <= 10:
                self.system = 'ROUND_ROBIN'
            elif 11 <= participant_count <= 24:
                self.system = 'GROUP_PLAYOFF'
            elif 25 <= participant_count <= 80:
                self.system = 'SWISS'
        super().save(*args, **kwargs)

    def get_format_category(self):
        for cat, formats in self.FORMAT_CATEGORIES.items():
            if self.format in [f[0] for f in formats]:
                return cat
        return None


class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, null=True, blank=True)
    rating_at_start = models.FloatField(default=50.0)
    points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    score_diff = models.IntegerField(default=0)  # разница забитых/пропущенных
    place = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('tournament', 'player', 'team')

    def get_name(self):
        if self.player:
            return self.player.get_full_name_or_username()
        return self.team.name if self.team else "Unknown"


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    round_number = models.IntegerField()
    match_number = models.IntegerField()
    participant1 = models.ForeignKey(TournamentParticipant, on_delete=models.CASCADE, related_name='matches_as_p1')
    participant2 = models.ForeignKey(TournamentParticipant, on_delete=models.CASCADE, related_name='matches_as_p2')
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    is_technical = models.BooleanField(default=False)
    technical_winner = models.ForeignKey(TournamentParticipant, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='SCHEDULED')  # SCHEDULED, PLAYED, TECHNICAL
    played_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_technical and self.technical_winner:
            if self.technical_winner == self.participant1:
                self.score1, self.score2 = 13, 7
            else:
                self.score1, self.score2 = 7, 13
            self.status = 'TECHNICAL'
        super().save(*args, **kwargs)

    @property
    def winner(self):
        if self.score1 > self.score2:
            return self.participant1
        elif self.score2 > self.score1:
            return self.participant2
        return None
