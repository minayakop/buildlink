from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service, ServiceCategory, ServiceImage, ServiceReview


def service_list(request):
    services = Service.objects.filter(status='active')

    category_id = request.GET.get('category')
    city        = request.GET.get('city')
    search      = request.GET.get('search')

    if category_id:
        services = services.filter(category_id=category_id)
    if city:
        services = services.filter(city__icontains=city)
    if search:
        services = services.filter(name__icontains=search) | \
                   services.filter(description__icontains=search)

    context = {
        'services'   : services,
        'categories' : ServiceCategory.objects.all(),
        'total'      : services.count(),
    }
    return render(request, 'services/list.html', context)


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    reviews = service.reviews.all().order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        rating  = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        if comment:
            ServiceReview.objects.update_or_create(
                service=service,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            # تحديث متوسط التقييم
            avg = service.reviews.all()
            if avg.exists():
                service.rating = sum(r.rating for r in avg) / avg.count()
                service.reviews_count = avg.count()
                service.save()
            messages.success(request, 'تم إضافة تقييمك بنجاح!')
            return redirect('services:detail', pk=pk)

    context = {
        'service': service,
        'reviews': reviews,
    }
    return render(request, 'services/detail.html', context)


@login_required
def service_add(request):
    if request.method == 'POST':
        service = Service.objects.create(
            owner           = request.user,
            category_id     = request.POST.get('category'),
            name            = request.POST.get('name'),
            description     = request.POST.get('description'),
            city            = request.POST.get('city'),
            address         = request.POST.get('address', ''),
            phone           = request.POST.get('phone'),
            whatsapp        = request.POST.get('whatsapp', ''),
            email           = request.POST.get('email', ''),
            min_price       = request.POST.get('min_price') or None,
            max_price       = request.POST.get('max_price') or None,
            experience_years= request.POST.get('experience_years', 0),
            status          = 'pending',
        )
        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            ServiceImage.objects.create(
                service=service,
                image=image,
                is_main=(i == 0)
            )
        messages.success(request, 'تم إضافة خدمتك بنجاح! سيتم مراجعتها قريباً.')
        return redirect('services:detail', pk=service.pk)

    context = {'categories': ServiceCategory.objects.all()}
    return render(request, 'services/add.html', context)