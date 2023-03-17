
import datetime
from django import forms
from projects.models import Category, Comment, Picture, Project ,Donation, Rates, ReportComment, ReportProject

class ProjectModelForm(forms.Form):
    title = forms.CharField(max_length=50, label='Project Title')
    details = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    total_target = forms.IntegerField(min_value=0, label="Total Target")
    tags = forms.CharField(max_length=500, label='Project Tages', widget=forms.TextInput(attrs={'placeholder': 'type your tages seperated by blank space...'}))
    end_time = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, datetime.date.today().year + 20)),
                              label='End Time')
    Pictures = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
# class ProjectModelForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         # fields = '__all__'
#         fields = ['title','details','category','total_target','tags','start_time','end_time',]
# ========================(start comment form)=========================================
class CommentModelForm(forms.ModelForm):
    comment_body = forms.CharField(widget=forms.Textarea(attrs={'rows':'4',
                                                                
                                                                }))
    class Meta:
        model = Comment
        # fields = '__all__'
        # fields = ['text',]
        fields = ('comment_body',)
# ========================(start donate form)=========================================

class DonateModelForm(forms.ModelForm):
    class Meta:
        model = Donation
        # fields = '__all__'
        fields = ('amount',)

# ========================(start rate form)=========================================
class RatesModelForm(forms.ModelForm):
    class Meta:
        model = Rates
        # fields = 'all'
        fields = ('rate',)

# class ReportModelForm(forms.ModelForm):
#     class Meta:
#         model = ReportComment
#         # fields = '_all_'
#         fields = ('report',)

# class PictureForm(forms.ModelForm):
#     images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

#     class Meta:
#         model = Picture
#         fields = ('images',)



class AddProject(forms.Form):
    title = forms.CharField(max_length=50, label='Project Title')
    Details = forms.CharField(widget=forms.Textarea)
    Category = forms.ModelChoiceField(queryset=Category.objects.all())
    CurrentMoney = forms.IntegerField(min_value=0, label='Current money')
    TotalTarget = forms.IntegerField(min_value=0, label="Total Target")
    Tags = forms.CharField(max_length=500, label='Project Tages', widget=forms.TextInput(attrs={'placeholder': 'type your tages seperated by blank space...'}))
    EndTime = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, datetime.date.today().year + 20)),
                              label='End Time')
    Pictures = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ReportCommentModelForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        # fields = '_all_'
        # fields = ['text',]
        fields = ('boolean_field',)

class ReportProjectModelForm(forms.ModelForm):
    class Meta:
        model = ReportProject
        # fields = 'all'
        fields = ('report_project',)



class EditProject(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('start_time', 'user_id','tags','avg_rate',)
        widgets = {
            'end_time': forms.SelectDateWidget(years=range(2020, datetime.date.today().year + 20)),
        }