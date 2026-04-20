from django.shortcuts import render, get_object_or_404,redirect
from .models import Candidate, Vote, Voter, Party, Election
from django.db.models import Count, Q
from .forms import VotingForm,VoterForm,ElectionForm,CandidateForm,PartyForm
from django.utils import timezone
from datetime import datetime
from zoneinfo import ZoneInfo
from django.conf import settings
from .forms import RegistrationForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required


def get_election_data(election_id):
    
    all_elections = Election.objects.all()
    if election_id:
        current_election = get_object_or_404(Election, id=election_id)
    else:
        current_election = all_elections.first()
    return current_election, all_elections

def index(request, election_id=None):
    current_election, all_elections = get_election_data(election_id)
    
    # Global counts
    party_count = Party.objects.count()
    election_count = all_elections.count()
    
    if current_election:
        # 1. Get candidates specifically associated with THIS election
        data_list = current_election.candidates.annotate(
            received_votes=Count('vote', filter=Q(vote__election=current_election))
        )
        
        # 2. Total votes cast in this specific election
        total_registered_voters = Voter.objects.count()       
        candidate_count = current_election.candidates.count()

        # 3. Calculate percentage based on total votes in THIS election
        for person in data_list:
            if total_registered_voters > 0:
                # Math: (1 vote / 100 total voters) * 100 = 1.0%
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

def voters_list(request, election_id=None):
    current_election, all_elections = get_election_data(election_id)

    voters = Voter.objects.all().prefetch_related('vote_set__candidate__party')
    
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

def candidate_list(request, election_id=None):
    addcandidate=Candidate.objects.all()
    current_election, all_elections = get_election_data(election_id)
    
   
    if current_election:
        candidates = current_election.candidates.all()
    else:
        candidates = []
    
    context = {
        'all_elections': all_elections,
        'election': current_election,
        'candidate': candidates,
        'addcandidate': addcandidate
    }
    return render(request, "candidatelist.html", context)

def party_list(request, election_id=None):
    addparty=Party.objects.all()
    current_election, all_elections = get_election_data(election_id)
    
    if current_election:
      
        parties = Party.objects.filter(candidates__in=current_election.candidates.all()).distinct()
    else:
        parties = []
    
    context = {
        'all_elections': all_elections,
        'election': current_election,
        'party': parties,
        'add': addparty,
        
    }
    return render(request, "partylist.html", context)

def election_list(request):
    all_elections = Election.objects.all()
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



# MODIFYING
@staff_member_required
def vote_cast(request, election_id=None):
    if request.method == "POST":
        form = VotingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request.path) # Redirects to the same page
    else:
        form = VotingForm()
        
    current_election, all_elections = get_election_data(election_id)
    
    if current_election:
        parties = Party.objects.filter(candidates__in=current_election.candidates.all()).distinct()
    else:
        parties = []
    context = {
        'form': form,
        'all_elections': all_elections,
        'election': current_election,
        'party': parties,
    }
    return render(request, "Modifying/voting.html", context)

@staff_member_required
def Electionadd(request, election_id=None):
    if request.method == "POST":
        form = ElectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request.path) # Redirects to the same page
    else:
        form = ElectionForm()
        
    current_election, all_elections = get_election_data(election_id)
    
    if current_election:
        parties = Party.objects.filter(candidates__in=current_election.candidates.all()).distinct()
    else:
        parties = []
    context = {
        'form': form,
        'all_elections': all_elections,
        'election': current_election,
        'party': parties,
    }
    return render(request, "Modifying/electionadd.html", context)

@staff_member_required
def votersadd(request, election_id=None):
    if request.method == "POST":
        form = VoterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request.path)
    else:
        form = VoterForm()
        
    current_election, all_elections = get_election_data(election_id)
    
    if current_election:
        parties = Party.objects.filter(candidates__in=current_election.candidates.all()).distinct()
    else:
        parties = []
    context = {
        'form': form,
        'all_elections': all_elections,
        'election': current_election,
        'party': parties,
    }
    return render(request, "Modifying/votersadd.html", context)

@staff_member_required
def candidateadd(request, election_id=None):
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request.path) # Redirects to the same page
    else:
        form = CandidateForm()
        
    current_election, all_elections = get_election_data(election_id)
    
    if current_election:
        parties = Party.objects.filter(candidates__in=current_election.candidates.all()).distinct()
    else:
        parties = []
    context = {
        'form': form,
        'all_elections': all_elections,
        'election': current_election,
        'party': parties,
    }
    return render(request, "Modifying/candidateadd.html", context)

@staff_member_required
def partyadd(request, election_id=None):
    if request.method == "POST":
        form = PartyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request.path)
    
    else:
        form = PartyForm()
        
    current_election, all_elections = get_election_data(election_id)
    
    if current_election:
        parties = Party.objects.filter(candidates__in=current_election.candidates.all()).distinct()
    else:
        parties = []
    context = {
        'form': form,
        'all_elections': all_elections,
        'election': current_election,
        'party': parties,
    }
    return render(request, "Modifying/partyadd.html", context)

@staff_member_required
def Electionedit(request, pk):
    instance= get_object_or_404(Election, pk=pk)
    if request.method == "POST":
        edit=ElectionForm(request.POST, instance=instance)
        if edit.is_valid():
            edit.save()
            return redirect('electionlist')
    edit=ElectionForm(instance=instance)
    context={
        'form': edit
    }
    return render(request, "Modifying/electionedit.html", context)

@staff_member_required
def ElectionDelete(request,pk):
    instance=get_object_or_404(Election,pk=pk)
    instance.delete()
    return redirect('electionlist')

@staff_member_required
def Voteredit(request, pk):
    instance= get_object_or_404(Voter, pk=pk)
    if request.method == "POST":
        edit=VoterForm(request.POST, request.FILES, instance=instance)
        if edit.is_valid():
            edit.save()
            return redirect('voterslist')
    edit=VoterForm(instance=instance)
    context={
        'form': edit
    }
    return render(request, "Modifying/voteredit.html", context)

@staff_member_required
def voterDelete(request,pk):
    instance=get_object_or_404(Voter,pk=pk)
    instance.delete()
    return redirect('voterslist')

@staff_member_required
def candidateedit(request, pk):
    instance= get_object_or_404(Candidate, pk=pk)
    if request.method == "POST":
        edit=CandidateForm(request.POST, request.FILES, instance=instance)
        if edit.is_valid():
            edit.save()
            return redirect('candidateslist')
    edit=CandidateForm(instance=instance)
    context={
        'form': edit
    }
    return render(request, "Modifying/candidateedit.html", context)

@staff_member_required
def candidateDelete(request,pk):
    instance=get_object_or_404(Candidate,pk=pk)
    instance.delete()
    return redirect('candidateslist')


@staff_member_required
def partyedit(request, pk):
    instance= get_object_or_404(Party, pk=pk)
    if request.method == "POST":
        edit=PartyForm(request.POST, request.FILES, instance=instance)
        if edit.is_valid():
            edit.save()
            return redirect('partyslist')
    edit=PartyForm(instance=instance)
    context={
        'form': edit
    }
    return render(request, "Modifying/partyedit.html", context)

@staff_member_required
def partydelete(request,pk):
    instance=get_object_or_404(Party,pk=pk)
    instance.delete()
    return redirect('partyslist')

@staff_member_required
def votedlist(request,election_id=None):
    election = get_object_or_404(Election, id=election_id)
    
    voted_voter_ids = Vote.objects.filter(election=election).values_list('voter_id', flat=True)
    voted_voters = Voter.objects.filter(id__in=voted_voter_ids)

    not_voted_voters = Voter.objects.exclude(id__in=voted_voter_ids)
    current_election, all_elections = get_election_data(election_id)
    
    if current_election:
        parties = Party.objects.filter(candidates__in=current_election.candidates.all()).distinct()
    else:
        parties = []

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
