from django.shortcuts import redirect, render, get_object_or_404
from xhtml2pdf import pisa
from .forms import CreateUserForm, LoginForm, UpdateUserForm, ProductForm, CategoryForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order
from payment.models import OrderItem
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from store.models import Category, Product
from django.contrib import messages
from .models import Log
import json
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay, TruncMonth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from cart.models import SavedCart
matplotlib.use('Agg')

def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url=login_url)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Account verification email"
            message = render_to_string(
                "account/registration/email-verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": user_tokenizer_generate.make_token(user),
                },
            )
            Log.objects.create(user=user, event_type="unverified_registered_user", description="User registration success, email send.")
            user.email_user(subject=subject, message=message)
            return redirect("email-verification-sent")
    context = {"form": form}
    return render(request, "account/registration/register.html", context=context)

def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        Log.objects.create(user=user, event_type="email_verification_success", description="Email verification success.")
        return redirect("email-verification-success")
    else:
        Log.objects.create(user=user, event_type="email_verification_failed", description="Email verification failed.")
        return redirect("email-verification-failed")

def email_verification_sent(request):
    return render(request, "account/registration/email-verification-sent.html")

def email_verification_success(request):
    return render(request, "account/registration/email-verification-success.html")

def email_verification_failed(request):
    return render(request, "account/registration/email-verification-failed.html")

def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                Log.objects.create(user=user, event_type='login', description='User logged in.')
                try:
                    save_cart = SavedCart.objects.get(user=user)
                    request.session["session_key"] = save_cart.cart_data
                except SavedCart.DoesNotExist:
                    request.session["session_key"] = {}
                return redirect("store")
    context = {"form": form}
    return render(request, "account/login.html", context=context)

def user_logout(request):
    Log.objects.create(user=request.user, event_type='logout', description='User logged out.')

    if request.user.is_authenticated:
        saved_cart, created = SavedCart.objects.get_or_create(user=request.user)
        saved_cart.cart_data = request.session.get("session_key", {})
        saved_cart.save()

    try:
        for key in list(request.session.keys()):
            if key == "session_key":
                continue
            else:
                del request.session[key]
        request.session["session_key"] = {}
        request.session.modified = True
    except KeyError:
        pass

    messages.success(request, "Logout success")
    return redirect("store")

@login_required(login_url="login")
def dashboard(request):
    return render(request, "account/dashboard.html")

@login_required(login_url="login")
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.info(request, "Update success!")
            Log.objects.create(user=request.user, event_type='profile_management', description='User edited profile.')
            return redirect("dashboard")

    context = {"user_form": user_form}
    return render(request, "account/profile-management.html", context=context)


@login_required(login_url="login")
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        user.delete()
        messages.error(request, "Account deleted")
        Log.objects.create(user=request.user, event_type='delete_account', description=f'User "{user.username}" deleted their account.')
        return redirect("store")
    return render(request, "account/delete-account.html")


# Shipping view
@login_required(login_url="login")
def manage_shipping(request):
    try:
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()
            messages.info(request, "Update success!")
            Log.objects.create(user=request.user, event_type='manage_shipping',
                               description=f'User updated their shipping.')
            return redirect("dashboard")
    context = {"form": form}
    return render(request, "account/manage-shipping.html", context=context)


@login_required(login_url="login")
def track_orders(request):
    try:
        orders = OrderItem.objects.filter(user=request.user)
        context = {"orders": orders}
        return render(request, "account/track-orders.html", context=context)
    except:
        return render(request, "account/track-orders.html")


@admin_required(login_url="login")
def admin_dashboard(request):
    logs = Log.objects.all().order_by('-timestamp')
    logs_paginator = Paginator(logs, 10)
    logs_page = request.GET.get('logs_page')
    try:
        logs = logs_paginator.page(logs_page)
    except PageNotAnInteger:
        logs = logs_paginator.page(1)
    except EmptyPage:
        logs = logs_paginator.page(logs_page.num_pages)
    logs_start_index = (logs.number - 1) * logs_paginator.per_page

    users = User.objects.all().order_by('id')
    user_paginator = Paginator(users, 10)
    user_page = request.GET.get('user_page')
    try:
        users = user_paginator.page(user_page)
    except PageNotAnInteger:
        users = user_paginator.page(1)
    except EmptyPage:
        users = user_paginator.page(user_paginator.num_pages)
    user_start_index = (users.number - 1) * user_paginator.per_page

    products = Product.objects.all().order_by('id')
    product_paginator = Paginator(products, 10)
    product_page = request.GET.get('product_page')
    try:
        products = product_paginator.get_page(product_page)
    except PageNotAnInteger:
        products = product_paginator.page(1)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)
    product_start_index = (products.number - 1) * product_paginator.per_page

    categories = Category.objects.all()

    # Pobranie danych sprzedaży dziennej
    sales_data = (
        Order.objects.filter()
        .annotate(date=TruncDay('date_ordered'))
        .values('date')
        .annotate(total_sales=Sum('amount_paid'))
        .order_by('date')
    )

    # Pobranie danych sprzedaży miesięcznej
    monthly_sales_data = (
        Order.objects.filter()
        .annotate(month=TruncMonth('date_ordered'))
        .values('month')
        .annotate(total_sales=Sum('amount_paid'))
        .order_by('month')
    )

    # Najlepiej sprzedające się produkty
    top_products = (
        OrderItem.objects.values('product__title')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:5]
    )

    # Sprzedaż według kategorii
    sales_by_category = (
        OrderItem.objects.values('product__category__name')
        .annotate(total_sales=Sum('quantity'))
        .order_by('-total_sales')
    )

    # Liczba zamówień dziennie
    orders_per_day = (
        Order.objects.annotate(date=TruncDay('date_ordered'))
        .values('date')
        .annotate(order_count=Count('id'))
        .order_by('date')
    )

    # Tabela klientów (użytkownicy, którzy nie są superuserami)
    customers = User.objects.filter(is_superuser=False)

    # Serializacja danych do formatu JSON
    sales_data_json = json.dumps(list(sales_data), default=str)
    monthly_sales_data_json = json.dumps(list(monthly_sales_data), default=str)
    top_products_json = json.dumps(list(top_products))
    sales_by_category_json = json.dumps(list(sales_by_category))
    orders_per_day_json = json.dumps(list(orders_per_day), default=str)

    context = {
        "logs_start_index": logs_start_index,
        "user_start_index": user_start_index,
        "product_start_index": product_start_index,
        "users": users,
        "categories": categories,
        "products": products,
        "logs": logs,
        "sales_data": sales_data_json,
        "monthly_sales_data": monthly_sales_data_json,
        "top_products": top_products_json,
        "sales_by_category": sales_by_category_json,
        "orders_per_day": orders_per_day_json,
        "customers": customers,
    }
    return render(request, "account/admin/admin-dashboard.html", context=context)


@admin_required(login_url="login")
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)

    if user == request.user:
        messages.error(request, "You can't delete your account!")
        return redirect("admin-dashboard")

    user.delete()
    messages.info(request, f"User {user.username} has been deleted.")
    Log.objects.create(user=request.user, event_type='delete_account',
                       description=f'Admin deleted {user.username} account.')
    return redirect("admin-dashboard")


@admin_required(login_url="login")
def change_user_permissions(request, user_id):
    if request.method == "POST":
        operation_type = request.POST.get('operation_type')
        user = User.objects.get(id=user_id)

        if operation_type == "change_permissions":
            if user.is_superuser:
                if User.objects.filter(is_superuser=True).count() <= 1:
                    messages.error(request, "The last super user cannot be deleted!")
                    return redirect("admin-dashboard")

                user.is_superuser = False
                user.is_staff = False
                user.save()
                messages.info(request, f"The user {user.username} has lost administrator privileges.")
                Log.objects.create(user=request.user, event_type='change_user_permissions',
                                   description=f'Admin changed user {user.username} privileges to user.')
            else:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                messages.info(request, f"The user {user.username} has become an administrator.")
                Log.objects.create(user=request.user, event_type='change_user_permissions',
                                   description=f'Admin changed user {user.username} privileges to admin.')

        return redirect("admin-dashboard")

@admin_required(login_url="login")
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, f'The product “{product.title}” has been updated.')
            Log.objects.create(user=request.user, event_type='update_product',
                               description=f'Product {product.title} updated.')
            return redirect('admin-dashboard')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'account/admin/update-product.html', context)

@admin_required(login_url="login")
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.info(request, f'The product “{product.title}” has been removed.')
    Log.objects.create(user=request.user, event_type='delete_product',
                       description=f'Product {product.title} deleted.')
    return redirect('admin-dashboard')

@admin_required(login_url="login")
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "The product has been successfully added.")
            Log.objects.create(user=request.user, event_type='create_product',
                               description=f'Product created.')
            return redirect('admin-dashboard')
    else:
        form = ProductForm()

    return render(request, 'account/admin/create-product.html', {'form': form})

@admin_required(login_url="login")
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The category has been successfully added.")
            Log.objects.create(user=request.user, event_type='create_category',
                               description=f'Category created.')
            return redirect('admin-dashboard')
    else:
        form = CategoryForm()
    return render(request, 'account/admin/create-category.html', {'form': form})

@admin_required(login_url="login")
def delete_logs(request):
    if request.method == 'POST':
        Log.objects.all().delete()
        messages.info(request, "The logs have been deleted.")
    return redirect('admin-dashboard')

def generate_chart(x, y, title):
    plt.figure(figsize=(10,6))
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

@admin_required(login_url="login")
def generate_pdf_report(request):
    sales_data = (
        Order.objects.filter()
        .annotate(date=TruncDay('date_ordered'))
        .values('date')
        .annotate(total_sales=Sum('amount_paid'))
        .order_by('date')
    )

    monthly_sales_data = (
        Order.objects.filter()
        .annotate(month=TruncMonth('date_ordered'))
        .values('month')
        .annotate(total_sales=Sum('amount_paid'))
        .order_by('month')
    )

    top_products = (
        OrderItem.objects.values('product__title')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:5]
    )

    sales_by_category = (
        OrderItem.objects.values('product__category__name')
        .annotate(total_sales=Sum('quantity'))
        .order_by('-total_sales')
    )

    customers = User.objects.filter(is_superuser=False)

    dates = [item['date'].strftime('%Y-%m-%d') for item in sales_data]
    total_sales = [item['total_sales'] for item in sales_data]
    daily_sales_chart = generate_chart(dates, total_sales, 'Daily Sales')

    months = [item['month'].strftime('%Y-%m') for item in monthly_sales_data]
    monthly_total_sales = [item['total_sales'] for item in monthly_sales_data]
    monthly_sales_chart = generate_chart(months, monthly_total_sales, 'Monthly Sales')

    product_titles = [item['product__title'] for item in top_products]
    product_quantities = [item['total_quantity'] for item in top_products]
    plt.figure(figsize=(10,6))
    plt.bar(product_titles, product_quantities)
    plt.title('Best Selling Products')
    plt.xlabel('Product')
    plt.ylabel('Quantity Sold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    top_products_chart = base64.b64encode(image_png).decode('utf-8')

    category_names = [item['product__category__name'] for item in sales_by_category]
    category_sales = [item['total_sales'] for item in sales_by_category]
    plt.figure(figsize=(10,6))
    plt.bar(category_names, category_sales)
    plt.title('Sales by Category')
    plt.xlabel('Category')
    plt.ylabel('Quantity Sold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    sales_by_category_chart = base64.b64encode(image_png).decode('utf-8')

    from datetime import datetime, timedelta
    last_week = datetime.now() - timedelta(days=7)
    weekly_sales = (
        Order.objects.filter(date_ordered__gte=last_week)
        .annotate(date=TruncDay('date_ordered'))
        .values('date')
        .annotate(total_sales=Sum('amount_paid'))
        .order_by('date')
    )

    context = {
        'sales_data': sales_data,
        'monthly_sales_data': monthly_sales_data,
        'top_products': top_products,
        'sales_by_category': sales_by_category,
        'customers': customers,
        'daily_sales_chart': daily_sales_chart,
        'monthly_sales_chart': monthly_sales_chart,
        'top_products_chart': top_products_chart,
        'sales_by_category_chart': sales_by_category_chart,
        'weekly_sales': weekly_sales,
    }

    template_path = 'account/pdf/pdf_report.html'
    html = render_to_string(template_path, context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        messages.error(request, 'Error during PDF generation.%s' % pisa_status.err )
        return HttpResponse('Error during PDF generation: %s' % pisa_status.err)
    return response

