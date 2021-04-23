from random import choice
from datacenter.models import \
    Chastisement, Mark, Schoolkid, Lesson, Commendation


def check_child_name(child_name):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
        return child
    except Schoolkid.MultipleObjectsReturned:
        print("По заданному имени найдено несколько учеников в базе данных.")
        print("Обеспечьте уникальность имени.")
    except Schoolkid.DoesNotExist:
        print("В имени допущена ошибка.")
        print("В базе данных нет ученика с таким именем")


def remove_chestiments(child_name):
    child = check_child_name(child_name)
    if child:
        this_child_chastiments = Chastisement.objects.filter(schoolkid=child)
        this_child_chastiments.delete()


def fix_marks(child_name):
    child = check_child_name(child_name)
    if child:
        this_child_marks = Mark.objects.filter(schoolkid=child)
        bad_marks = this_child_marks.filter(points__in=[2, 3])
        for mark in bad_marks:
            mark.points = 5
            mark.save()


def create_commendation(child_name, subject):
    child = check_child_name(child_name)
    if child:
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
            this_child_lessons = Lesson.objects.filter(
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
        except IndexError:
            print("Неверно указано название предмета.")
            print("Исправьте ошибку в названии предмета.")
