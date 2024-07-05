from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from quotes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('author/<int:author_id>/', views.author_detail, name='author-detail'),
    path('add-author/', views.add_author, name='add-author'),
    path('add-quote/', views.add_quote, name='add-quote'),
    path('quotes/', views.quote_list, name='quote-list'),
    path('tag/<str:tag_name>/', views.tag_search, name='tag-search'),
    path('top-tags/', views.top_tags, name='top-tags'),
]





