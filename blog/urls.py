from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', BlogHome.as_view(), name='index'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('contact/', ContactFormView.as_view(), name='contact'),

]



"""
djangoda dinamik urllarga 5 ta tip ishlatiladi

<str:pk>--lubaya ne pustoy stroka, iskluchit simvol '/'

<int:pk> - lubaya palajetilno chislo, bkluchaya 0

<slug:pk> - latinitsa ASCII, simvol defis i podcherkviniya

<uuid:pk> - sifre, mali latinskiy simvole ASCII, defis

<path:pk> - lubaya ne pustoy stroka, vkluchayet simvol '/'
 
category/<slug:cat_slug>/   slug bu title-dagi suzlarnu url kurinishidagi shakli
"""