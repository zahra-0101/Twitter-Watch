from django.shortcuts import render
from django.views.generic import View
from accounts.models import TwitterAccount

class AccountList(View):

    def get(self, request):
        context = {}

        context['accounts'] = TwitterAccount.objects.all()
        
        return render(request, 'accounts_list.html', context=context)