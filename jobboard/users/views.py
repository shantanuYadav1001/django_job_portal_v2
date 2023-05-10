from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import SignupForm, LoginForm, PostJobForm, JobApplicationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from django.db.models import Q

# # Create your views here.
# class ApplicantRegistrationView(View):
#     def get(self, request):
#         form = ApplicantRegistrationForm()
#         return render(request, "applicantregistration.html", {'form' : form})
    
#     def post(self, request):
#         form = ApplicantRegistrationForm(request.POST)
#         if form.is_valid():
#             messages.success(request, "Registered Successfully!!")
#             form.save()
#         return render(request, "applicantregistration.html", {'form' : form})

class SignupView(View):
    form_class = SignupForm
    template_name = 'new/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            #return redirect(reverse_lazy('applicant_login'))
            messages.success(request, 'Account created successfully')
            return redirect('users:applicant_login')

        return render(request, self.template_name, {'form': form})



class LoginView(LoginView):
    template_name = 'new/login.html'
    form_class = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('users:home')

    def form_valid(self, form):
        messages.success(self.request, 'You have been logged in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)
    

@login_required
def dashboard(request):
    return render(request, 'index.html')

@login_required
def sign_out(request):
    logout(request)
    return redirect('users:applicant_login')


@login_required
def post_job(request):
    is_logged_in = request.user.is_authenticated
    is_employer = request.user.is_employer
    if request.user.is_employer:
        if request.method == 'POST':
            form = PostJobForm(request.POST, request.FILES)
            if form.is_valid():
                job = form.save(commit=False)
                
                # set the employer to the current user
                job.employer = request.user

                form.save()
                
                return redirect('users:home')
        else:
            form = PostJobForm()
        return render(request, 'new/add_job_form.html', {'form': form, 'is_logged_in': is_logged_in, 
        'is_employer' : is_employer})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('users:applicant_login')


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})





@login_required
def job_apply(request, job_id):
    is_logged_in = request.user.is_authenticated
    is_employer = request.user.is_employer
    job = get_object_or_404(Job, id=job_id)
    if request.user.is_employer == True:
        return redirect('users:joblist')
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.job = job
            job_application.applicant = request.user
            job_application.save()
            #return redirect('job_detail', job_id=job_id)
            return redirect('users:home')
    else:
        form = JobApplicationForm()
    return render(request, 'new/job_application_form.html', {'job': job, 'form': form, 'is_logged_in': is_logged_in, 
        'is_employer' : is_employer})

def test(request, job_id):
    return render(job_id)


#SHOWS JOBS APPLED BY THE USER
@login_required
def my_applied_jobs(request):
    is_logged_in = request.user.is_authenticated
    is_employer = request.user.is_employer
    if request.user.is_employer == False:
        job_applications = JobApplication.objects.filter(applicant=request.user)
        jobs = [job_application.job for job_application in job_applications]
        return render(request, 'new/my_applications.html', {'jobs': jobs, 'is_logged_in': is_logged_in, 
        'is_employer' : is_employer})
    else:
        return redirect('users:joblist')



@login_required
def employer_job_list(request):
    is_logged_in = request.user.is_authenticated
    is_employer = request.user.is_employer
    if request.user.is_employer == True:
        jobs = Job.objects.filter(employer=request.user)
        return render(request, 'new/employer_jobs.html', {'jobs': jobs, 'is_logged_in': is_logged_in, 
        'is_employer' : is_employer})
    else:
        return redirect('users:joblist')


@login_required
def view_job_applications(request, job_id):
    is_logged_in = request.user.is_authenticated
    is_employer = request.user.is_employer
    job = get_object_or_404(Job, id=job_id)
    job_applicants = JobApplication.objects.filter(job=job)

    context = {
        'job': job,
        'job_applicants': job_applicants,
        'is_logged_in': is_logged_in, 
        'is_employer' : is_employer
    }
    return render(request, 'new/view_applicants.html', context)


def homeView(request):
    jobs = Job.objects.all()
    is_logged_in = request.user.is_authenticated
    if is_logged_in:
        is_employer = request.user.is_employer
        if request.user.is_employer:
            return render(request, 'new/index.html', {'is_logged_in': is_logged_in, 'jobs' : jobs, 'is_employer' : is_employer})
        else:
            return render(request, 'new/index.html', {'is_logged_in': is_logged_in, 'jobs' : jobs, 'is_employer' : False})
    else:
        return render(request, 'new/index.html', {'is_logged_in': False, 'jobs' : jobs, 'is_employer' : False})
    


@login_required
def edit_job(request, job_id):
    is_logged_in = request.user.is_authenticated
    is_employer = request.user.is_employer
    if request.user.is_employer == True:
        job = get_object_or_404(Job, id=job_id)
        form = PostJobForm(instance=job)
        if request.method == 'POST':
            form = PostJobForm(request.POST, request.FILES, instance=job)
            if form.is_valid():
                form.save()
                return redirect('users:employer_job_list', job_id=job.id)
        return render(request, 'new/job_application_form.html', {'form': form, 'is_logged_in': is_logged_in, 'is_employer' : is_employer})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('users:home')

@login_required
def application_detail_view(request, application_id):
    is_logged_in = request.user.is_authenticated
    is_employer = request.user.is_employer
    applicant = get_object_or_404(JobApplication, id=application_id)
    return render(request, 'new/application_detail.html', {'applicant': applicant, 'is_logged_in': is_logged_in, 'is_employer' : is_employer})



@login_required
def job_details(request, job_id):
    is_logged_in = request.user.is_authenticated
    is_employer = request.user.is_employer
    job = get_object_or_404(Job, id=job_id)

    return render(request, 'new/job_detail.html', {'job': job, 'is_logged_in': is_logged_in, 
    'is_employer' : is_employer})
  


def job_search(request):
    query = request.GET.get("q")
    if query:
        jobs = Job.objects.filter(Q(company_name__icontains=query) | Q(job_title__icontains=query) | Q(location__icontains=query)).distinct()
    else:
        jobs = Job.objects.all()

    # context = {'jobs': jobs,
    #            'query': query}
    #return render(request, 'new/job_search.html', context)
    is_logged_in = request.user.is_authenticated
    if is_logged_in:
        is_employer = request.user.is_employer
        if request.user.is_employer:
            return render(request, 'new/job_search.html', {'is_logged_in': is_logged_in, 'jobs' : jobs,'query': query, 'is_employer' : is_employer})
        else:
            return render(request, 'new/job_search.html', {'is_logged_in': is_logged_in, 'jobs' : jobs, 'query': query,'is_employer' : False})
    else:
        return render(request, 'new/job_search.html', {'is_logged_in': False, 'jobs' : jobs, 'query': query, 'is_employer' : False})