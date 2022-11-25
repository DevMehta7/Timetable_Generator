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


class SemMaster(models.Model):  # example = Sem 1,Sem 2...(for student group)
    sem_no = models.IntegerField()

    def __str__(self):
        return str(self.sem_no)


class Classroom(models.Model):  # example = C1,C2...
    class_no = models.IntegerField()
    allocated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.class_no)


class LabMaster(models.Model):  # example = lab1,lab2...
    Lab_no = models.IntegerField()
    allocated = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Lab_no)


class SubjectMaster(models.Model):  # example = SC,DBMS...
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    sem = models.ForeignKey('SemMaster', on_delete=models.CASCADE)
    lab_rm = models.IntegerField(default=0)
    lec_rm = models.IntegerField(default=0)
    max_lab = models.IntegerField(default=0)
    max_lec = models.IntegerField(default=0)

    def __str__(self):
        return str(self.short_name)


class DivisionMaster(models.Model):  # example = Co11,Co12... (for student group)
    div_no = models.CharField(max_length=20)
    sem = models.ForeignKey('SemMaster', on_delete=models.CASCADE)
    shift = models.ForeignKey('ShiftMaster', on_delete=models.CASCADE)
    allocated = models.IntegerField(default='0')
    curr_slot = models.TimeField(default="9:30")

    def __str__(self):
        return str(self.div_no)


class BatchMaster(models.Model):  # example = Co111,Co112...(for student group)
    batch_no = models.CharField(max_length=20)
    div = models.ForeignKey('DivisionMaster', on_delete=models.CASCADE)

    def __str__(self):
        return "%s%s" % (self.div, self.batch_no)


class FacultyMaster(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=20)
    shift = models.ForeignKey('ShiftMaster', on_delete=models.CASCADE)
    hire_date = models.DateField()
    subject = models.ManyToManyField('SubjectMaster', related_name='faculties')
    weight = models.IntegerField(default=10)
    allocated = models.IntegerField(default='0')

    def __str__(self):
        return "%s" % self.name


# not sure....


class DayMaster(models.Model):
    day = models.CharField(max_length=20)

    def __str__(self):
        return "%s" % self.day


class TimetableMaster(models.Model):
    slt_start = models.TimeField(default='9:30')
    slt_end = models.TimeField(default='9:30')
    laborlec = models.BooleanField(default=True)  # 0=lab & 1=lec
    day = models.ForeignKey('DayMaster', on_delete=models.CASCADE)
    faculty = models.ForeignKey('FacultyMaster', on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, null=True)
    lab = models.ForeignKey('LabMaster', on_delete=models.CASCADE, null=True)
    div = models.ForeignKey('DivisionMaster', on_delete=models.CASCADE)
    batch = models.ForeignKey('BatchMaster', on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey('SubjectMaster', on_delete=models.CASCADE)

    def __str__(self):
        return "%s -- (%s-%s) -- %s" % (self.day, self.slt_start, self.slt_end, self.div)
