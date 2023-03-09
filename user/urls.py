
from django.urls import path
from . import views
urlpatterns = [
    path("login/",views.login),
    path("signup",views.signup,name="home"),
    path("logout", views.logout),
    path("delete" , views.delete_account),
     path('activate/<uidb64>/<token>', views.activate, name='activate')



]
