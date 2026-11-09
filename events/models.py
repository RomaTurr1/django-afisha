from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    location = models.CharField('Место проведения', max_length=255)
    event_date = models.DateTimeField('Дата и время проведения')
    price = models.DecimalField('Стоимость билета', max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Категория'
    )
    is_finished = models.BooleanField('Мероприятие завершено', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['event_date']

    def __str__(self):
        return self.title

    @property
    def is_free(self):
        return self.price == 0
