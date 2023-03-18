
from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views
# urlpatterns = [

#     path("", include("django.contrib.auth.urls")),
#     path("profile",views.profile_page,name="profile_page"),
#     path("signup",views.signup,name="signup"),
#     path("update",views.update,name="update"),
#     # path("delete" , views.delete_account),
#  path('activate/<uidb64>/<token>', views.activate, name='activate')



# ]

urlpatterns=[
    path("reset_password", views.password_reset_request, name="reset_password"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('register/',views.users_register,name='register'),
    path('login/',views.users_login,name='login'),
    path('logout/', views.users_logout, name='logout'),
     path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/my_donations', views.my_donations, name='my_donation'),
    path('profile/my_projects', views.my_projects, name='my_projects'),
    path('profile/delete', views.delete_account, name='delete'),
    path('profile/',views.user_profile,name='profile'),

]
