from django.shortcuts import render, redirect, get_object_or_404

import datetime
from django.urls.base import reverse_lazy

from django.views import generic

from catalogApp.models import *

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from catalogApp.forms import RenewBookForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm  


# Create your views here.


# ---------------------------------------------------------------------------- #
#                                   indexView                                  #
# ---------------------------------------------------------------------------- #


def indexView(request):
    
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    
    num_authors = Book.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_languages = Language.objects.all().count()
    
    
    num_visits = request.session.get('num_visits', 0)     # setting  'num_visit' with initial value 0
    request.session['num_visits'] = num_visits + 1        # increment visit count with every visit

    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
        'num_languages': num_languages,

    }
    
    template_name = 'catalogApp/index.html'
    return render(request, template_name, context)


# ---------------------------------------------------------------------------- #
#                                 BookListView                                 #
# ---------------------------------------------------------------------------- #


class BookListView(generic.ListView):
    model = Book
    template_name = 'catalogApp/book_list.html'
    paginate_by = 10
    
    
# ---------------------------------------------------------------------------- #
#                                BookDetailView                                #
# ---------------------------------------------------------------------------- #


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalogApp/book_detail.html'
    
    
# ---------------------------------------------------------------------------- #
#                           LoanedBooksByUserListView                          #
# ---------------------------------------------------------------------------- #


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalogApp/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        borrower_list = BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        return borrower_list
    
    
    
# ---------------------------------------------------------------------------- #
#                            LoanedBooksAllListView                            #
# ---------------------------------------------------------------------------- #


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
        # all_borrowed = BookInstance.objects.filter(status__exact="o").order_by('due_back')
        # return all_borrowed
    
    
# ---------------------------------------------------------------------------- #
#                             renew_book_librarianView                         #
# ---------------------------------------------------------------------------- #


@login_required()
@permission_required('catalogApp.can_mark_returned', raise_exception=True)
def renew_book_librarianView(request, pk):
    
    book_instance = get_object_or_404(BookInstance, pk=pk)
    form = RenewBookForm()
    
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            
            return redirect('borrowed')
    
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        
    context = {'form': form, 'book_instance': book_instance}
    template_name = 'catalogApp/book_renew_librarian.html'
    
    return render(request, template_name, context)
        
    
    
# ---------------------------------------------------------------------------- #
#                          Author Model Generic Views                          #
# ---------------------------------------------------------------------------- #


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    # initial = {'date_of_death': '25/08/2025'}
    template_name = 'catalogApp/author_form.html'
    success_url = reverse_lazy('authors')
    
    
class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/author_form.html'
    success_url = reverse_lazy('authors')
    
    
class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/author_confirm_delete.html'
    
    
class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalogApp/author_list.html'
    paginate_by = 10
    
    
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalogApp/author_detail.html'




# ---------------------------------------------------------------------------- #
#                           Book Model Generic Views                           #
# ---------------------------------------------------------------------------- #


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/book_form.html'
    success_url = reverse_lazy('books')
    
    
class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/book_form.html'
    success_url = reverse_lazy('books')
    
    
class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalogApp.can_mark_returned'
    success_url = reverse_lazy('books')
    template_name = 'catalogApp/book_confirm_delete.html'
    
    
    
# ---------------------------------------------------------------------------- #
#                            Genre Model Class Views                           #
# ---------------------------------------------------------------------------- #


class GenreListView(generic.ListView):
    model = Genre
    template_name = 'catalogApp/genre_list.html'
    
    
class GenreDetailView(generic.DetailView):
    model = Genre
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/genre_detail.html'
    
    
class GenreCreate(PermissionRequiredMixin, CreateView):
    model = Genre
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/genre_form.html'
    
    
class GenreUpdate(PermissionRequiredMixin,UpdateView):
    model = Genre
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/genre_form.html'
    
    
class GenreDelete(PermissionRequiredMixin, DeleteView):
    model = Genre
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/genre_confirm_delete.html'
    success_url = reverse_lazy('genres')
    
    
    
# ---------------------------------------------------------------------------- #
#                          Language Model Class Views                          #
# ---------------------------------------------------------------------------- #


class LanguageListView(generic.ListView):
    model = Language
    template_name = 'catalogApp/language_list.html'
    
    
class LanguageDetailView(generic.DetailView):
    model = Language
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/language_detail.html'
    
    
class LanguageCreate(PermissionRequiredMixin, CreateView):
    model = Language
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/language_form.html'
    
    
class LanguageUpdate(PermissionRequiredMixin,UpdateView):
    model = Language
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/language_form.html'
    
    
class LanguageDelete(PermissionRequiredMixin, DeleteView):
    model = Language
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/language_confirm_delete.html'
    success_url = reverse_lazy('languages')
    
    
    
# ---------------------------------------------------------------------------- #
#                         BookInstance Model Class View                        #
# ---------------------------------------------------------------------------- #


    
class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = ['book', 'imprint', 'due_back', 'borrower', 'status']
    exclude = ['id']
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/bookinstance_form.html'
    success_url = reverse_lazy('books')
    
class BookInstanceUpdate(PermissionRequiredMixin,UpdateView):
    model = BookInstance
    fields = '__all__'
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/bookinstance_form.html'
    success_url = reverse_lazy('books')
    
class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    model = BookInstance
    permission_required = 'catalogApp.can_mark_returned'
    template_name = 'catalogApp/bookinstance_confirm_delete.html'
    success_url = reverse_lazy('books')
    
    
    
# ---------------------------------------------------------------------------- #
#                              User Creation Form                              #
# ---------------------------------------------------------------------------- #


def register_userView(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            
    template_name="registration/register_user.html"
    context = {'form':form }
    
    return render(request, template_name, context)




def error_404(request, exception):
        data = {}
        return render(request,'catalogApp/error_404.html', data)

def error_500(request):
        data = {}
        return render(request,'catalogApp/error_500.html', data)
