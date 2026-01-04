import uuid
from django.db import models
from django.conf import settings


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    SERVICE_CHOICES = [
        ('FCL', 'Full Container Load'),
        ('LCL', 'Less than Container Load'),
        ('DTD', 'Door to Door'),
    ]

    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_CHOICES
    )

    # ---------------------------------
    # ORIGIN & DESTINATION
    # ---------------------------------

    ORIGIN_REGION_CHOICES = [
        ('north_america', 'North America'),
        ('china', 'China'),
        ('europe', 'Europe'),
    ]

    DESTINATION_COUNTRY_CHOICES = [
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

    origin_region = models.CharField(
        max_length=50,
        choices=ORIGIN_REGION_CHOICES
    )

    destination_country = models.CharField(
        max_length=50,
        choices=DESTINATION_COUNTRY_CHOICES
    )

    # ---------------------------------
    # QUOTE FIELDS
    # ---------------------------------

    maersk_ocean_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    booking_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=600.00
    )

    quoted_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # ---------------------------------
    # ORIGIN LOGISTICS
    # ---------------------------------

    origin_address = models.TextField()
    dropoff_date = models.DateField(null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)

    QUOTE_STATUS = [
        ('new', 'New'),
        ('quoted', 'Quoted'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    quote_status = models.CharField(
        max_length=20,
        choices=QUOTE_STATUS,
        default='new'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    quote_sent_at = models.DateTimeField(null=True, blank=True)
    quote_accepted_at = models.DateTimeField(null=True, blank=True)

    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Credit / Debit Card (Apple Pay supported)'),
        ('cashapp', 'Cash App'),
        ('zelle', 'Zelle'),
        ('wire', 'Wire Transfer'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )

    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} | {self.customer.username} | {self.service_type}"
