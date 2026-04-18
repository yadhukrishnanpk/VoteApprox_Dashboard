from django.shortcuts import render, get_object_or_404
from .models import Candidate, Vote, Voter, Party, Election
from django.db.models import Count, Q

# Helper function to avoid repeating code in every view
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
        # Look for a vote record specifically for THIS election
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
    
    # Filter: Only show candidates registered for this election
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
        # Change 'candidate' to 'candidates'
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
    # For the general list, we don't necessarily need a "current" election filter
    context = {
        'all_elections': all_elections,
        'elections': all_elections, 
    }
    return render(request, "electionlist.html", context)