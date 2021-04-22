from random import choice
from datacenter.models import \
    Chastisement, Mark, Schoolkid, Lesson, Commendation


def remove_chestiments(child):
    chastiments = Chastisement.objects.all()
    this_child_chastiments = chastiments.filter(schoolkid=child)
    this_child_chastiments.delete()


def fix_marks(child):
    marks = Mark.objects.all()
    this_child_marks = marks.filter(schoolkid=child)
    bad_marks = this_child_marks.filter(points__in=[2, 3])
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def create_commendation(child_name, subject):
    schoolkids = Schoolkid.objects.all()
    child = schoolkids.get(full_name__contains=child_name)
    lessons = Lesson.objects.all()
    this_child_lessons = lessons.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
    )
    this_child_subject_lessons = this_child_lessons.filter(
        subject__title=subject,
    )
    current_lesson = choice(this_child_subject_lessons)
    Commendation.objects.create(
        text="Хвалю!",
        created=current_lesson.date,
        schoolkid=child,
        subject=current_lesson.subject,
        teacher=current_lesson.teacher,
    )
