from django.urls import path
from TCGTrackingTool import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    # default page
    path("", views.home, name="home"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("FAQ/", views.faq, name="FAQ"),
    path("support/", views.support, name="support"),
    path("profile/", views.profile, name="profile"),
    path("notifications/", views.notifications, name="notifications"),
    path("settings/", views.user_settings, name="user_settings"),
    path("account-created/", views.account_created, name="account-created"),
    path("register/", views.register, name="register"),
    path("signin/", views.signin, name="signin"),
    path('logout/', views.logout_user, name='logout'),
    path("product/", views.product, name="product"),
    path("notFoundError/", views.notfounderror, name="notFoundError"),
    path("info-recovery/", views.info_recovery, name="info-recovery"),
    path("add-card-view", views.add_card_view, name="add-card"),
    path('remove-card-view', views.remove_card_view, name='remove-card'),
    path('current-price-detail', views.current_price_detail,
         name='current-price-detail'),
    path('price-history-detail', views.price_history_detail,
         name='price-history-detail'),
    path('create-notification', views.create_notification,
         name='create-notification'),
     path("messages/", views.messages, name="messages"),

     # Change Password
     path('info-recovery/forgot-password/', auth_views.PasswordResetView.as_view(template_name="TCGTrackingTool/forgot-password.html"), name="password_reset"),
     path('info-recovery/forgot-password/done/', auth_views.PasswordResetDoneView.as_view(template_name="TCGTrackingTool/forgot-password-done.html"), name="password_reset_done"),
     path('info-recovery/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="TCGTrackingTool/forgot-password-reset.html"), name="password_reset_confirm"),
     path('info-recovery/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="TCGTrackingTool/forgot-password-reset-done.html"), name="password_reset_complete")
]
