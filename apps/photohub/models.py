from django.db import models


class Photo(models.Model):
    filename = models.CharField(max_length=255)
    number = models.IntegerField(null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )

    class Meta:
        db_table = 'photos'

    def __str__(self):
        return f'{self.filename} - {self.number}'
