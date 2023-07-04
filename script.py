from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
import random


def fix_marks(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print("Ученик не найден")
        return
    except MultipleObjectsReturned:
        print("Найдено несколько учеников")
        return
    marks = Mark.objects.filter(schoolkid=schoolkid,points__in=[2,3])
    for mark in marks:
        mark.points = 5
        mark.save()
        

def remove_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains = schoolkid_name)
    except ObjectDoesNotExist:
        print("По запросу ученик не найден")
        return
    except MultipleObjectsReturned:
        print("По запросу найдено несколько учеников")
        return
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid_name, subject):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains = schoolkid_name)
    except ObjectDoesNotExist:
        print("По запросу ученик не найден")
        return
    except MultipleObjectsReturned:
        print("По запросу найдено несколько учеников")
        return
    try:
        lessons = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject)
        lesson = lessons[0]
    except IndexError:
        print("По запросу предмет не найден. Проверьте правильность написания названия предмета")
        return
    phrases = ["Теперь у тебя точно все получится!", "Ты многое сделал, я это вижу!", "Я вижу, как ты стараешься!", "Мы с тобой не зря поработали!", "С каждым разом у тебя получается всё лучше!", "Я тобой горжусь!", "Это как раз то, что нужно!", "Здорово!", "Ты на верном пути!", "Ты, как всегда, точен!", "Так держать!", "Прекрасное начало!", "Замечательно!", "Потрясающе!", "Уже существенно лучше!"]
    phrase = random.choice(phrases)
    Commendation.objects.create(text = phrase, created = lesson.date, schoolkid = schoolkid, subject = lesson.subject, teacher = lesson.teacher)


