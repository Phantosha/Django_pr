from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    rating = models.FloatField(default=50.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    rating_history = models.JSONField(default=list)  # список изменений
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

    def update_rating(self, new_rating):
        self.rating_history.append({
            'date': timezone.now().isoformat(),
            'old_rating': self.rating,
            'new_rating': new_rating
        })
        self.rating = max(0, min(100, new_rating))
        self.save()

    def get_full_name_or_username(self):
        return self.get_full_name() or self.username
