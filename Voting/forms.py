from django import forms
from .models import Vote, Election, Candidate, Voter, Party
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class VotingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Pop the user out of the kwargs so it doesn't break the ModelForm
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter dropdowns to only show data belonging to this user
            self.fields['voter'].queryset = Voter.objects.filter(user=user)
            self.fields['candidate'].queryset = Candidate.objects.filter(user=user)
            self.fields['election'].queryset = Election.objects.filter(user=user)

    class Meta:
        model = Vote
        fields = ['voter', 'candidate', 'election']
        widgets = {
            'voter': forms.Select(attrs={'class': 'form-select searchable-select'}),
            'election': forms.Select(attrs={'class': 'form-select searchable-select'}),
            'candidate': forms.Select(attrs={'class': 'form-select searchable-select'}),
        }
        labels = {
            'voter': 'Select Citizen',
            'election': 'Choose Election',
            'candidate': 'Select Candidate',
        }

class ElectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only show candidates created by this staff user
            self.fields['candidates'].queryset = Candidate.objects.filter(user=user)

    class Meta:
        model = Election
        exclude = ['user'] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter election title'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'candidates': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        exclude = ['user']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CandidateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only show parties created by this staff user
            self.fields['party'].queryset = Party.objects.filter(user=user)

    class Meta:
        model = Candidate
        exclude = ['user']
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
        exclude = ['user']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username') # Removed password fields as UserCreationForm handles them