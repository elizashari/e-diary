from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from random import randrange

PHRASES = ["Теперь у тебя точно все получится!", "Ты многое сделал, я это вижу!",
           "Я вижу, как ты стараешься!","Мы с тобой не зря поработали!", 
           "С каждым разом у тебя получается всё лучше!", "Я тобой горжусь!",
           "Это как раз то, что нужно!", "Здорово!", "Ты на верном пути!",
           "Ты, как всегда, точен!", "Так держать!", "Прекрасное начало!",
           "Замечательно!", "Потрясающе!", "Уже существенно лучше!"]


def find_schoolkid(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print("Ученик не найден")
        return
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено несколько учеников")
        return


def fix_marks(schoolkid_name):
    Mark.objects.filter(
        schoolkid=find_schoolkid(schoolkid_name),
        points__in=[2,3]
        ).update(points=5)
        

def remove_chastisements(schoolkid_name):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid_name)
    chastisements.delete()


def create_commendation(schoolkid_name, subject):
    schoolkid=find_schoolkid(schoolkid_name)
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
        ).order_by("-date").first()
    commendation_text = PHRASES[randrange(len(PHRASES))]
    lesson_date = lesson.date
    lesson_teacher = lesson.teacher
    lesson_subject = lesson.subject
    Commendation.objects.create(
        text=commendation_text,
        schoolkid=schoolkid,
        created=lesson_date,
        subject=lesson_subject,
        teacher=lesson_teacher
        )

