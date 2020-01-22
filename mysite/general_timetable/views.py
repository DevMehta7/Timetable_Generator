from django.shortcuts import render
from django.http import HttpResponse
from .models import SubjectMaster, FacultyMaster
# Create your views here.


def home(request):
    qsub = SubjectMaster.objects.all()
    qfac = FacultyMaster.objects.all()
    jay_sub = SubjectMaster.objects.filter(faculties__name__contains='Jay Shah')
    ajava_fac = FacultyMaster.objects.filter(subject__name__contains='Advance Java')
    context={
        "obj_list_sub": qsub,
        "obj_list_fac": qfac,
        "jay_sub" : jay_sub,
        "ajava" : ajava_fac
    }
    return render(request, "home.html", context)
