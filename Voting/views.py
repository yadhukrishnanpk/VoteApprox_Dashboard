from django.shortcuts import render
from .models import Candidate,Vote,Voter,Party,Election
from django.db.models import Count


def index(request):
    
    candidate_count = Candidate.objects.count()
    voter_count = Voter.objects.count()
    party_count = Party.objects.count()
    election_count = Election.objects.count()
    candidates_list = Candidate.objects.annotate(received_votes=Count('vote', distinct=True))
    total_votes_cast = sum(c.received_votes for c in candidates_list)

    for person in candidates_list:
        if total_votes_cast > 0:
            # Math: (1 / 100) * 100 = 1%
            person.vote_percentage = (float(person.received_votes) / float(total_votes_cast)) * 100
        else:
            person.vote_percentage = 0
    context = {
        'candidate_count': candidate_count,
        'vote_count': total_votes_cast, 
        'voter_count': voter_count,
        'party_count': party_count,
        'election_count': election_count,
        'total_votes': total_votes_cast,
        'vote_count': Vote.objects.count(),
        'data_list': candidates_list, 
    }
    return render(request, "index.html", context)

def voters_list(request):
    VoterS =Voter.objects.all()
    voters = Voter.objects.prefetch_related('vote_set__candidate__party').all()
    for voter in voters:
        vote_record = voter.vote_set.first()
        if vote_record:
            voter.voted_for_party = vote_record.candidate.party.name
            voter.voted_for_candidate = vote_record.candidate.name
        else:
            voter.voted_for_party = "N/A"
            voter.voted_for_candidate = "N/A"
    
    context={
        'datas': VoterS,
        'voters': voters
        
    }
    return render(request, "voter_list.html",context)


def candidate_list(request):
    
    candidate=Candidate.objects.all()
    
    context={
        'candidate': candidate
    }
    
    return render(request, "candidatelist.html", context)

def party_list(request):
    
    party=Party.objects.all()
    
    context={
        'party': party
    }
    
    return render(request, "partylist.html", context)
