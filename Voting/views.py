from django.shortcuts import render, get_object_or_404,redirect
from .models import Candidate, Vote, Voter, Party, Election
from django.db.models import Count, Q
from .forms import VotingForm,VoterForm,ElectionForm,CandidateForm,PartyForm
from django.utils import timezone
from datetime import datetime
from zoneinfo import ZoneInfo
from django.conf import settings


def get_election_data(election_id):
    
    all_elections = Election.objects.all()
    if election_id:
        current_election = get_object_or_404(Election, id=election_id)
    else:
        current_election = all_elections.first()
    return current_election, all_elections

def index(request, election_id=None):
    
    
    current_election, all_elections = get_election_data(election_id)
    
    voter_count = Voter.objects.all().count
    party_count = Party.objects.all().count
    election_count = all_elections.count()
    voter=Voter.objects.count()

    if current_election:
        data_list = current_election.candidates.annotate(
            received_votes=Count('vote', filter=Q(vote__election=current_election))
        )
        total_votes_in_this_election = Vote.objects.filter(election=current_election).count()
        candidate_count = current_election.candidates.count()

        for person in data_list:
            if voter > 0:
                # Math: (1 vote / 100 total voters) * 100 = 1%
                person.vote_percentage = round(float(person.received_votes), 1)
            else:
                person.vote_percentage = 0
    else:
        data_list = []
        total_votes_in_this_election = 0
        candidate_count = 0

    context = {
        'election': current_election,
        'all_elections': all_elections,
        'data_list': data_list,
        'vote_count': total_votes_in_this_election, 
        'voter_count': voter_count,
        'party_count': party_count,
        'candidate_count': candidate_count,
        'election_count': election_count,
    }
    return render(request, "index.html", context)

def voters_list(request, election_id=None):
    current_election, all_elections = get_election_data(election_id)
    
    # Get EVERY voter in the database
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

def ElectionDelete(request,pk):
    instance=get_object_or_404(Election,pk=pk)
    instance.delete()
    return redirect('electionlist')

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

def voterDelete(request,pk):
    instance=get_object_or_404(Voter,pk=pk)
    instance.delete()
    return redirect('voterslist')


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

def candidateDelete(request,pk):
    instance=get_object_or_404(Candidate,pk=pk)
    instance.delete()
    return redirect('candidateslist')



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

def partydelete(request,pk):
    instance=get_object_or_404(Party,pk=pk)
    instance.delete()
    return redirect('partyslist')