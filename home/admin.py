from django.contrib import admin
from .models import *
from django.db.models import Sum

# Register your models here.
admin.site.register(Category)
class phonebooks(admin.ModelAdmin):
    list_display = ['name','age','mobile','dob','email','anniversary']
admin.site.register(PhoneBook,phonebooks)

admin.site.register(Department)
admin.site.register(StudentID)

class studentsAdmin(admin.ModelAdmin):
    list_display = ['student_id','student_name','student_age','student_email','student_address']
admin.site.register(Student, studentsAdmin)

admin.site.register(Subject)

class subjectMarksAdmin(admin.ModelAdmin):
    list_display = ['student','subject','marks']
admin.site.register(SubjectMarks, subjectMarksAdmin)


class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student','total_marks','rank','date_of_report_card_generation']
    ordering = ['-rank']
    def total_marks(self, obj):
        subject_marks = SubjectMarks.objects.filter(student=obj.student)
        marks = subject_marks.aggregate(marks = Sum('marks'))
        return marks['marks']
admin.site.register(ReportCard, ReportCardAdmin)