from django.db import models

# Create your models here.
class NonWorkingDays(models.Model):
    date = models.DateField(null=False, blank=False)
    reason = models.CharField(max_length=255, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.reason}"

# class dede