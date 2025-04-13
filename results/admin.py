from django.contrib import admin

# Register your models here.
from .models import Student, Subject, Semester, Result

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Semester)
admin.site.register(Result)
