from django.core.management.base import BaseCommand
from lib_app.models import User
import random


class Command(BaseCommand):
    help = 'Генерация пользователей библиотеки'