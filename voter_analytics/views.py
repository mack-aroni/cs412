from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import FilterVoterForm

# Create your views here.

class VoterListView(ListView):
    '''View to display voter results'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):

        queryset = Voter.objects.all()
        form = FilterVoterForm (self.request.GET)

        if form.is_valid():
            party = form.cleaned_data.get('party_affiliation')
            min_year = form.cleaned_data.get('min_birth_year')
            max_year = form.cleaned_data.get('max_birth_year')
            voter_score = form.cleaned_data.get('voter_score')

            if party:
                queryset = queryset.filter(party_affiliation=party)
            if min_year:
                queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
            if max_year:
                queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
            if voter_score:
                queryset = queryset.filter(voter_score=int(voter_score))

            # Election filters
            election_filters = Q()

            if form.cleaned_data.get('voted_20state'):
                election_filters |= Q(v20state__gt=0)
            if form.cleaned_data.get('voted_21town'):
                election_filters |= Q(v21town__gt=0)
            if form.cleaned_data.get('voted_21primary'):
                election_filters |= Q(v21primary__gt=0)
            if form.cleaned_data.get('voted_22general'):
                election_filters |= Q(v22general__gt=0)
            if form.cleaned_data.get('voted_23town'):
                election_filters |= Q(v23town__gt=0)

            # Apply filter only if election_filters has conditions
            if election_filters.children:  
                queryset = queryset.filter(election_filters)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FilterVoterForm(self.request.GET)
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'