from django.shortcuts import render, get_object_or_404, redirect
from .models import Candidate, Vote, Voter, Party, Election
from django.db.models import Count, Q
from .forms import VotingForm, VoterForm, ElectionForm, CandidateForm, PartyForm
from django.utils import timezone
from datetime import datetime
from zoneinfo import ZoneInfo
from django.conf import settings
from .forms import RegistrationForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

# Helper to filter election data by user
def get_election_data(request, election_id):
    # Only show elections belonging to the logged-in user
    all_elections = Election.objects.filter(user=request.user)
    if election_id:
        current_election = get_object_or_404(Election, id=election_id, user=request.user)
    else:
        current_election = all_elections.first()
    return current_election, all_elections

@login_required
def index(request, election_id=None):
    current_election, all_elections = get_election_data(request, election_id)
    
    # Isolated counts
    party_count = Party.objects.filter(user=request.user).count()
    election_count = all_elections.count()
    
    if current_election:
        data_list = current_election.candidates.annotate(
            received_votes=Count('vote', filter=Q(vote__election=current_election))
        )
        total_registered_voters = Voter.objects.filter(user=request.user).count()       
        candidate_count = current_election.candidates.count()

        for person in data_list:
            if total_registered_voters > 0:
                percentage = (person.received_votes / total_registered_voters) * 100
                person.vote_percentage = round(float(percentage), 1)
            else:
                person.vote_percentage = 0
    else:
        data_list = []
        total_registered_voters = 0
        candidate_count = 0

    context = {
        'election': current_election,
        'all_elections': all_elections,
        'data_list': data_list,
        'vote_count': total_registered_voters, 
        'party_count': party_count,
        'candidate_count': candidate_count,
        'election_count': election_count,
    }
    return render(request, "index.html", context)

@login_required
def voters_list(request, election_id=None):
    current_election, all_elections = get_election_data(request, election_id)
    voters = Voter.objects.filter(user=request.user).prefetch_related('vote_set__candidate__party')
    
    for voter in voters:
        vote_record = voter.vote_set.filter(election=current_election).first()
        if vote_record:
            voter.voted_for_party = vote_record.candidate.party.name
            voter.voted_for_candidate = vote_record.candidate.name
        else:
            voter.voted_for_party = "Not Voted"
            voter.voted_for_candidate = "Not Voted"
    
    return render(request, "voter_list.html", {
        'voters': voters, 
        'all_elections': all_elections, 
        'election': current_election
    })

@login_required
def candidate_list(request, election_id=None):
    addcandidate = Candidate.objects.filter(user=request.user)
    current_election, all_elections = get_election_data(request, election_id)
    
    candidates = current_election.candidates.all() if current_election else []
    
    context = {
        'all_elections': all_elections,
        'election': current_election,
        'candidate': candidates,
        'addcandidate': addcandidate
    }
    return render(request, "candidatelist.html", context)

@login_required
def party_list(request, election_id=None):
    addparty = Party.objects.filter(user=request.user)
    current_election, all_elections = get_election_data(request, election_id)
    
    if current_election:
        parties = Party.objects.filter(user=request.user, candidates__in=current_election.candidates.all()).distinct()
    else:
        parties = []
    
    context = {
        'all_elections': all_elections,
        'election': current_election,
        'party': parties,
        'add': addparty,
    }
    return render(request, "partylist.html", context)

@login_required
def election_list(request):
    all_elections = Election.objects.filter(user=request.user)
    current_time = timezone.now()
    user_tz = ZoneInfo(settings.TIME_ZONE)
    for e in all_elections:
        if e.start_date and e.start_time:
            naive_start = datetime.combine(e.start_date, e.start_time)
            naive_end = datetime.combine(e.end_date, e.end_time)
            e.full_start = naive_start.replace(tzinfo=user_tz)
            e.full_end = naive_end.replace(tzinfo=user_tz)
        else:
            e.full_start = current_time
            e.full_end = current_time
    context = {
        'all_elections': all_elections,
        'elections': all_elections, 
        'current_time': current_time,
    }
    return render(request, "electionlist.html", context)

# MODIFYING VIEWS
@login_required
def vote_cast(request, election_id=None):
    if request.method == "POST":
        form = VotingForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(request.path)
    else:
        form = VotingForm(user=request.user)
        
    current_election, all_elections = get_election_data(request, election_id)
    parties = Party.objects.filter(user=request.user, candidates__in=current_election.candidates.all()).distinct() if current_election else []

    context = {'form': form, 'all_elections': all_elections, 'election': current_election, 'party': parties}
    return render(request, "Modifying/voting.html", context)

@login_required
def Electionadd(request, election_id=None):
    if request.method == "POST":
        form = ElectionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            election = form.save(commit=False)
            election.user = request.user
            election.save()
            form.save_m2m() # Important for ManyToMany candidates
            return redirect(request.path)
    else:
        form = ElectionForm(user=request.user)
        
    current_election, all_elections = get_election_data(request, election_id)
    context = {'form': form, 'all_elections': all_elections, 'election': current_election}
    return render(request, "Modifying/electionadd.html", context)

@login_required
def votersadd(request, election_id=None):
    if request.method == "POST":
        form = VoterForm(request.POST, request.FILES)
        if form.is_valid():
            voter = form.save(commit=False)
            voter.user = request.user
            voter.save()
            return redirect(request.path)
    else:
        form = VoterForm()
        
    current_election, all_elections = get_election_data(request, election_id)
    context = {'form': form, 'all_elections': all_elections, 'election': current_election}
    return render(request, "Modifying/votersadd.html", context)

@login_required
def candidateadd(request, election_id=None):
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.save()
            return redirect(request.path)
    else:
        form = CandidateForm(user=request.user)
        
    current_election, all_elections = get_election_data(request, election_id)
    context = {'form': form, 'all_elections': all_elections, 'election': current_election}
    return render(request, "Modifying/candidateadd.html", context)

@login_required
def partyadd(request, election_id=None):
    if request.method == "POST":
        form = PartyForm(request.POST, request.FILES)
        if form.is_valid():
            party = form.save(commit=False)
            party.user = request.user
            party.save()
            return redirect(request.path)
    else:
        form = PartyForm()
        
    current_election, all_elections = get_election_data(request, election_id)
    context = {'form': form, 'all_elections': all_elections, 'election': current_election}
    return render(request, "Modifying/partyadd.html", context)

@login_required
def Electionedit(request, pk):
    instance = get_object_or_404(Election, pk=pk, user=request.user)
    if request.method == "POST":
        edit = ElectionForm(request.POST, instance=instance, user=request.user)
        if edit.is_valid():
            edit.save()
            return redirect('electionlist')
    else:
        edit = ElectionForm(instance=instance, user=request.user)
    return render(request, "Modifying/electionedit.html", {'form': edit})

@login_required
def ElectionDelete(request, pk):
    instance = get_object_or_404(Election, pk=pk, user=request.user)
    instance.delete()
    return redirect('electionlist')

@login_required
def Voteredit(request, pk):
    # Ensure the voter belongs to the logged-in user
    instance = get_object_or_404(Voter, pk=pk, user=request.user)
    
    if request.method == "POST":
        # No 'user' argument needed here as VoterForm doesn't filter foreign keys
        edit = VoterForm(request.POST, request.FILES, instance=instance)
        if edit.is_valid():
            edit.save()
            return redirect('voterslist')
    else:
        edit = VoterForm(instance=instance)
        
    context = {
        'form': edit,
        'instance': instance
    }
    return render(request, "Modifying/voteredit.html", context)

@login_required
def partyedit(request, pk):
    # Ensure the party belongs to the logged-in user
    instance = get_object_or_404(Party, pk=pk, user=request.user)
    
    if request.method == "POST":
        # No 'user' argument needed here as PartyForm doesn't filter foreign keys
        edit = PartyForm(request.POST, request.FILES, instance=instance)
        if edit.is_valid():
            edit.save()
            return redirect('partyslist')
    else:
        edit = PartyForm(instance=instance)
        
    context = {
        'form': edit,
        'instance': instance
    }
    return render(request, "Modifying/partyedit.html", context)

@login_required
def voterDelete(request, pk):
    # The user=request.user filter ensures you can only delete YOUR voters
    instance = get_object_or_404(Voter, pk=pk, user=request.user)
    instance.delete()
    return redirect('voterslist')

@login_required
def partydelete(request, pk):
    # The user=request.user filter ensures you can only delete YOUR parties
    instance = get_object_or_404(Party, pk=pk, user=request.user)
    instance.delete()
    return redirect('partyslist')

@login_required
def candidateedit(request, pk):
    # Security: Ensure the candidate belongs to the logged-in user
    instance = get_object_or_404(Candidate, pk=pk, user=request.user)
    
    if request.method == "POST":
        # Pass user=request.user to the form so the Party dropdown is filtered
        edit = CandidateForm(request.POST, request.FILES, instance=instance, user=request.user)
        if edit.is_valid():
            edit.save()
            return redirect('candidateslist')
    else:
        # Pass user=request.user here too for the GET request
        edit = CandidateForm(instance=instance, user=request.user)
    
    context = {
        'form': edit,
        'instance': instance
    }
    return render(request, "Modifying/candidateedit.html", context)

@login_required
def candidateDelete(request, pk):
    # Security: Only allow deletion if the candidate belongs to the logged-in user
    instance = get_object_or_404(Candidate, pk=pk, user=request.user)
    instance.delete()
    return redirect('candidateslist')

@login_required
def votedlist(request, election_id=None):
    election = get_object_or_404(Election, id=election_id, user=request.user)
    voted_voter_ids = Vote.objects.filter(election=election).values_list('voter_id', flat=True)
    
    # Filter voters by current user
    voted_voters = Voter.objects.filter(id__in=voted_voter_ids, user=request.user)
    not_voted_voters = Voter.objects.filter(user=request.user).exclude(id__in=voted_voter_ids)
    
    current_election, all_elections = get_election_data(request, election_id)
    
    context = {
        'election': election,
        'voted_voters': voted_voters,
        'not_voted_voters': not_voted_voters,
        'all_elections': all_elections,
        'elections': current_election,
    }
    return render(request, "Modifying/voted.html", context)


def set_election(request, election_id):
    # Store the election_id in the session
    request.session['selected_election_id'] = election_id
    # Redirect back to the page the user was on
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def register(request):
    if request.method == 'POST':
        form =RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
     form = RegistrationForm()
    context ={
        'form': form,
    }
    return render(request, "register.html", context)

def login(request):
    if request.method =='POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username =form.cleaned_data['username']
            password =form.cleaned_data['password']

            user =auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('index')
        return redirect('register')
        
    form = AuthenticationForm()
    context={
        'form': form,
    }
    return render(request, "login.html", context)

def logout(request):
    auth.logout(request)
    return redirect('index')
