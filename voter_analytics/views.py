# File: views.py
# Author: Ethan Macheder (emach@bu.edu) Apr 3, 2025
# Description: This file defines the views for the voter_analytics app.
# It handles displaying voter data, including lists, details, and visual analytics.
# The views also integrate filters for refining search results based on voter characteristics
# and election participation.

from django.shortcuts import render
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models.functions import ExtractYear

from .models import Voter
from .forms import FilterVoterForm

import plotly
import plotly.graph_objs as go
from plotly.offline import plot

# View to display a list of voters with filtering and pagination
class VoterListView(ListView):
    '''View to display voter results'''

    # Template and model configurations
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100  # Number of voters per page

    def get_queryset(self):
        '''Method to apply filters and return the filtered queryset of voters'''
        queryset = Voter.objects.all()
        form = FilterVoterForm(self.request.GET)

        if form.is_valid():
            # Extract filter data from the form
            party = form.cleaned_data.get('party_affiliation')
            min_year = form.cleaned_data.get('min_birth_year')
            max_year = form.cleaned_data.get('max_birth_year')
            voter_score = form.cleaned_data.get('voter_score')

            # Apply filters if provided
            if party:
                queryset = queryset.filter(party_affiliation=party)
            if min_year:
                queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
            if max_year:
                queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
            if voter_score:
                queryset = queryset.filter(voter_score=int(voter_score))

            # Election-related filters
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

            # Apply election filters if conditions exist
            if election_filters.children:
                queryset = queryset.filter(election_filters)

        return queryset

    def get_context_data(self, **kwargs):
        '''Method to pass the filtered queryset and form to the template'''
        context = super().get_context_data(**kwargs)
        context["form"] = FilterVoterForm(self.request.GET)
        context['voter_count'] = self.get_queryset().count()  # Total count of voters after filtering
        return context

# View to display detailed information about a single voter
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

# View to display various graphs and analytics based on filtered voter data
class GraphsView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        '''Method to generate graphs based on voter data and filters'''
        context = super().get_context_data(**kwargs)
        form = FilterVoterForm(self.request.GET)
        queryset = Voter.objects.all()  # Start with all voters

        if form.is_valid():
            # Apply filters from the form
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

            # Election-related filters
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

            # Apply election filters if conditions exist
            if election_filters.children:
                queryset = queryset.filter(election_filters)

        # Total voter count after applying filters
        total_voters = queryset.count()

        # Create a histogram of voters by year of birth
        voters_by_year = queryset.annotate(birth_year=ExtractYear('date_of_birth'))
        birth_year_counts = voters_by_year.values('birth_year').order_by('birth_year').annotate(count=Count('id'))
        fig_birth = go.Figure(data=[
            go.Bar(
                x=[b['birth_year'] for b in birth_year_counts],
                y=[b['count'] for b in birth_year_counts]
            )
        ])
        fig_birth.update_layout(
            title=f'Distribution of Voters by Year of Birth (n={total_voters})',
            xaxis_title='Year of Birth',
            yaxis_title='Number of Voters'
        )
        context['birth_year_chart'] = plot(fig_birth, output_type='div')

        # Create a pie chart of voters by party affiliation
        party_counts = queryset.values('party_affiliation').annotate(count=Count('id'))
        fig_party = go.Figure(data=[
            go.Pie(
                labels=[p['party_affiliation'].strip() for p in party_counts],
                values=[p['count'] for p in party_counts]
            )
        ])
        fig_party.update_layout(
            title=f'Distribution of Voters by Party Affiliation (n={total_voters})'
        )
        context['party_chart'] = plot(fig_party, output_type='div')

        # Create a histogram of voter participation in different elections
        elections = {
            '2020 State': 'v20state',
            '2021 Town': 'v21town',
            '2021 Primary': 'v21primary',
            '2022 General': 'v22general',
            '2023 Town': 'v23town',
        }
        participation_counts = [queryset.filter(**{f'{field}__gt': 0}).count() for field in elections.values()]
        fig_participation = go.Figure(data=[
            go.Bar(
                x=list(elections.keys()),
                y=participation_counts
            )
        ])
        fig_participation.update_layout(
            title=f'Voter Participation in Past Elections (n={total_voters})',
            xaxis_title='Election',
            yaxis_title='Number of Voters'
        )
        context['election_chart'] = plot(fig_participation, output_type='div')

        context['form'] = form  # Pass the filter form to the template
        return context
