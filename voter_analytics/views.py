from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class ResultView(View):
    '''View to display voter results'''

    template_name = 'voter_analytics/base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)