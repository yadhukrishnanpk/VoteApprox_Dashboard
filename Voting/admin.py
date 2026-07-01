from django.contrib import admin
from django.utils.html import format_html
from .models import Party, Candidate, Election, Voter, Vote

admin.site.site_header = "VoteApprox Administration Control"
admin.site.site_title = "VoteApprox Portal"
admin.site.index_title = "Election Database Management System"


class CandidateInline(admin.TabularInline):
    """Allows adding/editing candidates quickly right inside the Party screen."""
    model = Candidate
    extra = 1
    fields = ('name', 'bio', 'photo')


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('get_photo', 'name', 'abbreviation', 'user')
    list_display_links = ('name',)
    search_fields = ('name', 'abbreviation')
    list_filter = ('user',)
    inlines = [CandidateInline]

    def get_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover;" />', obj.photo.url)
        return "No Image"
    get_photo.short_description = 'Logo'


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('get_photo', 'name', 'party', 'bio', 'user')
    list_display_links = ('name',)
    search_fields = ('name', 'bio')
    list_filter = ('party', 'user')

    def get_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return "No Photo"
    get_photo.short_description = 'Photo'


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'start_time', 'end_time', 'user')
    search_fields = ('title',)
    list_filter = ('start_date', 'end_date', 'user')
    filter_horizontal = ('candidates',) 


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('get_photo', 'name', 'voter_id', 'dob', 'get_eligibility_badge', 'get_vote_status_badge', 'user')
    list_display_links = ('name', 'voter_id')
    search_fields = ('name', 'voter_id')
    list_filter = ('eligibility', 'vote_status', 'user')
    readonly_fields = ('eligibility',) 
    
    def get_photo(self, obj):
        if obj.voter_photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover;" />', obj.voter_photo.url)
        return "❌ Missing"
    get_photo.short_description = 'Avatar'

    def get_eligibility_badge(self, obj):
        if obj.eligibility == "ELIGIBLE":
            return format_html('<span style="background-color: #d4edda; color: #155724; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">ELIGIBLE</span>')
        return format_html('<span style="background-color: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">NOT ELIGIBLE</span>')
    get_eligibility_badge.short_description = 'Eligibility'

    def get_vote_status_badge(self, obj):
        if obj.vote_status == "VOTED":
            return format_html('<span style="background-color: #cce5ff; color: #004085; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">VOTED</span>')
        return format_html('<span style="background-color: #fff3cd; color: #856404; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">NOT VOTED</span>')
    get_vote_status_badge.short_description = 'Activity'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'election', 'candidate', 'timestamp')
    search_fields = ('voter__name', 'voter__voter_id', 'election__title', 'candidate__name')
    list_filter = ('election', 'candidate', 'timestamp')

    def has_change_permission(self, request, obj=None):
        return False