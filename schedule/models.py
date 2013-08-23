from django.db import models


class AcademicTitle(models.Model):
    a_title_full = models.CharField(max_length=30)
    a_title_short = models.CharField(max_length=5)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s.' % (self.id, self.a_title_short, self.a_title_full)


class AcademicDegree(models.Model):
    a_degree_full = models.CharField(max_length=30)
    a_degree_short = models.CharField(max_length=5)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s.' % (self.id, self.a_degree_short, self.a_degree_full)


class Faculty(models.Model):
    fac_full = models.CharField(max_length=30)
    fac_short = models.CharField(max_length=10)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s.' % (self.id, self.fac_short, self.fac_full)


class Subject(models.Model):
    subj_full = models.CharField(max_length=30)
    subj_short = models.CharField(max_length=10)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s.' % (self.id, self.subj_short, self.subj_full)


class Type(models.Model):
    type_full = models.CharField(max_length=30)
    type_short = models.CharField(max_length=10)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s.' % (self.id, self.type_short, self.type_full)


class Speciality(models.Model):
    spec_full = models.CharField(max_length=50)
    spec_short = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s.' % (self.id, self.spec_short, self.spec_full)


class Chair(models.Model):
    cha_full = models.CharField(max_length=50)
    cha_short = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s, faculty: %s' % \
               (self.id, self.cha_full, self.cha_short, self.faculty.fac_short)


class Group(models.Model):
    title = models.CharField(max_length=10)
    course = models.IntegerField()
    spec = models.ForeignKey(Speciality)

    def __unicode__(self):
        return u'ID: %d, Title: %s, course: %s, speciality: %s' % \
               (self.id, self.title, self.course, self.spec.spec_short)


class Teacher(models.Model):
    academic_degree = models.ForeignKey(AcademicDegree)
    academic_title = models.ForeignKey(AcademicTitle)
    chair = models.ForeignKey(Chair)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'ID: %d, name: %s, degree: %s, title: %s, chair: %s' % \
            (self.id, self.name, self.academic_degree.a_degree_short, self.academic_title.a_title_short, self.chair.cha_short)


class Auditory(models.Model):
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return u'ID %d, number: %s' % (self.id, self.title)


class Lesson(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    subject = models.ForeignKey(Subject)
    teacher = models.ForeignKey(Teacher)
    lesson_type = models.ForeignKey(Type)
    group = models.ForeignKey(Group)
    auditory = models.ForeignKey(Auditory)

    def __unicode__(self):
        return u'ID %d, number: %s, date: %s, subject: %s, teacher: %s, type: %s, group: %s, auditory: %s ' % \
               (self.id, self.number, self.date, self.subject.subj_full, self.teacher.name,
                self.lesson_type.type_full, self.group.title, self.auditory.title)