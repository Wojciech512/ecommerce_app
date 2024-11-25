from django.urls import path

from . import views


from django.contrib.auth import views as auth_views
urlpatterns = [
    path("register", views.register, name="register"),
    path(
        "email-verification/<str:uidb64>/<str:token>/",
        views.email_verification,
        name="email-verification",
    ),
    path(
        "email-verification-sent",
        views.email_verification_sent,
        name="email-verification-sent",
    ),
    path(
        "email-verification-success",
        views.email_verification_success,
        name="email-verification-success",
    ),
    path(
        "email-verification-failed",
        views.email_verification_failed,
        name="email-verification-failed",
    ),
    path("login", views.login, name="login"),
    path("user-logout", views.user_logout, name="user-logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile-management", views.profile_management, name="profile-management"),
    path("delete-account", views.delete_account, name="delete-account"),
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password-reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path("manage-shipping", views.manage_shipping, name="manage-shipping"),
    path("track-orders", views.track_orders, name="track-orders"),
    path("admin_dashboard", views.admin_dashboard, name="admin-dashboard"),
    path("admin/delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
    path("admin/change-user-permissions/<int:user_id>/", views.change_user_permissions, name="change_user_permissions"),
    path('admin/update-product/<int:product_id>/', views.update_product, name='update_product'),
    path('admin/delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin/create-category/', views.create_category, name='create_category'),
    path('admin/create-product/', views.create_product, name='create_product'),
    path('admin/delete-logs/', views.delete_logs, name='delete_logs'),
    path('admin_dashboard/generate_pdf_report/', views.generate_pdf_report, name='generate_pdf_report'),
]
