from django.db import models
from django.contrib.auth.models import User

# Create your models here. ORM

# For student profile, supposedly AccountProfile
class JobPost(models.Model):
    #author = models.ForeignKey(UserD, on_delete=models.CASCADE)       # if this post is deleted, the user will be deleted as well
    username = models.OneToOneField(User, on_delete=models.DO_NOTHING, default='0', related_name='intern')   #null=True
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    applicant_contact_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    GPA = models.FloatField()
    curricular_skills = models.TextField(max_length=3000)
    noncurricular_skills = models.TextField(max_length=3000)
    biography = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add = True)  
    file_upload_CV = models.FileField(upload_to='uploads_CV/%y/%m/%d/', null=True, default="NULL")

    def __str__(self):
        return self.curricular_skills


# For employer profile
class JobDescription(models.Model):
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='employer')    
    jd_id = models.CharField(max_length=20, unique=True, blank=True)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    term = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=3000)
    job_requirements = models.CharField(max_length=3000)
    file_upload = models.FileField(upload_to='uploads_JD/%y/%m/%d/', null=True, default="NULL")

    def __str__(self):
        return self.qualifications + self.job_requirements
    
    def save(self, *args, **kwargs):
        if not self.jd_id:
            self.jd_id = f"jd{self.id if self.id else ''}"
            super(JobDescription, self).save(*args, **kwargs)
        super(JobDescription, self).save(*args, **kwargs)
  