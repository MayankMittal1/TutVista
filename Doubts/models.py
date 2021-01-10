from django import forms
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.forms import widgets
from django.forms.fields import CharField

# Create your models here.
def upload_image(instance, filename):
    return "%s/%s" % (instance.question_id, filename)

def upload_file(instance, filename):
    return "%s/%s" % (instance.question_id, filename)

dept_choice=(('Physics','Physics'),('Chemistry','Chemistry'),('Maths','Maths'))
class Student(models.Model):
    username=models.CharField(primary_key=True, max_length=20, unique=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    phone=models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    image=models.ImageField(upload_to='student_profile/',null=True, blank=True, default='profile.png')

    class Meta:
        db_table = 'Doubts_Student'

class Teacher(models.Model):
    username=models.CharField(primary_key=True, max_length=20, unique=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    phone=models.CharField(max_length=10, null=True, blank=True)
    department = models.CharField(max_length=20,null=True,choices=dept_choice,default='physics')
    assigned=models.CharField(null=True,max_length=500, default=",")
    assigned_count=models.IntegerField(default=0)
    image=models.ImageField(upload_to='teacher_profile/',null=True, blank=True,default='profile.png')
    class Meta:
        db_table = 'Doubts_Teacher'

class Question(models.Model):
     id= models.IntegerField(primary_key=True, unique=True, default=1)
     user_id=models.ForeignKey(Student, on_delete=CASCADE)
     question_text=models.TextField()
     question_dept=models.CharField(max_length=20,null=True, choices=dept_choice, default="physics")
     question_image=models.ImageField(upload_to='questions/',blank=True, default='white.jpg')
     ans_id=models.CharField(max_length=20)
     assigned_teacher=models.CharField(max_length=20,null=True)
     time=models.DateTimeField(auto_now=True)
     answered=models.IntegerField(default=0)
     class Meta:
        db_table = 'Doubts_Question'

class Answer(models.Model):
    question_id= models.CharField(max_length=20, null=True)
    id=models.IntegerField(primary_key=True, unique=True, default=1)
    answer_text=models.TextField()
    answer_image=models.ImageField(upload_to='answers/', blank=True, null=True, default='white.jpg')
    comment=models.TextField(max_length=100000,null=True, blank=True)
    time=models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Doubts_Answer'

class get_info(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    comment=models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        db_table = 'Doubts_get_info'