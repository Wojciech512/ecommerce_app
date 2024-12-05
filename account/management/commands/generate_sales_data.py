from django.core.management.base import BaseCommand
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from store.models import Category, Product
from payment.models import Order, OrderItem
from django.utils.text import slugify
from django.db import transaction

class Command(BaseCommand):
    help = 'Generuje dane testowe dla modeli Category, Product, Order i OrderItem'

    def handle(self, *args, **kwargs):
        # Wyczyszczenie istniejących danych (opcjonalne)
        Category.objects.all().delete()
        Product.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Tworzenie kategorii
        categories = ['Electronics', 'Books', 'Fashion', 'Home and Garden', 'Sports', 'Health']
        category_objects = []

        for category_name in categories:
            category = Category.objects.create(
                name=category_name,
                slug=slugify(category_name)
            )
            category_objects.append(category)

        # Tworzenie produktów
        product_objects = []
        for category in category_objects:
            for i in range(1, 6):  # 5 produktów na kategorię
                product_title = f'{category.name} Produkt {i}'
                product = Product.objects.create(
                    category=category,
                    title=product_title,
                    brand='BrandX',
                    description=f'Product description {product_title}',
                    slug=slugify(f'{product_title}-{random.randint(1, 100000)}'),
                    price=round(random.uniform(10.0, 1000.0), 2),
                    image='images/placeholder.png',
                )
                product_objects.append(product)

        # Tworzenie użytkowników (klientów)
        user_objects = []
        for i in range(1, 11):  # 10 użytkowników
            username = f'Customer{i}'
            email = f'Customer{i}@example.com'
            password = 'password123'

            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            if created:
                user.set_password(password)
                user.save()
            user_objects.append(user)

        # Generowanie zamówień i pozycji zamówień
        start_date = datetime.now() - timedelta(days=60)  # 60 dni wstecz
        end_date = datetime.now()

        total_days = (end_date - start_date).days

        with transaction.atomic():
            for day_offset in range(total_days):
                current_date = start_date + timedelta(days=day_offset)
                num_orders = random.randint(1, 5)

                for _ in range(num_orders):
                    user = random.choice(user_objects)
                    amount_paid = 0

                    # Tworzenie zamówienia
                    order = Order.objects.create(
                        full_name=f'{user.username}',
                        email=user.email,
                        shipping_address='123 Example Street',
                        amount_paid=2,
                        date_ordered=current_date,
                        user=user
                    )

                    # Dodawanie pozycji zamówienia
                    num_items = random.randint(1, 5)
                    for _ in range(num_items):
                        product = random.choice(product_objects)
                        quantity = random.randint(1, 3)
                        price = product.price * quantity
                        amount_paid += price

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=price,
                            user=user
                        )

                    # Aktualizacja kwoty zapłaconej
                    order.amount_paid = amount_paid
                    order.save()

        self.stdout.write(self.style.SUCCESS('The test data was successfully generated.'))
