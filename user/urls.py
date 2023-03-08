
from django.urls import path
from . import views
urlpatterns = [
    path("login/",views.login),
    path("signup",views.signup),
    path("logout", views.logout),
    path("delete" , views.delete_account)



]
