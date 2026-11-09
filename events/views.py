from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Event
from .forms import EventForm


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = Event.objects.select_related('category').order_by('event_date')
        
        # Поиск по названию (icontains)
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(title__icontains=query)
            
        # Фильтрация по категории
        category_id = self.request.GET.get('category', '').strip()
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        # Фильтрация «Только бесплатные»
        only_free = self.request.GET.get('only_free', '').strip()
        if only_free == '1':
            queryset = queryset.filter(price=0)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_query'] = self.request.GET.get('q', '').strip()
        context['selected_category'] = self.request.GET.get('category', '').strip()
        context['only_free'] = self.request.GET.get('only_free', '').strip()
        # Флаг: был ли применен хоть один фильтр
        context['is_filtered'] = bool(context['selected_query'] or context['selected_category'] or context['only_free'])
        context['total_events_count'] = Event.objects.count()
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить мероприятие'
        context['button_text'] = 'Создать событие'
        return context


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Редактировать: {self.object.title}'
        context['button_text'] = 'Сохранить изменения'
        return context


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    context_object_name = 'event'
    success_url = reverse_lazy('events:event_list')
