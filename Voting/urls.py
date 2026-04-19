from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('election/<int:election_id>/', views.index, name='index_with_id'),
    path('votelist/', views.voters_list, name='voterslist'),
    path('candidatelist/', views.candidate_list, name='candidateslist'),
    path('partylist/', views.party_list, name='partyslist'),
    path('elections/', views.election_list, name='electionlist'),
    
    
    path('voters/<int:election_id>/', views.voters_list, name='voterlist'),
    path('candidates/<int:election_id>/', views.candidate_list, name='candidatelist'),
    path('parties/<int:election_id>/', views.party_list, name='partylist'),
    
    
    #Modifying
    path('voting/', views.vote_cast, name='castlist'),
    path('ElectionAdd/', views.Electionadd, name='electionadd'),
    path('VotersAdd/', views.votersadd, name='votersadd'),
    path('CandidateAdd/', views.candidateadd, name='candidateadd'),
    path('PartyAdd/', views.partyadd, name='partyadd'),
    
    
    path('Electionedit/<int:pk>/', views.Electionedit, name='electionedit'),
    path('ElectionDelete/<int:pk>/', views.ElectionDelete, name='electiondelete'),
    
    path('voteredit/<int:pk>/', views.Voteredit, name='voteredit'),
    path('candidateDelete/<int:pk>/', views.voterDelete, name='voterdelete'),
    
    path('candidateedit/<int:pk>/', views.candidateedit, name='candidateedit'),
    path('candidatedelete/<int:pk>/', views.candidateDelete, name='candidatedelete'),
    
    path('partyedit/<int:pk>/', views.partyedit, name='partyedit'),
    path('partydelete/<int:pk>/', views.partydelete, name='partydelete'),
]

