from django.db import models
from django.contrib.auth.models import User
from django.db.models import  Sum,Avg


# Create your models here.
# ==============================(category)=============================================
class Category(models.Model):
    cat_title = models.CharField(max_length=255)
    cat_description = models.CharField(max_length=255)
    def __str__(self):
        return self.cat_title  
# ==============================(project)=============================================



# _______________________TAG_________________

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name

    
class Project(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    details = models.TextField(blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    current_money = models.IntegerField(default=0)
    total_target = models.IntegerField(blank=False, null=False)
    tags = models.ManyToManyField(Tag)
    start_time = models.DateField(auto_now_add=True)
    end_time = models.DateField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    avg_rate = models.IntegerField(null=True,default=0)
    featured=models.BooleanField(default=False)

    def __str__(self):
        return self.title 
# =======================(donation)==========================================

class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='user')
    amount = models.PositiveIntegerField(null=True)
    def __str__(self):
        return (f"{self.user} Donate to {self.project}")
    @classmethod
    def Newamount(cls,project):
         t_donation =cls.objects.filter(project=project).aggregate(Sum('amount'))['amount__sum']
         if t_donation == None :
              return 0 
         else :  
             
             return t_donation


# ================================(comments)=================================================
class Comment(models.Model):
    ###############using on_delete beacuse when project is deleted also all comment that realted to it will also deleted
    project = models.ForeignKey(Project,related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='userCommenter')
    # commenter_name=models.ForeignKey(User ,on_delete=models.CASCADE, null=True,related_name='cuser')
    comment_body = models.TextField(null=True)

    def __str__(self):
        return '%s - %s' % (self.project.title,self.user)

# ================================(images)=============================================
# class Pictures(models.Model):
#     image = models.ImageField(max_length=255, upload_to='projects/images')
#     project = models.ForeignKey(
#         Project, on_delete=models.CASCADE, related_name='images')
#     def __str__(self):
#         return f"/media/{self.image}"


# ================================(rate prioject)=============================================
class Rates(models.Model):
    rate = models.IntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
      return (f"{self.user} Rate to {self.project}")
    @classmethod
    def Avgrate(cls,project):
         x= cls.objects.filter(project=project).aggregate(Avg('rate'))['rate__avg']
         if x == None :
             return 0
         else:
             return x

# ==============================================================================
# class ReportComment(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE,null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     report = models.BooleanField(null=True, default=False)
#     def __str__(self):
#       return (f"{self.user} Report to {self.comment}")

# ============================================================
class Picture(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    pic_path = models.ImageField(
        upload_to='images/projects/')


    def __str__(self):
        return str(self.pic_path)
    
# class ReportComment(models.Model):
#     project = models.ForeignKey(Project,related_name="commentrr", on_delete=models.CASCADE,null=True)
#     user_id = models.TextField(null=True)
#     boolean_field = models.BooleanField(default=True)

class ReportComment(models.Model):
    project = models.ForeignKey(Project,related_name="commentrr", on_delete=models.CASCADE,null=True)
    user_id = models.TextField(null=True)
    boolean_field = models.BooleanField(default=True)



class ReportProject(models.Model):
    report_project = models.BooleanField(default=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return (f"{self.project}")