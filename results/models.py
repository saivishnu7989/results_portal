from django.db import models

# Create your models here.

# ------------------------
# 1. Semester Model
# ------------------------
class Semester(models.Model):
    name = models.CharField(max_length=50)  # Ex: III B.Tech I Sem
    regulation = models.CharField(max_length=10)  # Ex: R16, R19, R20

    def __str__(self):
        return f"{self.name} ({self.regulation})"


# ------------------------
# 2. Student Model
# ------------------------
class Student(models.Model):
    roll_number = models.CharField(max_length=15, unique=True)
    branch = models.CharField(max_length=100)

    def __str__(self):
        return self.roll_number


# ------------------------
# 3. Subject Model
# ------------------------
class Subject(models.Model):
    code = models.CharField(max_length=20)  # R203104K
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.name}"


# ------------------------
# 4. Result Model
# ------------------------
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    internal_marks = models.IntegerField(default=0)  # 👈 ADD THIS
    grade = models.CharField(max_length=10)
    credits = models.FloatField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code} - {self.grade}"


class ResultExcelUpload(models.Model):
    file = models.FileField(upload_to="excel_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Uploaded on {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"


