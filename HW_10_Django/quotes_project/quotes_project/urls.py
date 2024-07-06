from django.contrib import admin
from django.urls import path, include
from quotes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='index'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('tag/<str:tag_name>/', views.tag_quotes, name='tag_quotes'),
]

urlpatterns += [
    path('scrape/', views.scrape_data, name='scrape_data'),
]