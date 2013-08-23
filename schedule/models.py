from django.db import models


class AcademicTitle(models.Model):
    a_title_full = models.CharField(max_length=30)
    a_title_short = models.CharField(max_length=5)


class AcademicDegree(models.Model):
    a_degree_full = models.CharField(max_length=30)
    a_degree_short = models.CharField(max_length=5)


class Faculty(models.Model):
    fac_full = models.CharField(max_length=30)
    fac_short = models.CharField(max_length=10)


class Subject(models.Model):
    subj_full = models.CharField(max_length=30)
    subj_short = models.CharField(max_length=10)


class Type(models.Model):
    type_full = models.CharField(max_length=30)
    type_short = models.CharField(max_length=10)


class Speciality(models.Model):
    spec_full = models.CharField(max_length=50)
    spec_short = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty)


class Chair(models.Model):
    cha_full = models.CharField(max_length=50)
    cha_short = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty)


class Group(models.Model):
    title = models.CharField(max_length=10)
    course = models.IntegerField()
    spec = models.ForeignKey(Speciality)


class Teacher(models.Model):
    academic_degree = models.ForeignKey(AcademicDegree)
    academic_title = models.ForeignKey(AcademicTitle)
    chair = models.ForeignKey(Chair)
    name = models.CharField(max_length=50)


class Auditory(models.Model):
    title = models.CharField(max_length=30)


class Lesson(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    subject = models.ForeignKey(Subject)
    teacher = models.ForeignKey(Teacher)
    lesson_type = models.ForeignKey(Type)
    group = models.ForeignKey(Group)
    auditory = models.ForeignKey(Auditory)