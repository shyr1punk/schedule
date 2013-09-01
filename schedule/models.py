from django.db import models


class Faculty(models.Model):
    fac_full = models.CharField(max_length=100)
    fac_short = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%d: %s (%s)' % (self.id, self.fac_full, self.fac_short)


class Subject(models.Model):
    subj_full = models.CharField(max_length=200)
    subj_short = models.CharField(max_length=10)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s.' % (self.id, self.subj_short, self.subj_full)


class Type(models.Model):
    type_full = models.CharField(max_length=30)
    type_short = models.CharField(max_length=10)

    def __unicode__(self):
        return u'ID: %d, Short title: %s, full title: %s.' % (self.id, self.type_short, self.type_full)


class Speciality(models.Model):
    spec_full = models.CharField(max_length=100)
    spec_short = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty)

    def __unicode__(self):
        return u'%d: %s (%s)' % (self.id, self.spec_full, self.spec_short)


class Group(models.Model):
    title = models.CharField(max_length=10)
    course = models.IntegerField()
    spec = models.ForeignKey(Speciality)

    def __unicode__(self):
        return u'ID: %d, Title: %s, course: %s, speciality: %s' % \
               (self.id, self.title, self.course, self.spec.spec_short)


class Teacher(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'ID: %d, name: %s' % \
            (self.id, self.name)


class Lesson(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    subject = models.ForeignKey(Subject)
    teacher = models.ForeignKey(Teacher)
    lesson_type = models.ForeignKey(Type)
    group = models.ForeignKey(Group)
    auditory = models.CharField(max_length=10)

    def __unicode__(self):
        return u'ID %d, number: %s, date: %s, subject: %s, teacher: %s, type: %s, group: %s, auditory: %s ' % \
               (self.id, self.number, self.date, self.subject.subj_full, self.teacher.name,
                self.lesson_type.type_full, self.group.title, self.auditory)
