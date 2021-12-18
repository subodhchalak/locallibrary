from django.contrib import admin

from catalogApp.models import *

# Register your models here.

admin.site.register(Genre)
admin.site.register(Language)

# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)


# ------------------------------------- X ------------------------------------ #


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]       # Display fields in tuple horizontally
    inlines = [BooksInline]
    
admin.site.register(Author, AuthorAdmin)


# ------------------------------------- X ------------------------------------ #


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0                                           # remove extra fields for adding new books

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('genre',)
    inlines = [BooksInstanceInline]               # It will allow to add book instances in book page itself


# ------------------------------------- X ------------------------------------ #


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('borrower', 'status', 'due_back')
    
    fieldsets = (
        (None, {
            "fields": ('book', 'imprint', 'id'),
        }),
        
        ('Availability', {
             'fields' : ('status', 'due_back', 'borrower')
         }),
    )
    
    
# ------------------------------------- X ------------------------------------ #


@admin.register(BookInstanceRequest)
class BookInstanceRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'book', 'copy')
    list_filter = ('sender', 'book', 'copy')