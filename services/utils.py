
from decimal import Decimal


# --------------------------------------------------
# Shipping Price Calculation
# --------------------------------------------------
def calculate_shipping_price(
    service,
    weight_kg,
    volume_cbm,
    pickup_required=False,
):
    """
    Core pricing logic for DTD, FCL, LCL
    """

    base_price = Decimal(service.base_price)

    # -------------------------
    # Weight-based pricing
    # -------------------------
    if service.service_type == 'DTD':
        base_price += Decimal(weight_kg) * Decimal('2.50')

    elif service.service_type == 'LCL':
        base_price += Decimal(volume_cbm) * Decimal('150.00')

    elif service.service_type == 'FCL':
        # Flat container rate
        base_price += Decimal('2500.00')

    # -------------------------
    # Pickup fee
    # -------------------------
    if pickup_required:
        base_price += Decimal('75.00')

    return base_price


# --------------------------------------------------
# Tax Calculation (Origin only)
# --------------------------------------------------
def calculate_tax(amount, origin_country):
    """
    Apply tax at origin only.
    For MVP: flat 5% if origin is taxable.
    """

    taxable_origins = [
        'United States',
        'Canada',
        'China',
    ]

    if origin_country in taxable_origins:
        return amount * Decimal('0.05')

    return Decimal('0.00')
