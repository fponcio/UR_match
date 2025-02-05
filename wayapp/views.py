from PyPDF2 import PdfReader
from rapidfuzz import fuzz
from django.shortcuts import redirect, render
from .models import JobPost, JobDescription
from .forms import RegisterForm, JobPostForm, JobDescriptionForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from sentence_transformers import SentenceTransformer, util

#nltk.download('punkt')
#nltk.download('stopwords')
#Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-V2')

# Create your views here.
def home(request):
    # return HttpResponse("Hello World!")
    return render(request, "home.html")
    
@csrf_exempt
def register(request):
    #group = CustomGroup.objects.create(groupname='Employers')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():    
            form.cleaned_data['status']    
            user=form.save()         
            if form.data['status'] == 'Employer':   
                user.is_staff = True 
            user=form.save()                              # user = form.save()
            login(request, user)                          # Once the user created an account, it is automaticaaly logged in         
            return redirect('/present_user')                       
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {"form": form })


def present_user(request):
    user = User.objects.get(username=request.user)
    if user.is_staff:    
        return redirect('/profile_employer')
    else:
        return redirect('/profile_user')
    

def profile_user(request):           
    current_job_post = JobPost.objects.filter(username=request.user)   
    
    if not current_job_post:
        return redirect('/create_profile')
    else:
        return redirect('/update_profile')
    

def login_user(request):
    return render(request, 'registration/login.html', {})          

 
def logout_user(request):
    logout(request)
    return redirect('/')


def affiliations(request):  
    return render(request, 'affiliations.html')  


#This module updates user account or creates jobpost
def create_profile(request):  
    if request.method == 'POST':        
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()            
            return redirect('/update_profile')
    else:
        form = JobPostForm(initial={
                                'username': request.user, 
                                'email': request.user.email,
                                'first_name': request.user.first_name,
                                'last_name': request.user.last_name})

    acc = User.objects.get(username=request.user)            
    account = RegisterForm(instance=acc)
    #bio = JobPost.objects.all()
    JDQuery_set = JobDescription.objects.all()
    return render(request, 'profile.html', {"form": form, "accform": account, "JDQuery_set": JDQuery_set })  #"bio": bio })


#Updates current job posts
def update_profile(request):        
    if request.method == "GET":
        if id == 0:
            posts = JobPostForm()
        else:
            jp = JobPost.objects.get(username=request.user)
            posts = JobPostForm(instance=jp)            
        #render prev'sly here        
    else:
        if id == 0:
            posts = JobPostForm(request.POST, request.FILES)
        else:
            jp = JobPost.objects.get(username=request.user)
            posts = JobPostForm(request.POST, request.FILES, instance=jp)
            
        if posts.is_valid():            
            update = posts.save(commit=False)
            update.jobpost = request.user.intern        #related_name
            update.save()              
            return redirect('/update_profile')

    acc = User.objects.get(username=request.user)            
    account = RegisterForm(instance=acc)  
    #bio = JobPost.objects.all()   #Extract biography data then display it on Jumbotron
    JDQuery_set = JobDescription.objects.all()
    return render(request, 'profile.html', {'posts': posts, "accform": account, "JDQuery_set": JDQuery_set }) #, "bio": bio })    
        
        
   
def profile_employer(request):
    # check if employer posted job vacancies
    count = 'a'
    jd_id = f'{request.user.id}_{count}'
    current_job_lists = JobDescription.objects.filter(username=request.user)
    if not current_job_lists:
        return redirect('/create_jobdescription')
    else:   
        return redirect(f'/update_jobdescription/{jd_id}/')
    #current_job_lists = JobDescription.objects.filter(username=request.user)
    #return render(request, 'employer.html', {"current_job_lists": current_job_lists})


def create_jobdescription(request):     
    count = 'a'
    current_jd_id = f'{request.user.id}_{count}'

    current_job_lists = JobDescription.objects.filter(username=request.user)    

    if request.method == 'POST':        
        jdform = JobDescriptionForm(request.POST, request.FILES)
        if jdform.is_valid():            
            jdform.save()            
            return redirect(f'/update_jobdescription/{current_jd_id}/')            
        
    else:        
        jdform = JobDescriptionForm(initial={
            'username': request.user, 
            'email': request.user.email,
            'jd_id': current_jd_id
            })
    
    CVQuery_set = JobPost.objects.all()
    return render(request, 'employer.html', {"jdform": jdform, "current_jd_id": current_jd_id, "CVQuery_set": CVQuery_set, "current_job_lists": current_job_lists })


def create_jobdescription_another(request, jd_id):   
    count = jd_id[-1]
    alpha = chr(ord(count) + 1)       
    current_jd_id = f'{request.user.id}_{alpha}'

    current_job_lists = JobDescription.objects.filter(username=request.user)
    
    if request.method == 'POST':        
        jdform = JobDescriptionForm(request.POST, request.FILES)
        if jdform.is_valid():            
            jdform.save()            
            return redirect(f'/update_jobdescription_another/{current_jd_id}/')

    else:                
        jdform = JobDescriptionForm(initial={
            'username': request.user, 
            'email': request.user.email,
            'jd_id': current_jd_id              
            })
            
    CVQuery_set = JobPost.objects.all()
    return render(request, 'employer.html', {"jdform": jdform, "current_jd_id": current_jd_id, "CVQuery_set": CVQuery_set, "current_job_lists": current_job_lists })


#extract jd_id
def update_jobdescription(request, jd_id):  

    current_job_lists = JobDescription.objects.filter(username=request.user)

    current_jd_id = jd_id    
    if request.method == "GET":
        if id == 0:
            jdposts = JobDescriptionForm()
        else:                        
            jd = JobDescription.objects.get(
                username=request.user, 
                email=request.user.email,
                jd_id=current_jd_id
                )
            
            jdposts = JobDescriptionForm(instance=jd)
        
        CVQuery_set = JobPost.objects.all()
        return render(request, 'employer.html', {'jdposts': jdposts, "current_jd_id": current_jd_id, "CVQuery_set": CVQuery_set, "current_job_lists": current_job_lists })    
    
    else:
        if id == 0:
            jdposts = JobDescriptionForm(request.POST, request.FILES)  #prev: post
        else:
            jd = JobDescription.objects.get(
                username=request.user, 
                email=request.user.email,
                jd_id=current_jd_id
                )
            jdposts = JobDescriptionForm(request.POST, request.FILES, instance=jd)

        if jdposts.is_valid():            
            update = jdposts.save(commit=False)
            update.jobdescription = request.user.employer   #related_name
            update.save()            
            return redirect(f'/update_jobdescription/{current_jd_id}/')



def update_jobdescription_another(request, jd_id):    

    current_job_lists = JobDescription.objects.filter(username=request.user)

    current_jd_id = jd_id     
    
    if request.method == "GET":
        if id == 0:
            jdposts = JobDescriptionForm()
        else:
            jd = JobDescription.objects.get(
                username=request.user, 
                email=request.user.email,
                jd_id=current_jd_id
                )            
            jdposts = JobDescriptionForm(instance=jd)
        
        CVQuery_set = JobPost.objects.all()
        return render(request, 'employer.html', {'jdposts': jdposts, "current_jd_id": current_jd_id, "CVQuery_set": CVQuery_set, "current_job_lists": current_job_lists })    
    
    else:
        if id == 0:
            jdposts = JobDescriptionForm(request.POST, request.FILES)  #prev: post
        else:
            jd = JobDescription.objects.get(
                username=request.user, 
                email=request.user.email,
                jd_id=current_jd_id
                )
            jdposts = JobDescriptionForm(request.POST, request.FILES, instance=jd)

        if jdposts.is_valid():            
            update = jdposts.save(commit=False)
            update.jobdescription = request.user.employer   #related_name
            update.save()            
            return redirect(f'/update_jobdescription_another/{current_jd_id}/')


# Match CVs to JDs here
def matched_results(request):
    #retrieve skills of current user
    current_user_cv = JobPost.objects.get(username=request.user)
    
    cur_skills = current_user_cv.curricular_skills
    noncur_skills = current_user_cv.noncurricular_skills

    #cv_profile = f"{cur_skills} {noncur_skills}"
    cv_profile_list = cur_skills + noncur_skills
    cv_profile_set = set(map(str.lower, cv_profile_list)) 
    
    #retrieve ALL JDs
    job_desc = JobDescription.objects.all()
    jd_contents = [f"{jd.qualifications} {jd.job_requirements}" for jd in job_desc]
 
    #encode CV and all JDs
    cv_embeddings = model.encode(cv_profile_list, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_contents, convert_to_tensor=True)
    
    #compare similarities
    sim = util.pytorch_cos_sim(cv_embeddings, jd_embeddings)[0]

    similarities = (sim + 1) / 2  # normalized similarities

    #KB Matching
    def match_jd_cv(jd, current_user_cv, cv_profile_set):

        jd_quali = jd.qualifications
        jd_reqt = jd.job_requirements

        jd_list = jd_quali + jd_reqt
        jd_set = set(map(str.lower, jd_list)) 

        skill_match = len(jd_set & cv_profile_set) / len(jd_set) if jd_set else 0

        #Fuzzy Matching
        jd_text = f"{jd.qualifications} {jd.job_requirements}".lower()
        cv_text = " ".join(cv_profile_list).lower()
        fuzzy_match_score = fuzz.partial_ratio(jd_text, cv_text) / 100

        total_score = (0.8 * skill_match) + (0.2 * fuzzy_match_score)

        return total_score


    #prepare result
    results = []
    for index, (jd, similarity) in enumerate(zip(job_desc, similarities)):
        results.append({
            'index': index + 1,
            'similarity': round(similarity.item() * 100, 2),
            'similarity_kb': round(match_jd_cv(jd, current_user_cv, cv_profile_set) * 100, 2),
            'title': jd.title,
            'company_name': jd.company_name,                
            'location': jd.location,
            'term': jd.term,
            'email': jd.email,
            'category': jd.category,
            'contact_person': jd.contact_person,
            'contact_number': jd.contact_number,            
            'department': jd.department,
            'qualifications': jd.qualifications,
            'job_requirements': jd.job_requirements,
        })

    #sort results by similarity (highest first)
    sorted_results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    
    return render(request, 'matched_jd_cv.html', {"results": sorted_results })
    

# Match a JD with CVs here using CBF
def matched_interns_results(request, jd_id):
    #retrieve qualifications posted by current user
    current_user_jd = JobDescription.objects.get(username=request.user, jd_id = jd_id)
    
    qualifications = current_user_jd.qualifications
    requirements = current_user_jd.job_requirements

    #jd_profile = f"{qualifications} {requirements}".lower().split()
    jd_profile_list = qualifications + requirements    
    jd_profile_set = set(map(str.lower, jd_profile_list))
    
    #retrieve ALL JDs
    cur_vit = JobPost.objects.all()
    cv_contents = [f"{cv.curricular_skills} {cv.noncurricular_skills}" for cv in cur_vit]
 
    #encode CV and all JDs
    jd_embeddings = model.encode(cv_contents, convert_to_tensor=True)
    cv_embeddings = model.encode(jd_profile_list, convert_to_tensor=True)
    
    #compare similarities
    sim = util.pytorch_cos_sim(cv_embeddings, jd_embeddings)[0]

    similarities = (sim + 1) / 2  # normalized cosine similarities


    #KB Matching
    def match_cv_jd(cv, current_user_jd, jd_profile_set):
        
        cv_curricular = cv.curricular_skills
        cv_noncur = cv.noncurricular_skills

        cv_list = cv_curricular + cv_noncur
        cv_set = set(map(str.lower, cv_list))

        skill_match = len(cv_set & jd_profile_set) / len(cv_set) if cv_set else 0

        #Fuzzy Matching
        cv_text = f"{cv.curricular_skills} {cv.noncurricular_skills}".lower()
        jd_text = " ".join(jd_profile_list).lower()
        fuzzy_match_score = fuzz.partial_ratio(cv_text, jd_text) / 100

        total_score = (0.5 * skill_match) + (0.5 * fuzzy_match_score)

        return total_score


    #prepare result
    results = []
    for index, (cv, similarity) in enumerate(zip(cur_vit, similarities)):
        results.append({
            'index': index + 1,
            'similarity': round(similarity.item()*100,3),               # based on Cosine Similarity
            'similarity_kb': round(match_cv_jd(cv, current_user_jd, jd_profile_set) * 100, 2),    # knowledge-based score
            'applicant_name': f"{cv.first_name} {cv.last_name}",
            'applicant_contact_number': cv.applicant_contact_number,
            'email': cv.email,                
            'degree': cv.degree,
            'curricular_skills': cv.curricular_skills,
            'noncurricular_skills': cv.noncurricular_skills,            
        })
    #sort results by similarity (highest first)
    sorted_results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    
    return render(request, 'matched_cv2jd.html', {"results": sorted_results, "current_jd_id": jd_id })
