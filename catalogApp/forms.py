import datetime

from django import forms
from django.forms import ModelForm

from django.core.exceptions import ValidationError

from catalogApp.models import BookInstance, Author

from django.contrib.auth.forms import UserCreationForm



# ---------------------------------------------------------------------------- #
#                           RenewBookForm(forms.Form)                          #
# ---------------------------------------------------------------------------- #


class RenewBookForm(forms.Form):
    
    renewal_date = forms.DateField(help_text="Please enter a date between today and max 4 weeks ahead.")
    
    
    def cleaned_renewal_date(self):
        
        data = self.cleaned_data['renewal_date']
        
        if data < datetime.date.today():
            raise ValidationError("Please don't enter past date.")
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError("Future date should not be greater than 4 weeks from today.")
        
        return data
    
    
    
    



# ---------------------------------------------------------------------------- #
#                                 AuthorAddForm                                #
# ---------------------------------------------------------------------------- #


# class AuthorAddForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = '__all__'
    
    
    
    
    
    
    
    
  
# ---------------------------------------------------------------------------- #
#                           RenewBookForm(ModelForm):                          #
# ---------------------------------------------------------------------------- #


# class RenewBookForm(ModelForm):
    
#     class Meta:
#         model = BookInstance
#         fields = ['due_back']
#         labels = {'due_back': 'New renewal date'}
#         help_texts = {'due_back': 'Enter a date between now and 4 weeks (default 3).'}
        
        
#     def cleaned_due_back(self):
        
#         data = self.cleaned_data['due_back']
        
#         if data < datetime.date.today():
#             raise ValidationError("Please don't enter past date.")
        
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError("Future date should not be greater than 4 weeks from today.")
        
#         return data
    
    
    
    
