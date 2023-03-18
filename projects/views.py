from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView
from projects.forms import  AddProject, EditProject, ProjectModelForm ,CommentModelForm ,DonateModelForm, RatesModelForm, ReportCommentModelForm, ReportProjectModelForm
from projects.models import Category, Comment, Donation, Picture, Project, Rates, ReportComment, ReportProject, Tag
from django.db.models import  Sum ,Avg
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
# ============================(start projects)===================
class AllProjects(ListView):
    model = Project
    template_name = 'project_list.html'



def ProjectDetailedView (request,pk ): 
    project = get_object_or_404(Project ,id=pk)
    average_rating = Rates.objects.filter(project_id=pk).aggregate(Avg('rate'))['rate__avg']
    form = CommentModelForm
    donate =DonateModelForm
    rate=RatesModelForm
    total_donation = Donation.Newamount(project)
    pictures = Picture.objects.filter(project_id=pk)
    avg_rate=Rates.Avgrate(project)
    reportcomment=ReportCommentModelForm()
    reportproject=ReportProjectModelForm()
    # get all same category 
    tag_names = [tag.tag_name for tag in project.tags.all()]  # retrieve the names of all tags associated with the project
    tags = Tag.objects.filter(tag_name__in=tag_names)
    projects = Project.objects.filter(tags__in=tags).distinct()
    Project.objects.filter(id=pk).update(avg_rate=average_rating)


    # context={'pictures':pictures}
    context= {'form': form,'donate':donate,'total_donation':total_donation,'avg_rate':avg_rate, 'rate':rate,'project' : project,'pictures':pictures,'projects':projects,'reportcomment':reportcomment,'reportproject':reportproject}
    return render(request, 'project_detail.html',context)

# def tagged(request, slug):
#     tag = get_object_or_404(Tag, slug=slug)
#     project = Project.objects.filter(tags=tag)
#     context = {
#         'tag':tag,
#         'project':project,
#     }
#     return render(request, 'project_list.html', context)

# def create_project(request):
#     pass



# class ProjectUpdateView(UpdateView):
#     model = Project
#     template_name = 'update_project.html'
#     form_class = ProjectModelForm
#     success_url = '/projects/'
#     #  return redirect('detail', project.id)

@login_required(login_url='/user/login')
def update_project(request, _id):
    submitted = False
    if request.method == 'POST':
        project = Project.objects.get(id=_id)
        edit_form = EditProject(request.POST, instance=project)
        edit_form.save()
        tages = request.POST['tags'].split(" ")
        for tag in tages:
            obj, created = Tag.objects.get_or_create(
                tag_name=tag,
                defaults={'tag_name': tag},
            )
            if obj:
                project.tags.add(obj)
            elif created:
                project.tags.add(created)

        return redirect('detail',project.id)
    else:
        if 'submitted' in request.GET:
            submitted = True
        project = Project.objects.get(id=_id)
        oldtags=Tag.objects.filter(project=project)
        oldtagsstr=' '.join([str(i) for i in oldtags])
        oldtags.delete()
        edit_form = EditProject(instance=project)
    return render(request, 'update_project.html', {'form': edit_form, 'oldtags':oldtagsstr, 'submitted': submitted})


@login_required(login_url='/user/login')
def ProjectDeleteView(request,id):
    project = get_object_or_404(Project ,id=id)
    target=project.total_target
    print('target--------------', target)
    # target = Project.get_target(id)
    total_donation = Donation.Newamount(project)
    print(total_donation)
    if total_donation < 0.25 * target:
        project.delete()
        return redirect('allprojects')
    else:
        return redirect('detail', project.id)
# ============================(End projects)===================
# ============================(start donate)===================
@login_required(login_url='/user/login')

def donate(request, pk):
    project = Project.objects.get(id=pk)
    # print(Donation.objects.values('amount').annotate(Sum('amount')))
    donate = DonateModelForm(instance=project)
    if request.method == 'POST':
        donate = DonateModelForm(request.POST ,instance=project)
        if donate.is_valid():
            user = request.user
            print(user) # admin 
            amount = request.POST.get('amount')
            c = Donation(project=project, user=user, amount=amount)
            # DonateModelForm.save(self=c) 
            c.save()
            # new=Donation.objects.filter(project=project).aggregate(Sum('amount'))
            # print(new)
            return redirect('detail', project.id)
        else:
            print('form is not_valid')
    else:
        donate = DonateModelForm()    
        return render(request, 'donate.html', context={ 'donate': donate})
# ============================(End donate)===================
# ============================(start comment)===================
@login_required(login_url='/user/login')
def add_comment(request,pk):
    eachproject=Project.objects.get(id=pk)
    form=CommentModelForm(instance=eachproject)
    if request.method == 'POST':
        form = CommentModelForm(request.POST, instance=eachproject)
        if form.is_valid():
            name = request.user
            print(name)
            print(eachproject)
            body = request.POST.get('comment_body')
            print(body)
            c = Comment(project =eachproject, user=name, comment_body=body)
            c.save()
            return redirect('detail', eachproject.id) 
      
# ////////////////
@login_required(login_url='/user/login')

def delete_comment(request,pk):
    # get all comment based on project
    comment =Comment.objects.filter(project=pk).first()
    product_id = comment.project.id
    comment.delete()
    return redirect(reverse('detail', args=[product_id]))

# ======================================    
@login_required(login_url='/user/login')

def rates_create(request,pk):
    project = Project.objects.get(id=pk)
    rate = RatesModelForm(instance=project)
    if request.method == 'POST':
        rate = RatesModelForm(request.POST ,instance=project)
        if rate.is_valid():
            user = request.user
            print(user) # admin 
            rate = request.POST.get('rate')
            print(rate) # project
            print(project) # project
            c = Rates(project=project, user=user, rate=rate)
            c.save()
            return redirect('detail', project.id)
        else:
            print('form is not_valid')
    else:
        rate = RatesModelForm()    
        return render(request, 'project_rate.html', context={ 'rate': rate })
    
# ==================================================================

# ================================(home page)===================================================
def homepage(request):
    first = Project.objects.order_by('-id')[:5]
    f_projects = Project.objects.filter(featured=True)[:5]

    category= Category.objects.all()
    print (first ,'===============')
    projectrate = Project.objects.order_by('-avg_rate')[:5]
    project = Category.objects.all()
    return render(request, 'home_page.html' ,context = {'first':first,'category':category,'projects': projectrate, 'project':project,'f_projects':f_projects})

# def project_home(request):
#     projectrate = Project.objects.order_by('-avg_rate')[:5]
#     project = Category.objects.all()
#     return render(request, 'home.html', context={ 'projects': projectrate, 'project':project })


# ==================
def category(request,id):
    mycategory = get_object_or_404(Category, pk=id)
    return render(request, 'category.html', context={"mycategory": mycategory})

# highest five rated running projects to
# encourage users to donate

def highestrated (request):
    high =Rates.objects.all()
    
    return render(request, 'category.html', context={"high": high})


# _______________________


def search(request):
    query = request.GET.get('q')
    if query:
        projects = Project.objects.filter(title__icontains=query)
    else:
        projects = Project.objects.all()
    context = {
        'projects': projects,
        'query': query,
    }
    return render(request, 'search_project.html', context)

# addd project 

@login_required(login_url='/user/login')

def add_project(request):
    if request.method == 'POST':
        form = AddProject(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            project = Project()
            project.title = cd['title']
            project.details = cd['Details']
            project.category = cd['Category']
            project.current_money = cd['CurrentMoney']
            project.total_target = cd['TotalTarget']
            project.end_time = cd['EndTime']
            project.user_id = request.user
            project.save()

            tages = cd['Tags'].split(" ")
            for tag in tages:
                obj, created = Tag.objects.get_or_create(
                    tag_name=tag,
                    defaults={'tag_name': tag},
                )
                if obj:
                    project.tags.add(obj)
                elif created:
                    project.tags.add(created)

            for file in request.FILES.keys():
                image_file = request.FILES.getlist(file)
                print("imffileeee", image_file)
                for i in image_file:
                    fs = FileSystemStorage()
                    filename = fs.save('images/projects/' + i.name, i)
                    img = Picture()
                    img.pic_path = filename
                    img.project_id = project
                    img.save()

            return HttpResponseRedirect('/projects')

    else:
        form = AddProject()
       

    return render(request, 'create_project.html', {'form': form })



@login_required(login_url='/user/login')

def report_comment(request,pk):
    eachproject=Project.objects.get(id=pk)
    print(eachproject,"kemooooo")
    form=ReportCommentModelForm(instance=eachproject)
    if request.method == 'POST':
        form = ReportCommentModelForm(request.POST, instance=eachproject)
        if form.is_valid():
            name = request.user.username
            # report=request.POST.get('boolean_field')
            # print(report)
            field = form.cleaned_data['boolean_field']
            r = ReportComment(boolean_field=field,user_id=name,project=eachproject)
            r.save()
            return redirect('detail' , eachproject.id) 
        else:
            print('form is invalid')
    else:
        context={
        'form': form,
        'eachproject':eachproject
        }
    return render(request, 'report.html',context )


    # report project 
@login_required(login_url='/user/login')

def project_report(request,pk):
    project = Project.objects.get(id=pk)
    form = ReportProjectModelForm(instance=project)
    if request.method == 'POST':
        form = ReportProjectModelForm(request.POST ,instance=project)
        if form.is_valid():
            user = request.user
            print(user) # admin 
            report_project = form.cleaned_data['report_project']
            print(report_project) # project
            print(project) # project
            c = ReportProject(project=project, user=user, report_project=report_project)
            c.save()
            return redirect('detail',project.id)
        else:
            print('form is not_valid')
    else:
        form = ReportProjectModelForm() 
        return render(request, 'project_report.html', context={ 'form': form })
    



def category_projects(request, pk):
    category = Category.objects.get(id=pk)
    project_category = Project.objects.filter(category=category)
    return render(request, 'category.html', context={ 'category':project_category})