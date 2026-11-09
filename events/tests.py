from decimal import Decimal
from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Category, Event


class AfishaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat_workshop = Category.objects.create(name='Мастер-классы')
        self.cat_concert = Category.objects.create(name='Концерты')
        self.cat_exhibition = Category.objects.create(name='Выставки')

        now = timezone.now()

        self.event_free_py = Event.objects.create(
            title='Python Workshop',
            category=self.cat_workshop,
            description='Учим Python и Django с нуля',
            location='Главный корпус, ауд. 101',
            event_date=now + timedelta(days=1),
            price=Decimal('0.00'),
        )

        self.event_paid_concert = Event.objects.create(
            title='Рок концерт',
            category=self.cat_concert,
            description='Живой звук',
            location='Клуб Легенда',
            event_date=now + timedelta(days=3),
            price=Decimal('1500.00'),
        )

    def test_models_str_and_properties(self):
        self.assertEqual(str(self.cat_workshop), 'Мастер-классы')
        self.assertEqual(str(self.event_free_py), 'Python Workshop')
        self.assertTrue(self.event_free_py.is_free)
        self.assertFalse(self.event_paid_concert.is_free)

    def test_event_list_view(self):
        url = reverse('events:event_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Workshop')
        self.assertContains(response, 'Рок концерт')
        self.assertContains(response, 'Бесплатно')
        self.assertContains(response, '1500')

    def test_event_search_and_filter_together(self):
        url = reverse('events:event_list')
        
        # Поиск по категории и запросу: совпадает
        response = self.client.get(url, {'q': 'Python', 'category': self.cat_workshop.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Workshop')
        self.assertNotContains(response, 'Рок концерт')

        # Поиск по другой категории с тем же запросом: ничего не найдено
        response_empty = self.client.get(url, {'q': 'Python', 'category': self.cat_concert.id})
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, 'По вашему запросу ничего не найдено')
        self.assertNotContains(response_empty, 'Python Workshop')

    def test_filter_only_free(self):
        url = reverse('events:event_list')
        response = self.client.get(url, {'only_free': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Workshop')
        self.assertNotContains(response, 'Рок концерт')

    def test_empty_events_list(self):
        Event.objects.all().delete()
        url = reverse('events:event_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Мероприятий пока нет')

    def test_event_detail_view(self):
        url = reverse('events:event_detail', kwargs={'pk': self.event_free_py.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Workshop')
        self.assertContains(response, 'Учим Python и Django с нуля')
        self.assertContains(response, 'Главный корпус, ауд. 101')
        self.assertContains(response, 'Вернуться к списку мероприятий')

    def test_event_create_view(self):
        create_url = reverse('events:event_add')
        date_str = (timezone.now() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M')
        data = {
            'title': 'Турнир по шахматам',
            'category': self.cat_workshop.id,
            'description': 'Блиц турнир',
            'location': 'Шахматный клуб',
            'event_date': date_str,
            'price': '250.00',
        }
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('events:event_list'))
        self.assertTrue(Event.objects.filter(title='Турнир по шахматам').exists())

    def test_event_update_view(self):
        update_url = reverse('events:event_edit', kwargs={'pk': self.event_free_py.pk})
        date_str = (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        data = {
            'title': 'Python Workshop Обновленный',
            'category': self.cat_workshop.id,
            'description': 'Обновленное описание',
            'location': 'Главный корпус, ауд. 202',
            'event_date': date_str,
            'price': '100.00',
        }
        response = self.client.post(update_url, data)
        self.assertEqual(response.status_code, 302)
        self.event_free_py.refresh_from_db()
        self.assertEqual(self.event_free_py.title, 'Python Workshop Обновленный')

    def test_event_delete_view(self):
        delete_url = reverse('events:event_delete', kwargs={'pk': self.event_free_py.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(pk=self.event_free_py.pk).exists())
