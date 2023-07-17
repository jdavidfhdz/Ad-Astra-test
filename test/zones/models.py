from django.db import models


class Distribution(models.Model):
    percentage = models.IntegerField(default=0)
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE, related_name='distributions', null=True)

    def __str__(self):
        return '{} - {}%'.format(self.pk, self.percentage)

    def save(self, *args, **kwargs):
        return super(Distribution, self).save(*args, **kwargs)

class Zone(models.Model):
    name = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
