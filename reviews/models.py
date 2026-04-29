from django.db import models
from django.contrib.auth.models import User
from spaces.models import Space
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """تقييمات المساحات — ForeignKey مع Space و User"""

    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='المساحة'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='المستخدم'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='التقييم (1-5)'
    )
    comment = models.TextField(verbose_name='التعليق')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['space', 'user']
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقييمات'

    def __str__(self):
        return f"{self.user.username} — {self.space.title} ({self.rating}/5)"
