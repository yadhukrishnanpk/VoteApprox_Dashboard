from django import forms
from .models import Vote,Election,Candidate,Voter,Party
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
    
class VotingForm(forms.ModelForm):
    class Meta:
        model= Vote
        fields = ['voter', 'candidate','election']
        widgets = {
            # Adding 'searchable-select' class for JavaScript to find
            'voter': forms.Select(attrs={'class': 'form-select searchable-select'}),
            'election': forms.Select(attrs={'class': 'form-select searchable-select'}),
            'candidate': forms.Select(attrs={'class': 'form-select searchable-select'}),
        }
        labels = {
            'voter': 'Select Citizen',
            'election': 'Choose Election',
            'candidate': 'Select Candidate',
        }
        
from django import forms
from .models import Election

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = '__all__' 
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter election title'
            }),
            # Separate DATE Pickers
            'start_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',  
                'class': 'form-control'
            }),
            # Separate TIME Pickers (Ensure these fields exist in models.py)
            'start_time': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control'
            }),
            'candidates': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
        }
    
    
        
class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = '__all__'
        
        widgets = {
            
            'dob': forms.DateInput(attrs={
                'type': 'date',  
                'class': 'form-control'
            }),
            
        }
        
        
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 1, 
                'style': 'resize:none;', 
                'placeholder': 'Enter Constituency...'
            }),
        }
        
class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = '__all__'
        
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields= ('email', 'username','password1','password2')
        
                
        
        