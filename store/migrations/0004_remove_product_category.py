from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_product_category_alter_product_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="category",
        ),
    ]
