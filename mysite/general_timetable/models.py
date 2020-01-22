from django.db import models


# Create your models here.
class ShiftMaster(models.Model):  # example = SFT 1,SFT 2...
    shift_no = models.IntegerField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    break_from_time = models.TimeField()
    break_to_time = models.TimeField()

    def __str__(self):
        return str(self.shift_no)


class SemMaster(models.Model):  # example = Sem 1,Sem 2...
    sem_no = models.IntegerField()

    def __str__(self):
        return str(self.sem_no)


class Classroom(models.Model): # example = C1,C2...
    class_no = models.IntegerField()

    def __str__(self):
        return str(self.class_no)


class LabMaster(models.Model): # example = lab1,lab2...
    Lab_no = models.IntegerField()

    def __str__(self):
        return str(self.Lab_no)


class SubjectMaster(models.Model): # example = CP,DBMS...
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    sem = models.ForeignKey('SemMaster', on_delete=models.CASCADE)
    max_lab = models.IntegerField(default=0)
    max_lec = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


class DivisionMaster(models.Model):  # example = Co11,Co12...
    div_no = models.CharField(max_length=20)
    sem = models.ForeignKey('SemMaster', on_delete=models.CASCADE)
    shift = models.ForeignKey('ShiftMaster', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.div_no)


class BatchMaster(models.Model): # example = Co111,Co112...
    batch_no = models.CharField(max_length=20)
    div = models.ForeignKey('DivisionMaster', on_delete=models.CASCADE)

    def __str__(self):
        return "%s%s" % (self.div, self.batch_no)


class FacultyMaster(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=20)
    shift = models.ForeignKey(ShiftMaster,on_delete=models.CASCADE)
    hire_date = models.DateField()
    subject = models.ManyToManyField('SubjectMaster', related_name='faculties')

    def __str__(self):
        return "%s" % (self.name)

