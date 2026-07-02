from django.shortcuts import render
from .models import Plan


def pricing_view(request):
    plans = Plan.objects.filter(is_active=True).order_by('price')
    context = {'plans': plans}
    return render(request, 'subscriptions/pricing.html', context)