# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/add_expense/', views.add_expense, name='add_expense'),
    path('group/<int:group_id>/add_member/', views.add_member, name='add_member'),
    path('group/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('group/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
]
