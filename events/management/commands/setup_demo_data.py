from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from events.models import Category, Event


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми категориями, мероприятиями и суперпользователем'

    def handle(self, *args, **options):
        # 1. Создаем суперпользователя
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Суперпользователь admin создан (логин: admin, пароль: admin123)'))
        else:
            self.stdout.write(self.style.NOTICE('Суперпользователь admin уже существует'))

        # 2. Создаем категории
        categories_data = [
            'Мастер-классы',
            'Концерты',
            'Выставки',
            'Лекции',
            'Турниры',
        ]
        category_objects = {}
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_name)
            category_objects[cat_name] = cat

        self.stdout.write(self.style.SUCCESS(f'Категории созданы / проверены: {len(category_objects)}'))

        # 3. Создаем мероприятия
        now = timezone.now()

        events_data = [
            {
                'title': 'Интенсивный воркшоп по Python и Django',
                'category': category_objects['Мастер-классы'],
                'description': 'Практический воркшоп для начинающих разработчиков. Разберем создание веб-приложений, работу с ORM, шаблонизатором и формами Django.',
                'location': 'IT-хаб «Инновация», Конференц-зал 2',
                'event_date': now + timedelta(days=2, hours=3),
                'price': Decimal('0.00'),
                'is_finished': False,
            },
            {
                'title': 'Симфонический рок-концерт «Классика и Драйв»',
                'category': category_objects['Концерты'],
                'description': 'Легендарные мировые рок-хиты в исполнении большого симфонического оркестра с мощным световым шоу.',
                'location': 'БКЗ «Октябрьский», Зал 1',
                'event_date': now + timedelta(days=4, hours=6),
                'price': Decimal('1800.00'),
                'is_finished': False,
            },
            {
                'title': 'Выставка современного цифрового искусства Digital Art 2026',
                'category': category_objects['Выставки'],
                'description': 'Интерактивная экспозиция работ медиахудожников, VR-инсталляции, генеративная графика и искусственный интеллект в искусстве.',
                'location': 'Музей современного искусства «Эрарта»',
                'event_date': now + timedelta(days=7, hours=2),
                'price': Decimal('650.00'),
                'is_finished': False,
            },
            {
                'title': 'Лекция: Архитектура современных веб-сервисов',
                'category': category_objects['Лекции'],
                'description': 'Ведущий архитектор расскажет о микросервисах, кэшировании, асинхронных задачах и надежности распределенных систем.',
                'location': 'Коворкинг «Среда», Лекторий А',
                'event_date': now + timedelta(days=10, hours=4),
                'price': Decimal('0.00'),
                'is_finished': False,
            },
            {
                'title': 'Киберспортивный турнир по CS2 & Dota 2',
                'category': category_objects['Турниры'],
                'description': 'Городской открытый чемпионат с призовым фондом 500 000 рублей. Регистрация команд и зрителей.',
                'location': 'Кибер-арена «CyberSpace Arena»',
                'event_date': now + timedelta(days=14, hours=1),
                'price': Decimal('300.00'),
                'is_finished': False,
            },
            {
                'title': 'Продвинутый мастер-класс: Асинхронный Python и FastAPI',
                'category': category_objects['Мастер-классы'],
                'description': 'Глубокое погружение в asyncio, event loop и построение высоконагруженных API.',
                'location': 'Онлайн / Центр цифровых технологий',
                'event_date': now + timedelta(days=18, hours=5),
                'price': Decimal('1200.00'),
                'is_finished': False,
            },
        ]

        created_count = 0
        for edata in events_data:
            obj, created = Event.objects.get_or_create(
                title=edata['title'],
                defaults=edata
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Мероприятия успешно подготовлены! Новых добавлено: {created_count}'))
