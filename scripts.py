from random import choice
from datacenter.models import \
    Chastisement, Mark, Schoolkid, Lesson, Commendation


def remove_chestiments(child_name):
    try:
        schoolkids = Schoolkid.objects.all()
        child = schoolkids.get(full_name__contains=child_name)
        chastiments = Chastisement.objects.all()
        this_child_chastiments = chastiments.filter(schoolkid=child)
        this_child_chastiments.delete()
    except Schoolkid.MultipleObjectsReturned:
        print("По заданному имени найдено несколько учеников в базе данных.")
        print("Обеспечьте уникальность имени.")
    except Schoolkid.DoesNotExist:
        print("В имени допущена ошибка.")
        print("В базе данных нет ученика с таким именем")


def fix_marks(child_name):
    try:
        schoolkids = Schoolkid.objects.all()
        child = schoolkids.get(full_name__contains=child_name)
        marks = Mark.objects.all()
        this_child_marks = marks.filter(schoolkid=child)
        bad_marks = this_child_marks.filter(points__in=[2, 3])
        for mark in bad_marks:
            mark.points = 5
            mark.save()
    except Schoolkid.MultipleObjectsReturned:
        print("По заданному имени найдено несколько учеников в базе данных.")
        print("Обеспечьте уникальность имени.")
    except Schoolkid.DoesNotExist:
        print("В имени допущена ошибка.")
        print("В базе данных нет ученика с таким именем")


def create_commendation(child_name, subject):
    try:
        commendations = [
            "Молодец!",
            "Отлично!",
            "Прекрасно!",
            "Талантливо!",
            "Так держать!",
            "Я тобой горжусь!",
            "Я вижу, как ты стараешься!",
            "Я поражен!",
        ]
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
            text=choice(commendations),
            created=current_lesson.date,
            schoolkid=child,
            subject=current_lesson.subject,
            teacher=current_lesson.teacher,
        )
    except Schoolkid.MultipleObjectsReturned:
        print("По заданному имени найдено несколько учеников в базе данных.")
        print("Обеспечьте уникальность имени.")
    except Schoolkid.DoesNotExist:
        print("В имени допущена ошибка.")
        print("В базе данных нет ученика с таким именем.")
    except IndexError:
        print("Неверно указано название предмета.")
        print("Исправьте ошибку в названии предмета.")
