from faker import Faker
from .models import *
import random
from django.db.models import Sum

fake = Faker()

def seed_db(n=10) -> None:
    try:
        for i in range(0,n):
            categoriesList = Category.objects.all()
            category_name = fake.name()
            user = User.objects.get(id=1)
            name = fake.name()
            age = random.randint(1,110)
            dob = fake.date()
            email = fake.email()
            mobile = '0000000000'
            anniversary = fake.date()

            category_obj = Category.objects.create(category_name=category_name)

            phone_obj = PhoneBook.objects.create(
                user = user,
                name = name,
                age = age,
                dob = dob,
                email = email,
                mobile = mobile,
                category = category_obj,
                anniversary = anniversary
            )
    except Exception as e:
        print(e)


def seeddb(n=10) -> None:
    try:
        for i in range(0,n):
            department_objs = Department.objects.all()
            random_index = random.randint(0,(len(department_objs)-1))
            student_id = f'STU-0{i}'
            department = department_objs[random_index]
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20,35)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id = student_id)

            student_obj = Student.objects.create(
                department = department,
                student_id = student_id_obj,
                student_name = student_name,
                student_email = student_email,
                student_age = student_age,
                student_address = student_address
            )
    except Exception as e:
        print(e)


def create_stu_marks():
    try:
        student_objs = Student.objects.all()

        for student in student_objs:
            subjects = Subject.objects.all()
            for subject in subjects:
                stu_marks = SubjectMarks.objects.create(
                    student = student,
                    subject = subject,
                    marks = random.randint(0,100)
                )

    except Exception as e:
        print(e)


def generate_reprt_card():
    ranks = Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-student_age')
    i = 1
    for rank in ranks:
        ReportCard.objects.create(
            student=rank,
            rank = i)
        i+=1
