from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, FormView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin  # bu huddi @login_requerid dekoratorga uxshab ishlaydi
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


class BlogHome(DataMixin, ListView):
    # paginate_by = 3
    model = Blog  # posts = Blog.objects.all()      # viewsda claslar bilan ishlaganda model va context_object_name kursatilishi kerak bulmasa ishlamaydi
    template_name = 'blog/index.html'
    context_object_name = 'posts'  # htnl ga malumot posts ichida boradi

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # temadagi ListView clasidan meros oldik hamma kalitlarini
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # get_queryset orqali Blogdan qanday malumot olishni kursatib utsak buladi
        return Blog.objects.filter(is_published=True).select_related('cat')


class ShowPost(DataMixin, DeleteView):  # DeleteView id ga qqarab 1 ta malumotni db dan olib beradi
    model = Blog
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'  # post_slug urli orqali kelgan malumotni Blog modeldan topib beradi agar urlda pk bulsa pk_url_kwargs yoailadi
    context_object_name = 'post'  # malumot htmlga post orqali boradi

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            **kwargs)  # get_context_data da biz uzimiz yuqoeidagi classga malumot qushamiz
        # context['title'] = context['post']                       # htmlda title deb yozsak post qiymati chiqadi
        # context['menu'] = menu
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class BlogCategory(DataMixin, ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = "Категория -" + str(context['posts'][0].cat)
        # context['cat_selected'] = context['posts'][0].cat_id
        # context['menu'] = menu
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title="Категория -" + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')  # LoginRequiredMixinfoydalanuvchi ruyhatdan utmagan bulsa index ga otib yuboradi

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Добавить статя'
        # context['menu'] = menu
        c_def = self.get_user_context(title='Добавить статя')
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm  # htmlga ketadigan forma
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')  # post request ishlasa indexga otib yuboradi

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        subject = 'Message'
        body = {
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'content': form.cleaned_data['content']

        }
        message = '\n'.join(body.values())   # values malumotlarni list qilib beradi

        try:
            send_mail(
                subject,
                message,
                form.cleaned_data['email'],
                ["tuychiyevbaxtiyor06@gmail.com"],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse('Найден некорректно  ')
        return redirect('index')