from django.db import migrations
from decimal import Decimal

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_pricerule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricerule',
            old_name='night_service_fee',
            new_name='night_service_price',
        ),
    ] 