from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model

#User = get_user_model()

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class PhoneBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    anniversary = models.DateField(blank=True, null=True)
    status = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name 


class Department(models.Model):
    department_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.department_name
    
    class Meta:
        ordering = ['department_name']        


class StudentID(models.Model):
    student_id = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.student_id

class StudentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Student(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="depart")
    student_id = models.OneToOneField(StudentID, on_delete=models.CASCADE, related_name="studentid")
    student_name = models.CharField(max_length=255)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()
    is_deleted = models.BooleanField(default=False)

    objects = StudentsManager()
    admin_objects = models.Manager()

    def __str__(self) -> str:
        return self.student_name
    
    class Meta:
        ordering = ['student_name']
        verbose_name = "student"

class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.subject_name

class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studentmarks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.student.student_name} {self.subject.subject_name}'

    class Meta:
        unique_together = ['student','subject']
    
class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studentreportcard")
    rank = models.IntegerField(default=-1)
    date_of_report_card_generation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['rank','date_of_report_card_generation']