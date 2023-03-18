from django.contrib import admin

# Register your models here.

from projects.models import Project,Comment,Category,Donation,Rates,Picture, ReportComment, ReportProject,Tag

admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Donation)
admin.site.register(Rates)
admin.site.register(ReportComment)
admin.site.register(Picture)
admin.site.register(Tag)
admin.site.register(ReportProject)


# admin.site.register(Pictures)

