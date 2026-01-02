from django.db import models

# Create your models here.

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('DTD', 'Door-to-Door'),
        ('FCL', 'Full Container Load'),
        ('LCL', 'Less than Container Load'),
    ]

    ORIGIN_CHOICES = [
        ('NA', 'North America'),
        ('CN', 'China'),
        ('EU', 'Europe'),
    ]

    DESTINATION_COUNTRIES = [
        # West Africa
        ('NG', 'Nigeria'),
        ('GH', 'Ghana'),
        ('CI', "Côte d'Ivoire"),
        ('SN', 'Senegal'),
        ('BJ', 'Benin'),
        ('TG', 'Togo'),
        ('ML', 'Mali'),
        ('BF', 'Burkina Faso'),
        ('GM', 'Gambia'),
        ('SL', 'Sierra Leone'),

        # Central Africa
        ('CM', 'Cameroon'),
        ('CG', 'Congo (Republic)'),
        ('CD', 'DR Congo'),
        ('GA', 'Gabon'),
        ('TD', 'Chad'),
        ('CF', 'Central African Republic'),
        ('GQ', 'Equatorial Guinea'),
    ]

    name = models.CharField(max_length=100)
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_TYPE_CHOICES
    )

    origin = models.CharField(
        max_length=2,
        choices=ORIGIN_CHOICES
    )

    destination_country = models.CharField(
        max_length=2,
        choices=DESTINATION_COUNTRIES
    )

    description = models.TextField(blank=True)

    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_time_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.name}: "
            f"{self.get_origin_display()} → "
            f"{self.get_destination_country_display()}"
        )
