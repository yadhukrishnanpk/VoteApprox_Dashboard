from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Party(models.Model):
    photo = models.ImageField(upload_to='candidates/%Y/%m/%d', null=True, blank=True)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural='PARTY'

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidates/%Y/%m/%d', null=True, blank=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='candidates')
    bio = models.TextField(blank=True)
    class Meta:
        verbose_name_plural='CANDIDATE'

    def __str__(self):
        return self.name

class Election(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    candidates = models.ManyToManyField(Candidate, related_name='elections')
    class Meta:
        verbose_name_plural='ELECTION'

    def __str__(self):
        return self.title
    
STATUS_CHOICES=(
    ("VOTED", "VOTED"),
    ("NOT VOTED", "NOT VOTED")
)
CHOICES=(
    ("ELIGIBLE", "ELIGIBLE"),
    ("NOT ELIGIBLE","NOT ELIGIBLE")
)
class Voter(models.Model):
    name = models.CharField(max_length=100)
    Voter_photo= models.ImageField(upload_to='uploads/%Y/%m/%d')
    voter_id = models.CharField(max_length=200, unique=True,db_index=True, help_text="Enter the unique National Voter ID number")
    dob=models.DateField(null=True,verbose_name='Date Of Birth')
    eligibility= models.CharField(max_length=20,choices=CHOICES,default="ELIGIBLE")
    vote_status=models.CharField(choices=STATUS_CHOICES,default="NOT VOTED")
    class Meta:
        verbose_name_plural='VOTER'
    def __str__(self):
        return (f"{self.name}-{self.voter_id}")
    def save(self, *args, **kwargs):
        # Rule: If a voter is switched to NOT ELIGIBLE, 
        # ensure their status reflects they can't have 'VOTED' in the future
        if self.eligibility == "NOT ELIGIBLE":
            # Optional: You could force status to NOT VOTED here if desired
            pass
        super().save(*args, **kwargs)
   
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')
        verbose_name_plural='VOTE'
        
    def __str__(self):
        return (f"{self.voter}")   
        
    def clean(self):
       
        if self.voter.eligibility == "NOT ELIGIBLE":
            raise ValidationError(f"Vote Denied: {self.voter.name} is NOT ELIGIBLE to vote.")

    def save(self, *args, **kwargs):
        # 1. Run the clean() method to check eligibility before saving
        self.full_clean() 
        
        # 2. Save the Vote
        super().save(*args, **kwargs)
        
        # 3. Update the Voter's status
        self.voter.vote_status = "VOTED"
        self.voter.save()