
from django.urls import path , include
from . import views
urlpatterns = [

    path("", include("django.contrib.auth.urls")),
    path("profile",views.profile_page,name="profile_page"),
    path("signup",views.signup,name="signup"),
    path("update",views.update,name="update"),
    # path("delete" , views.delete_account),
 path('activate/<uidb64>/<token>', views.activate, name='activate')



]
