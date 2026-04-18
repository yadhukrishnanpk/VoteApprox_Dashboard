from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('election/<int:election_id>/', views.index, name='index_with_id'),
    path('votelist/', views.voters_list, name='voterlist'),
    path('candidatelist/', views.candidate_list, name='candidatelist'),
    path('partylist/', views.party_list, name='partylist'),
    path('elections/', views.election_list, name='electionlist'),
    
    
    path('voters/<int:election_id>/', views.voters_list, name='voterlist'),
    path('candidates/<int:election_id>/', views.candidate_list, name='candidatelist'),
    path('parties/<int:election_id>/', views.party_list, name='partylist'),
]
