from django.shortcuts import render
from django.http import JsonResponse
# from django.http import HttpResponse
from .models import SubjectMaster, FacultyMaster, Classroom, ShiftMaster, LabMaster, DivisionMaster, BatchMaster, \
    DayMaster, TimetableMaster
import random
from datetime import datetime, time, date, timedelta


# Create your views here.

def test_ajax(request):
    return JsonResponse({
        'hello': 'hello'
    }, status=200)


def home_page(request):
    return render(request, "home-page.html", {})


def generate_time_table_api(request):
    def lecture(div_func, day, slt_time, inc):
        var_tt = TimetableMaster()
        avail_cls = Classroom.objects.filter(allocated=False)  # available class
        if avail_cls.exists():
            cls_r = random.choice(avail_cls)
            print("Class: " + str(cls_r))
            var_tt.classroom = cls_r
            cls_r.allocated = True
            
        else:
            print("class not available")
            # return
            lab(div_func, day, slt_time, inc)

        while True:
            sub = SubjectMaster.objects.filter(sem=div_func.sem, lec_rm__gte= '0')
            if sub.exists():
                sub_r = random.choice(sub)  # Random subjects..
            
                avail_fac = FacultyMaster.objects.filter(subject__name__contains=sub_r.name, allocated='0')
                if avail_fac.exists():
                    fac_r = random.choice(avail_fac)  # Random Faculties..
                    print("Faculty: " + str(fac_r))
                    print("Sub: " + str(sub_r))
                    var_tt.faculty = fac_r
                    var_tt.subject = sub_r
                    fac_r.allocated = '1'  # lock faculty for a slot..
                    sub_r.lec_rm -= 1
                    sub_r.save()
                    cls_r.save()
                    fac_r.save()
                    break
        var_tt.day = day
        var_tt.slt_start = slt_time
        var_tt.slt_end = inc
        var_tt.div = div_loop
        var_tt.laborlec = True
        var_tt.save()
        return

    def lab(div_func, day, slt_time, inc):

        batches = BatchMaster.objects.filter(div=div_func)
        ttl_btch = BatchMaster.objects.filter(div=div_func).count()  # total batches count in div...
        unalloc_lab = LabMaster.objects.filter(allocated='0').count()

        if unalloc_lab >= ttl_btch:  # compare unallocated labs with total batches in div...

            for batch in batches:
                var_tt = TimetableMaster()
                avail_lab = LabMaster.objects.filter(allocated='0')  # available lab...
                # available lab count...
                lab_r = random.choice(avail_lab)
                print("Lab: " + str(lab_r))
                lab_r.allocated = '2'
                

                print(batch)
                #     while True:
                #         sub_r = random.choice(SubjectMaster.objects.filter(sem=div_func.sem))  # Random subjects..
                #
                #         avail_fac = FacultyMaster.objects.filter(subject__name__contains=sub_r.name, allocated=False)
                #         if avail_fac.exists():
                #             fac_r = random.choice(avail_fac)  # Random Faculties..
                #             print("Faculty: " + str(fac_r))
                #             print("Sub: " + str(sub_r))
                #             fac_r.allocated = True  # lock faculty for a slot..
                #             fac_r.save()
                #             break
                while True:
                    sub = SubjectMaster.objects.filter(sem=div_func.sem, lab_rm__gte= '0')
                    if sub.exists():
                        sub_r = random.choice(sub)
                
                        # for sub_r in SubjectMaster.objects.filter(sem=div_func.sem):
                        avail_fac = FacultyMaster.objects.filter(subject__name__contains=sub_r.name, allocated='0')
                        if avail_fac.exists():
                            fac_r = random.choice(avail_fac)  # Random Faculties..
                            print("Faculty: " + str(fac_r))
                            print("Sub: " + str(sub_r))
                            var_tt.subject = sub_r
                            var_tt.faculty = fac_r
                            fac_r.allocated = '2'  # lock faculty for a slot..
                            sub_r.lab_rm -= 2
                            sub_r.save()
                            fac_r.save()
                            lab_r.save()
                            break
                    else:
                        # inc = (datetime.combine(date(1, 1, 1), div_loop.curr_slot) - timedelta(hours=1)).time()
                        lecture(div_loop, day, slt_time, inc)
                var_tt.day = day
                var_tt.slt_start = slt_time
                var_tt.slt_end = inc
                var_tt.div = div_loop
                var_tt.laborlec = False
                var_tt.batch = batch
                var_tt.lab = lab_r
                var_tt.save()

        else:
            # inc = (datetime.combine(date(1, 1, 1), div_loop.curr_slot) - timedelta(hours=1)).time()
            lecture(div_func, day, slt_time, inc)
        return

    # start from HERE ........................................................
    TimetableMaster.objects.all().delete()

    shift_1 = ShiftMaster.objects.get(shift_no='1')
    slt_time = shift_1.from_time
    days = DayMaster.objects.all()
    all_div = DivisionMaster.objects.all()
    sub_l = SubjectMaster.objects.all()
    for i in sub_l:
        i.lab_rm = i.max_lab + 2
        i.lec_rm = i.max_lec + 2
        i.save()
        # i.lab_rm = getattr(i, max_lab)
        # i.lec_rm = getattr(i, max_lec)
            
    # flag_4_true = 0
    for day in days:
        # free every resources.....................
        fac_l = FacultyMaster.objects.all()
        for i in fac_l:
            i.allocated = '0'  # Free allocated faculties ..
            i.save()

        lab_l = LabMaster.objects.all()
        for i in lab_l:
            i.allocated = '0'  # Free allocated labs..
            i.save()

        class_l = Classroom.objects.all()
        for i in class_l:
            i.allocated = False  # Free allocated labs..
            i.save()

        div_l = DivisionMaster.objects.all()
        for i in div_l:
            i.curr_slot = time(9, 30, 00)  # Free allocated labs..
            i.save()

        
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  {} @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@".format(day))
        slt_time = shift_1.from_time
        # print(slt_time)
        while slt_time < shift_1.to_time:
            # var_tt = TimetableMaster()

            break_end = shift_1.break_to_time

            all_div = DivisionMaster.objects.all()  # repeating to check whether it solve the error or not...*****WORKS
            for div_loop in all_div:
                # print(slt_time)  # problem finder not necessary

                if div_loop.curr_slot == shift_1.break_from_time:
                    div_loop.curr_slot = break_end

                # lab or lec to start with...0=lab & 1=lec

                laborlec = random.randint(1, 10)
                if div_loop.curr_slot == slt_time:

                    if laborlec >= 7:
                        inc = (datetime.combine(date(1, 1, 1), div_loop.curr_slot) + timedelta(hours=2)).time()
                        # if inc <= shift_1.to_time and (div_loop.curr_slot <= shift_1.break_from_time or break_end <= inc):
                        if inc <= shift_1.to_time:
                            if break_end <= inc and div_loop.curr_slot < break_end:
                                inc = (datetime.combine(date(1, 1, 1), inc) + timedelta(hours=0.5)).time()
                            print(div_loop)
                            print("lab is selected")
                            print("{} : {}".format(div_loop.curr_slot, inc))
                            # saving to tt master

                            lab(div_loop, day, slt_time, inc)

                            div_loop.curr_slot = inc
                            div_loop.save()
                        else:
                            inc = (datetime.combine(date(1, 1, 1), div_loop.curr_slot) - timedelta(hours=2)).time()
                            laborlec = 1

                    if laborlec < 7:
                        
                        inc = (datetime.combine(date(1, 1, 1), div_loop.curr_slot) + timedelta(hours=1)).time()
                        if inc <= shift_1.to_time:
                            print(div_loop)
                            print("lecture is selected")
                            print("{} : {}".format(div_loop.curr_slot, inc))

                            lecture(div_loop, day, slt_time, inc)

                            div_loop.curr_slot = inc
                            div_loop.save()

                    # free allocated resources after single slot................
                    fac_l = FacultyMaster.objects.all()
                    for i in fac_l:

                        if i.allocated == 2:
                            i.allocated = 1  # Free allocated faculties ..
                            i.save()
                        elif i.allocated == 1:
                            i.allocated = 0  # Free allocated faculties ..
                            i.save()

                    lab_l = LabMaster.objects.all()
                    for i in lab_l:
                        if i.allocated == '2':
                            i.allocated = '1'  # Free allocated labs ..
                            i.save()
                        elif i.allocated == '1':
                            i.allocated = '0'  # Free allocated faculties ..
                            i.save()

                    class_l = Classroom.objects.all()
                    for i in class_l:
                        i.allocated = False  # Free allocated labs..
                        i.save()

            if slt_time == shift_1.break_from_time:
                print("*****************break start : {}**************".format(slt_time))
                slt_time = break_end
                print("*****************break ends : {}**************".format(slt_time))
            else:
                slt_time = (datetime.combine(date(1, 1, 1), slt_time) + timedelta(hours=1)).time()

    return JsonResponse({
        'msg': 'created'
    }, status=200)


def generate_time_table_page(request):
    return render(request, "generate-time-table-page.html", {})


def view_time_table_page(request):
    div_no = request.GET.get('div_no')
    div_check = False
    # tt = TimetableMaster.objects.all()
    tt = TimetableMaster.objects.filter(div__div_no=div_no)
    divs = DivisionMaster.objects.all()

    if div_no and tt.exists():
        div_check = True

    tt_sorted_by_days = {}
    days = DayMaster.objects.all()
    for day in days:
        tt_sorted_by_days[day.day] = tt.filter(day=day)

    context = {
        "div_check": div_check,
        "divs": divs,
        "div_no": div_no,
        "tt_sorted_by_days": tt_sorted_by_days
    }
    return render(request, "view-time-table-page.html", context)


def home(request):
    qsub = SubjectMaster.objects.all()
    qfac = FacultyMaster.objects.all()
    jay_sub = SubjectMaster.objects.filter(faculties__name__contains='Jay Shah')
    ajava_fac = FacultyMaster.objects.filter(subject__name__contains='Advance Java')
    shift_1 = ShiftMaster.objects.filter(shift_no="1")
    unalloc_fac = FacultyMaster.objects.filter(allocated=False)
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
        "unalloc_fac": unalloc_fac,
        # "unall_ajava" : unall_ajava
    }
    return render(request, "home.html", context)


# def main(request):
#     def lecture(div_func, day, slt_time, inc):
#         var_tt = TimetableMaster()
#         avail_cls = Classroom.objects.filter(allocated=False)  # available class
#         if avail_cls.exists():
#             cls_r = random.choice(avail_cls)
#             print("Class: " + str(cls_r))
#             var_tt.classroom = cls_r
#             cls_r.allocated = True
#             cls_r.save()
#         else:
#             print("class not available")
#             lab(div_func, day, slt_time, inc)

#         while True:
#             sub_r = random.choice(SubjectMaster.objects.filter(sem=div_func.sem))  # Random subjects..

#             avail_fac = FacultyMaster.objects.filter(subject__name__contains=sub_r.name, allocated='0')
#             if avail_fac.exists():
#                 fac_r = random.choice(avail_fac)  # Random Faculties..
#                 print("Faculty: " + str(fac_r))
#                 print("Sub: " + str(sub_r))
#                 var_tt.faculty = fac_r
#                 var_tt.subject = sub_r
#                 fac_r.allocated = '1'  # lock faculty for a slot..
#                 fac_r.save()
#                 break
#         var_tt.day = day
#         var_tt.slt_start = slt_time
#         var_tt.slt_end = inc
#         var_tt.div = div_loop
#         var_tt.laborlec = True
#         var_tt.save()
#         return

#     def lab(div_func, day, slt_time, inc):

#         batches = BatchMaster.objects.filter(div=div_func)
#         ttl_btch = BatchMaster.objects.filter(div=div_func).count()  # total batches count in div...
#         unalloc_lab = LabMaster.objects.filter(allocated='0').count()

#         if unalloc_lab >= ttl_btch:  # compare unallocated labs with total batches in div...

#             for batch in batches:
#                 var_tt = TimetableMaster()
#                 avail_lab = LabMaster.objects.filter(allocated='0')  # available lab...
#                 # available lab count...
#                 lab_r = random.choice(avail_lab)
#                 print("Lab: " + str(lab_r))
#                 lab_r.allocated = '2'
#                 lab_r.save()

#                 print(batch)
#                 #     while True:
#                 #         sub_r = random.choice(SubjectMaster.objects.filter(sem=div_func.sem))  # Random subjects..
#                 #
#                 #         avail_fac = FacultyMaster.objects.filter(subject__name__contains=sub_r.name, allocated=False)
#                 #         if avail_fac.exists():
#                 #             fac_r = random.choice(avail_fac)  # Random Faculties..
#                 #             print("Faculty: " + str(fac_r))
#                 #             print("Sub: " + str(sub_r))
#                 #             fac_r.allocated = True  # lock faculty for a slot..
#                 #             fac_r.save()
#                 #             break

#                 for sub_r in SubjectMaster.objects.filter(sem=div_func.sem):
#                     avail_fac = FacultyMaster.objects.filter(subject__name__contains=sub_r.name, allocated='0')
#                     if avail_fac.exists():
#                         fac_r = random.choice(avail_fac)  # Random Faculties..
#                         print("Faculty: " + str(fac_r))
#                         print("Sub: " + str(sub_r))
#                         var_tt.subject = sub_r
#                         var_tt.faculty = fac_r
#                         fac_r.allocated = '2'  # lock faculty for a slot..
#                         fac_r.save()
#                         break
#                 var_tt.day = day
#                 var_tt.slt_start = slt_time
#                 var_tt.slt_end = inc
#                 var_tt.div = div_loop
#                 var_tt.laborlec = False
#                 var_tt.batch = batch
#                 var_tt.lab = lab_r
#                 var_tt.save()

#         else:
#             lecture(div_func, day, slt_time, inc)
#         return

#     # start from HERE ........................................................
#     shift_1 = ShiftMaster.objects.get(shift_no='1')
#     slt_time = shift_1.from_time
#     days = DayMaster.objects.all()
#     all_div = DivisionMaster.objects.all()
#     # flag_4_true = 0
#     for day in days:
#         # free every resources.....................
#         fac_l = FacultyMaster.objects.all()
#         for i in fac_l:
#             i.allocated = '0'  # Free allocated faculties ..
#             i.save()

#         lab_l = LabMaster.objects.all()
#         for i in lab_l:
#             i.allocated = '0'  # Free allocated labs..
#             i.save()

#         class_l = Classroom.objects.all()
#         for i in class_l:
#             i.allocated = False  # Free allocated labs..
#             i.save()

#         div_l = DivisionMaster.objects.all()
#         for i in div_l:
#             i.curr_slot = time(9, 30, 00)  # Free allocated labs..
#             i.save()

#         print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ {} @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@".format(day))
#         slt_time = shift_1.from_time
#         # print(slt_time)
#         while slt_time < shift_1.to_time:
#             # var_tt = TimetableMaster()

#             break_end = shift_1.break_to_time

#             all_div = DivisionMaster.objects.all()  # repeating to check whether it solve the error or not...*****WORKS
#             for div_loop in all_div:
#                 # print(slt_time)  # problem finder not necessary

#                 if div_loop.curr_slot == shift_1.break_from_time:
#                     div_loop.curr_slot = break_end

#                 # lab or lec to start with...0=lab & 1=lec

#                 laborlec = random.randint(0, 1)
#                 if div_loop.curr_slot == slt_time:

#                     if laborlec == 0:

#                         inc = (datetime.combine(date(1, 1, 1), div_loop.curr_slot) + timedelta(hours=2)).time()
#                         if inc <= shift_1.to_time:
#                             print(div_loop)
#                             print("lab is selected")
#                             print("{} : {}".format(div_loop.curr_slot, inc))
#                             # saving to tt master

#                             lab(div_loop, day, slt_time, inc)

#                             div_loop.curr_slot = inc
#                             div_loop.save()
#                         else:
#                             laborlec = 1

#                     if laborlec == 1:
#                         inc = (datetime.combine(date(1, 1, 1), div_loop.curr_slot) + timedelta(hours=1)).time()
#                         if inc <= shift_1.to_time:
#                             print(div_loop)
#                             print("lecture is selected")
#                             print("{} : {}".format(div_loop.curr_slot, inc))

#                             lecture(div_loop, day, slt_time, inc)

#                             div_loop.curr_slot = inc
#                             div_loop.save()

#                     # free allocated resources after single slot................
#                     fac_l = FacultyMaster.objects.all()
#                     for i in fac_l:

#                         if i.allocated == 2:
#                             i.allocated = 1  # Free allocated faculties ..
#                             i.save()
#                         elif i.allocated == 1:
#                             i.allocated = 0  # Free allocated faculties ..
#                             i.save()

#                     lab_l = LabMaster.objects.all()
#                     for i in lab_l:
#                         if i.allocated == '2':
#                             i.allocated = '1'  # Free allocated labs ..
#                             i.save()
#                         elif i.allocated == '1':
#                             i.allocated = '0'  # Free allocated faculties ..
#                             i.save()

#                     class_l = Classroom.objects.all()
#                     for i in class_l:
#                         i.allocated = False  # Free allocated labs..
#                         i.save()

#             if slt_time == shift_1.break_from_time:
#                 print("*****************break start : {}**************".format(slt_time))
#                 slt_time = break_end
#                 print("*****************break ends : {}**************".format(slt_time))
#             else:
#                 slt_time = (datetime.combine(date(1, 1, 1), slt_time) + timedelta(hours=1)).time()

#     context = {}
#     return render(request, "main.html", context)


# main function ends.........

def unalloc_func(request):
    fac_l = FacultyMaster.objects.all()
    for i in fac_l:
        i.allocated = '0'  # Free allocated faculties ..
        i.save()

    lab_l = LabMaster.objects.all()
    for i in lab_l:
        i.allocated = '0'  # Free allocated labs..
        i.save()

    class_l = Classroom.objects.all()
    for i in class_l:
        i.allocated = False  # Free allocated labs..
        i.save()

    div_l = DivisionMaster.objects.all()
    for i in div_l:
        i.curr_slot = '9:30'  # Free allocated labs..
        i.save()
    TimetableMaster.objects.all().delete()

    return render(request, "home.html")


def try_sft(request):
    tt = TimetableMaster.objects.all()
    context = {
        "tt": tt,
    }
    return render(request, "try.html", context)

    # print("try_sft")
    # shift_1 = ShiftMaster.objects.get(shift_no='1')
    # slt = time(9,30,00)
    # all_div = DivisionMaster.objects.all()
    # print(shift_1.from_time)
    # for div in all_div:
    #     if div.curr_slot == shift_1.from_time:
    #         print("True for div")
    #     print("hello")
    #     if slt == shift_1.from_time:
    #         print("true for slt")
    #     if div.curr_slot == slt:
    #         print("True ")
    # flag_4_true = 0
    #     shift_1 = ShiftMaster.objects.get(shift_no="1")
    #     slt_time = shift_1.from_time
    #     while slt_time<shift_1.to_time:
    #
    #     inc = (datetime.combine(date(1,1,1), slt_time ) + timedelta(hours=1)).time()
    #     print("next slot : %s" % inc)
    #
    return render(request, "try.html")
#
#
#

# increment hours to slot time code..................................................................................
# shift_1 = ShiftMaster.objects.get(shift_no="2")
# slt_time = shift_1.from_time
# inc = (datetime.combine(date(1,1,1), slt_time ) + timedelta(hours=1)).time()
