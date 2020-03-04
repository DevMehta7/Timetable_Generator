from django.contrib import admin

# Register your models here.
from . models import ShiftMaster, DayMaster, TimetableMaster, SlotMaster, SemMaster, Classroom, LabMaster,\
    SubjectMaster, DivisionMaster, BatchMaster, FacultyMaster

admin.site.register(ShiftMaster)
admin.site.register(SemMaster)
admin.site.register(Classroom)
admin.site.register(LabMaster)
admin.site.register(SubjectMaster)
admin.site.register(DivisionMaster)
admin.site.register(BatchMaster)
admin.site.register(FacultyMaster)
admin.site.register(DayMaster)
admin.site.register(TimetableMaster)
admin.site.register(SlotMaster)
