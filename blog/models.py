from django.db import models
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')  # SlugField Charfildga uxshsh faqat url larni yozish uchun ishlatiladi
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='фото')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикация')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обнавления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликавано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')   # Protect foydalanuvchida kamida 1 ta boganish  ulsa ham uni uchurishga yul quymaydi

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})  # bu funksiya denamik urlni taminlab beradi 'post/<slug:post_slug> post_slug = self.slug

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'    # Adminkada blog modeli новости bulib kurinadi
        ordering = ['-time_created']       # verbose_name db dagi hech narssani uzgartirmaydi faqat adminkada ruscha kursatub beradi


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'