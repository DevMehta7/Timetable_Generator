from django.shortcuts import render
# from django.http import HttpResponse
from .models import SubjectMaster, FacultyMaster, ShiftMaster, LabMaster, DivisionMaster, BatchMaster
import random
# Create your views here.


def home(request):
    qsub = SubjectMaster.objects.all()
    qfac = FacultyMaster.objects.all()
    jay_sub = SubjectMaster.objects.filter(faculties__name__contains='Jay Shah')
    ajava_fac = FacultyMaster.objects.filter(subject__name__contains='Advance Java')
    shift_1 = ShiftMaster.objects.filter(shift_no="1")
    # unall_ajava = FacultyMaster.objects.filter(subject__name__contains='Advance Java', allocated=True)
    # for i in unall_ajava:
    #     # i.allocated = False
    #     # i.save()
    context = {
        "obj_list_sub": qsub,
        "obj_list_fac": qfac,
        "jay_sub": jay_sub,
        "ajava": ajava_fac,
        "shift_1": shift_1,
        # "unall_ajava" : unall_ajava
    }
    return render(request, "home.html", context)


def main(request):

    def lecture(div_func):
        print(div_func)
        return

    def lab(div_func):
        batches = BatchMaster.objects.filter(div=div_func)
        for batch in batches:
            avail_lab = LabMaster.objects.filter(allocated=False)  # available lab
            if avail_lab.exists():
                lab_r = random.choice(avail_lab)
                print("Lab: " + str(lab_r))
                lab_r.allocated = True
                lab_r.save()
            else:
                lecture(div_func)

            print(batch)
            while True:
                sub_r = random.choice(SubjectMaster.objects.filter(sem=div_func.sem))  # Random subjects..

                avail_fac = FacultyMaster.objects.filter(subject__name__contains=sub_r.name, allocated=False)
                if avail_fac.exists():
                    fac_r = random.choice(avail_fac)  # Random Faculties..
                    print("Faculty: " + str(fac_r))
                    print("Sub: " + str(sub_r))
                    fac_r.allocated = True  # lock faculty for a slot..
                    fac_r.save()
                    break
        return

    # start from HERE ........................................................

    all_div = DivisionMaster.objects.all()
    for div_loop in all_div:
        print(div_loop)
        # lab or lec to start with...0=lab & 1=lec
        laborlec = random.randint(0, 1)
        print(laborlec)
        if laborlec == 0:
            lab(div_loop)
        else:
            lecture(div_loop)

    fac_l = FacultyMaster.objects.all()
    for i in fac_l:
        i.allocated = False  # Free allocated faculties ..
        i.save()

    lab_l = LabMaster.objects.all()
    for i in lab_l:
        i.allocated = False  # Free allocated labs..
        i.save()

    context = {}
    return render(request, "main.html", context)
