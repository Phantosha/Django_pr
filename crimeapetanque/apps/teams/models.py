from django.db import models
from django.conf import settings


class Team(models.Model):
    TYPE_CHOICES = [
        ('DOUBLET', 'Дуплет'),
        ('TRIPLET', 'Триплет'),
    ]
    GENDER_COMPOSITION = [
        ('MM', 'Мужчины'),
        ('FF', 'Женщины'),
        ('MX', 'Смешанная'),
    ]
    name = models.CharField(max_length=100)
    team_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    gender_composition = models.CharField(max_length=2, choices=GENDER_COMPOSITION)
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='captained_teams')
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TeamMembership', related_name='teams')
    rating = models.FloatField(default=50.0)
    is_technical = models.BooleanField(default=False)  # техническая команда
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_rating(self):
        members = self.teammembership_set.select_related('player').all()
        if not members:
            return 50.0
        avg = sum(m.player.rating for m in members) / len(members)
        return avg

    def update_team_rating(self):
        new_rating = self.calculate_rating()
        self.rating = new_rating
        self.save()

    def __str__(self):
        return f"{self.get_team_type_display()} '{self.name}'"


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'player')
