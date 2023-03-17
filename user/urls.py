
from django.urls import path , include
from . import views
# urlpatterns = [

#     path("", include("django.contrib.auth.urls")),
#     path("profile",views.profile_page,name="profile_page"),
#     path("signup",views.signup,name="signup"),
#     path("update",views.update,name="update"),
#     # path("delete" , views.delete_account),
#  path('activate/<uidb64>/<token>', views.activate, name='activate')



# ]

urlpatterns=[
    path('register/',views.users_register,name='register'),
    path('login/',views.users_login,name='login'),
    path('logout/', views.users_logout, name='logout'),
     path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/my_donations', views.my_donations, name='my_donation'),
    path('profile/my_projects', views.my_projects, name='my_projects'),
    path('profile/delete', views.delete_account, name='delete'),
    path('profile/',views.user_profile,name='profile'),
    #  path("password_change", views.password_change, name="password_change"),


]
