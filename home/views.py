from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.urls import reverse
from .forms import JobApplicationForm
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    projects = Project.objects.order_by('?')[:4]
    category = Category.objects.all()
    latest_blogs = Blog.objects.all()[:2]  # Meta ordering ensures newest first
    return render(request, 'home/home.html', {
        'projects': projects,
        'category': category,
        'latest_blogs': latest_blogs,
    })


def about(request):
    return render(request, 'home/about.html')


def project_detail(request, pk):
    projects = Project.objects.all()
    project = get_object_or_404(Project, pk=pk)
    images = Images.objects.filter(project_id=pk)
    category = Category.objects.all()
    next_project = Project.objects.filter(id__gt=project.id).order_by('id').first()
    previous_project = Project.objects.filter(id__lt=project.id).order_by('-id').first()
    context = {'project': project, 'images': images, 'category': category, 'projects': projects ,'next_project': next_project ,'previous_project':previous_project}
    return render(request, 'home/project-1.html', context)


def portfolio(request):
    projects = Project.objects.all()
    category = Category.objects.all()
    return render(request, 'home/portfolio.html', {'projects': projects , 'category':category})


def contact(request):
    projects = Project.objects.order_by('?')[:4]
    category = Category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Thanks for contacting us. We will keep in touch with you!')
            form = ContactForm()  # Reset the form
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'projects': projects , 'category':category , 'form':form})

# ✅ applying for publication view
def publication(request):
    return render(request, 'home/publication.html')

# ⚙️ applying for services view
def services(request):
    projects = Project.objects.order_by('?')[:4]
    category = Category.objects.all()
    return render(request, 'home/services.html', {'projects': projects ,'category':category})

# ⚙️ applying for team view
def team(request):
    return render(request, 'home/team.html')

# ✅ applying for Blog view
def blog(request):
    return render(request, 'home/blog-inner.html')


#
# def login_view(request):
#     projects = Project.objects.all()
#     category = Category.objects.all()
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             # Use the namespace if your URLs are namespaced as 'home'
#             return redirect('home:preview')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'home/login.html', {'projects': projects, 'category':category})
#
#
# @login_required
# def preview_view(request):
#     try:
#         # Retrieve the ClientPreview for the current user
#         client_preview = ClientPreview.objects.get(user=request.user)
#     except ClientPreview.DoesNotExist:
#         messages.error(request, "No preview content found for your account.")
#         return redirect('home:login')
#
#     # Assuming your unique preview templates are stored in the "home" subfolder,
#     # prepend "home/" to the template_name stored in the model.
#     template_path = f"previews/{client_preview.template_name}/index.html"
#     return render(request, template_path, {'user': request.user})
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('home:login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home:preview_default')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'home/login.html')


@login_required
def preview_view(request, page="index.html"):
    """
    Renders a dynamic preview page based on the path.
    If no path is provided, defaults to index.html.
    """
    try:
        client_preview = ClientPreview.objects.get(user=request.user)
    except ClientPreview.DoesNotExist:
        messages.error(request, "No preview content found for your account.")
        return redirect('home:login')

    # Build the template path dynamically.
    # For example, if client_preview.template_name is "client_restaurant" and page is "menu.html",
    # then the template path will be "previews/client_restaurant/menu.html"
    template_path = f"previews/{client_preview.template_name}/{page}"
    return render(request, template_path, {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('home:login')
    
    
 
def job_list(request):
    categories = JobCategory.objects.all()
    return render(request, 'home/jobs.html', {'categories': categories})

def job_apply(request, slug):
    category = get_object_or_404(JobCategory, slug=slug)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.category = category
            app.save()
            return redirect(reverse('home:thank_you'))
    else:
        form = JobApplicationForm()
    return render(request, 'home/job_apply.html', {
        'category': category,
        'form': form,
    })

def thank_you(request):
    return render(request, 'home/thank_you.html')

def blog_list(request):
    blog_qs = Blog.objects.all()
    paginator = Paginator(blog_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    projects = Project.objects.order_by('?')[:4]
    category = Category.objects.all()
    return render(request, 'home/blogs.html', {
        'page_obj': page_obj,'projects': projects ,'category':category
    })

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    projects = Project.objects.order_by('?')[:4]
    category = Category.objects.all()
    return render(request, 'home/blog_detail.html', {'blog': blog,'projects': projects ,'category':category})