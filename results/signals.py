import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ResultExcelUpload, Student, Subject, Result, Semester

@receiver(post_save, sender=ResultExcelUpload)
def process_excel(sender, instance, created, **kwargs):
    if created:
        df = pd.read_excel(instance.file.path)

        for _, row in df.iterrows():
            roll = row["Htno"]
            # dob = "2000-01-01"  # or get from somewhere if available
            branch = "CSE"       # or deduce from roll if you want

            semester_name = row["Semester"]
            semester, _ = Semester.objects.get_or_create(name=semester_name, regulation="R20")

            student, _ = Student.objects.get_or_create(
                roll_number=roll,
                defaults={"branch": branch}
            )

            subject, _ = Subject.objects.get_or_create(
                code=row["Subcode"],
                name=row["Subname"],
                semester=semester
            )

            Result.objects.create(
                student=student,
                subject=subject,
                grade=row["Grade"],
                credits=row["Credits"],
                semester=semester
            )
