from .models import *
from django.db.models import Count

menu = [
    {'title': 'Добавить статя', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},


]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('blog'))

        user_menu = menu.copy()  # menu ni kopy qilsak user_menu xotirada boshqa joyda saqlanadi va uni uzgartirsak menu dan hech narsa uzgarmaydi
        if not self.request.user.is_authenticated:
            user_menu.pop(0)  # agar user ruyhatdan utmahan bulsa

        context['menu'] = user_menu
        context['cats'] = cats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context
