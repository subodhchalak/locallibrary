from django.urls import path
from catalogApp.views import *


from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest

urlpatterns = [
    path('', indexView, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    path('mybooks/', LoanedBooksByUserListView.as_view(), name='mybooks'),
    path('borrowed/', LoanedBooksAllListView.as_view(), name='borrowed'),
    
    path('book/<uuid:pk>/renew/', renew_book_librarianView, name='renew-book-librarian'),
    
    
    path('author/create/', AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', AuthorDelete.as_view(), name='author-delete'),
    
    path('authors/', AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    
    path('book/create/', BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', BookDelete.as_view(), name='book-delete'),
    
    path('genres/', GenreListView.as_view(), name='genres'),
    path('genre/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    
    path('genre/create/', GenreCreate.as_view(), name='genre-create'),
    path('genre/<int:pk>/update/', GenreUpdate.as_view(), name='genre-update'),
    path('genre/<int:pk>/delete/', GenreDelete.as_view(), name='genre-delete'),
    
    path('languages/', LanguageListView.as_view(), name='languages'),
    path('language/<int:pk>/', LanguageDetailView.as_view(), name='language-detail'),
    
    path('language/create/', LanguageCreate.as_view(), name='language-create'),
    path('language/<int:pk>/update/', LanguageUpdate.as_view(), name='language-update'),
    path('langauge/<int:pk>/delete/', LanguageDelete.as_view(), name='language-delete'),
    
    path('bookinstance/create/', BookInstanceCreate.as_view(), name='bookinstance-create'),
    path('bookinstance/<str:pk>/update/', BookInstanceUpdate.as_view(), name='bookinstance-update'),
    path('bookinstance/<str:pk>/delete/', BookInstanceDelete.as_view(), name='bookinstance-delete'),
    
    path('register/', register_userView, name='register-user'),
    
]



