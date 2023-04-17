from django.db import models


class Location(models.Model):
    address = models.CharField('Адрес', max_length=100, unique=True)
    lat = models.FloatField('Широта', null=True, blank=True)
    lon = models.FloatField('Долгота', null=True, blank=True)
    updated_at = models.DateTimeField(
        'Дата запроса к геокодеру',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'{self.address} ({self.lat}, {self.lon})'
