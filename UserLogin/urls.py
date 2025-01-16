''' urls.py for UserLogin app '''
''''''
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.login, name='login'),
#     path('register/', views.register, name='register'),
#     path('logout/', views.logout, name='logout'),
#     path('reset_password/', views.reset_password, name='reset_password'),
#     path('profile/', views.profile, name='profile'),
#     path('edit_profile/', views.edit_profile, name='edit_profile'),
#     path('change_password/', views.change_password, name='change_password'),
#     path('delete_user/', views.delete_user, name='delete_user'),
# ]


from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    
]


