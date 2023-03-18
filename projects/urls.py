
# urls for projects only 


from django.urls import path

from projects.views import *


urlpatterns = [
    path('',AllProjects.as_view(),name="allprojects"),
    path('detail/<int:pk>',ProjectDetailedView,name="detail"),
    # path('createproject/',ProjectCreateView.as_view(),name="createproject"),
    # path('createproject/',create_project,name="createproject"),
    path('createproject/',add_project,name="createproject"),

    path('deleteproject/<int:id>', ProjectDeleteView, name='deleteproject'),
    path('updateproject/<int:_id>', update_project,name='updateproject'),
    #==========================(CommentCreateion)==========================\
    path('add-comment/<int:pk>', add_comment,name='add_comment'),
    path('delete-comment/<int:pk>', delete_comment,name='delete_comment'),
    #==========================(donateion)==========================
    path('donate/<int:pk>',donate,name="donate"),
        #==========================(rate)==========================
    path('rate/<int:pk>',rates_create,name="rateproject"),
        #==========================(rate)==========================
    path('category/<int:id>/', category, name="category"),
    path('search/', search, name="search"),
    path('<int:pk>/report-comment', report_comment,name='report_comment'),
    path('report/<int:pk>',project_report,name="reportproject"),
    path('category/<int:pk>',category_projects,name="category"),


    


]

