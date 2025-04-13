import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadResultsForm
from .models import Student, Subject, Result, Semester
from django.contrib import messages
import random
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
import weasyprint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import random
import string


def index(request):
    semesters = Semester.objects.order_by('-id')  # List of all uploaded semesters
    return render(request, 'index.html', {'semesters': semesters})

@login_required
def upload_results(request):
    if request.method == 'POST':
        form = UploadResultsForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            regulation = form.cleaned_data['regulation']
            branch = form.cleaned_data['branch']
            # dob = form.cleaned_data['dob']

            try:
                df = pd.read_excel(excel_file)

                for _, row in df.iterrows():
                    roll_number = str(row['Htno']).strip()
                    semester_name = str(row['Semester']).strip()
                    sub_code = str(row['Subcode']).strip()
                    sub_name = str(row['Subname']).strip()
                    internal_marks = float(row['Internalmarks'])
                    grade = str(row['Grade']).strip()
                    credits = float(row['Credits'])

                    semester, _ = Semester.objects.get_or_create(name=semester_name, regulation=regulation)
                    student, _ = Student.objects.get_or_create(
                        roll_number=roll_number,
                        defaults={'branch': branch}
                    )
                    subject, _ = Subject.objects.get_or_create(
                        code=sub_code,
                        name=sub_name,
                        semester=semester
                    )
                    Result.objects.update_or_create(
                        student=student,
                        subject=subject,
                        semester=semester,
                        defaults={'grade': grade, 'credits': credits, 'internal_marks': internal_marks}
                    )

                messages.success(request, "All results uploaded successfully.")
            except Exception as e:
                messages.error(request, f"Error: {e}")
            return redirect('upload_results')
    else:
        form = UploadResultsForm()

    return render(request, 'upload.html', {'form': form})



from .forms import CheckResultForm

def check_result(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    error = None
    student = None
    results = []
    total_credits = 0

    if request.method == 'POST':
        form = CheckResultForm(request.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number']
            try:
                student = Student.objects.get(roll_number=roll_number)
                results = Result.objects.filter(student=student, semester=semester)
                total_credits = sum(r.credits for r in results)
            except Student.DoesNotExist:
                error = "Student not found."
        else:
            error = "Invalid captcha or input."
    else:
        form = CheckResultForm()

    return render(request, 'check_result.html', {
        'semester': semester,
        'form': form,
        'student': student,
        'results': results,
        'total_credits': total_credits,
        'error': error,
    })




def download_pdf(request, roll_number, semester_id):
    from .models import Student, Semester, Result

    student = get_object_or_404(Student, roll_number=roll_number)
    semester = get_object_or_404(Semester, id=semester_id)
    results = Result.objects.filter(student=student, semester=semester)

    html = render_to_string("pdf_template.html", {
        "student": student,
        "semester": semester,
        "results": results
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{roll_number}_{semester.name}.pdf"'
    weasyprint.HTML(string=html).write_pdf(response)

    return response


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def refresh_captcha(request):
    new_captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    request.session['captcha'] = new_captcha
    return JsonResponse({'captcha': new_captcha})