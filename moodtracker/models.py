from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Entry(models.Model):
    MOOD_CHOICES = [
        (1, 'Очень плохо'),
        (2, 'Плохо'),
        (3, 'Нейтрально'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    date = models.DateField()
    mood = models.PositiveSmallIntegerField(choices=MOOD_CHOICES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')
        db_table = 'moodtracker_entry'

    def __str__(self):
        return f"{self.user} — {self.date}: {self.get_mood_display()}"
