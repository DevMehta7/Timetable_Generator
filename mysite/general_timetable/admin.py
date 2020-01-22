from django.contrib import admin

# Register your models here.
from . models import ShiftMaster,SemMaster,Classroom,LabMaster,SubjectMaster,DivisionMaster,BatchMaster,FacultyMaster

admin.site.register(ShiftMaster)
admin.site.register(SemMaster)
admin.site.register(Classroom)
admin.site.register(LabMaster)
admin.site.register(SubjectMaster)
admin.site.register(DivisionMaster)
admin.site.register(BatchMaster)
admin.site.register(FacultyMaster)

