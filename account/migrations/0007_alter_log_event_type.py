# Generated by Django 5.0.1 on 2024-10-29 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_log_event_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='event_type',
            field=models.CharField(choices=[('login', 'User login'), ('logout', 'User logout'), ('register', 'User register'), ('payment_success', 'User payment success'), ('payment_failed', 'User payment failed'), ('email_verification_success', 'User email verification success'), ('email_verification_failed', 'User email verification failed'), ('order_success', 'User order success'), ('profile_management', 'User edit profile'), ('delete_account', 'User account deleted'), ('manage_shipping', 'User updated shipping'), ('change_user_permissions', 'User change permissions'), ('update_product', 'Product update'), ('delete_product', 'Product deleted'), ('create_product', 'Product created'), ('create_category', 'Category created')], max_length=50),
        ),
    ]
