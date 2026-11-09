from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'description', 'location', 'event_date', 'price', 'is_finished']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Концерт группы Кино'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Подробное описание мероприятия'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Клуб Космонавт, Санкт-Петербург'}),
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'placeholder': '0.00'}),
            'is_finished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Название мероприятия',
            'category': 'Категория',
            'description': 'Описание',
            'location': 'Место проведения',
            'event_date': 'Дата и время проведения',
            'price': 'Стоимость билета (руб.)',
            'is_finished': 'Мероприятие уже завершено',
        }
        help_texts = {
            'price': 'Укажите 0, если мероприятие бесплатное.',
        }
