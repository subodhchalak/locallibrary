from django.db import models
from django.urls import reverse         # get_absolute_url()

from django.contrib.auth.models import User

import uuid                             # Required for unique book instances

from datetime import date

# Create your models here.


# ---------------------------------------------------------------------------- #
#                                  Genre Model                                 #
# ---------------------------------------------------------------------------- #

class Genre(models.Model):
    
    name=models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science fiction)")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])


# ---------------------------------------------------------------------------- #
#                                 Author Model                                 #
# ---------------------------------------------------------------------------- #

class Author(models.Model):
    
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(null=True, blank=True)
    date_of_death=models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['-id']
        
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return (f"{self.last_name} {self.first_name}")
    




# ---------------------------------------------------------------------------- #
#                                Language Model                                #
# ---------------------------------------------------------------------------- #


class Language(models.Model):
    
    name= models.CharField(max_length=200, help_text="Enter the name of natural language of the book (e.g. English, Marathi, Hindi etc.)")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])
    
    
    

# ---------------------------------------------------------------------------- #
#                                  Book Model                                  #
# ---------------------------------------------------------------------------- #



class Book(models.Model):
    
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text="Enter a short description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    
    # One book usually have only one Author, but one Author may have multiple books
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, help_text="Select a author for this book")
    
    # One book book may have multiple genres and also one genre may have multiple books      
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    
    # One book book may have only one language and one language may have multiple books  
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, help_text="Select a language for this book")
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
    
    
    
# ---------------------------------------------------------------------------- #
#                              BookInstance Model                              #
# ---------------------------------------------------------------------------- #



class BookInstance(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this book across whole libary")
    imprint = models.CharField(max_length=200, help_text="Short info about imprint version")
    due_back = models.DateField(null=True, blank=True, help_text="Date Format: YYYY-MM-DD")
    
    
    # Once book copy can have only one Title but ine Title may have multiple book copies
    # on_delete=models.RESTRICT  -  It will restrict 'Title' being deleted if it is being used by this model
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    loan_status = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),        
    )
    
    status = models.CharField(
        max_length = 1,
        choices = loan_status,
        default = 'm',
        blank = True,
        help_text = "Book Availability",
    )
    
    
    class Meta:
        ordering = ('due_back', )
        permissions = (("can_mark_returned", "Set book as returned"), )
        
    def __str__(self):
        # queryset = self.Book.filter(self.status__exact="a")
        return (f"{self.id} ({self.book.title}) ({self.status})")
    
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    
    

# ---------------------------------------------------------------------------- #
#                               BookRequest Model                              #
# ---------------------------------------------------------------------------- #


class BookInstanceRequest(models.Model):
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    copy = models.ForeignKey(BookInstance, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.sender.username

    
    
    
    
                       
                       