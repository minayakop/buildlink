from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Property, PropertyType, City, District
from decouple import config

def home(request):
    featured    = Property.objects.filter(is_featured=True, status='available')[:6]
    latest      = Property.objects.filter(status='available')[:8]
    cities      = City.objects.all()
    for_sale    = Property.objects.filter(listing_type='sale', status='available').count()
    for_rent    = Property.objects.filter(listing_type='rent', status='available').count()

    context = {
        'featured'  : featured,
        'latest'    : latest,
        'cities'    : cities,
        'for_sale'  : for_sale,
        'for_rent'  : for_rent,
    }
    return render(request, 'properties/home.html', context)


def property_list(request):
    properties = Property.objects.filter(status='available')

    listing_type    = request.GET.get('listing_type')
    property_type   = request.GET.get('property_type')
    city_id         = request.GET.get('city')
    min_price       = request.GET.get('min_price')
    max_price       = request.GET.get('max_price')
    min_area        = request.GET.get('min_area')
    bedrooms        = request.GET.get('bedrooms')
    search          = request.GET.get('search')

    if listing_type:
        properties = properties.filter(listing_type=listing_type)
    if property_type:
        properties = properties.filter(property_type_id=property_type)
    if city_id:
        properties = properties.filter(city_id=city_id)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if min_area:
        properties = properties.filter(area__gte=min_area)
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)
    if search:
        from django.db.models import Q
        properties = properties.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(address__icontains=search)
        )

    paginator   = Paginator(properties, 12)
    page        = request.GET.get('page')
    properties  = paginator.get_page(page)

    context = {
        'properties'    : properties,
        'cities'        : City.objects.all(),
        'property_types': PropertyType.objects.all(),
        'total'         : paginator.count,
    }
    return render(request, 'properties/list.html', context)


def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    prop.views_count += 1
    prop.save()

    similar = Property.objects.filter(
        city=prop.city,
        listing_type=prop.listing_type,
        status='available'
    ).exclude(pk=pk)[:4]

    context = {
        'property'  : prop,
        'similar'   : similar,
    }
    return render(request, 'properties/detail.html', context)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PropertyForm

@login_required
def property_add(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.status = 'pending'
            prop.save()

            # حفظ الصور
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                PropertyImage.objects.create(
                    property=prop,
                    image=image,
                    is_main=(i == 0)
                )

            messages.success(request, 'تم إضافة العقار بنجاح! سيتم مراجعته قريباً.')
            return redirect('properties:detail', pk=prop.pk)
    else:
        form = PropertyForm()

    return render(request, 'properties/add.html', {'form': form})
def property_map(request):
    properties = Property.objects.filter(status='available')
    cities = City.objects.all()
    context = {
        'properties': properties,
        'cities': cities,
    }
    return render(request, 'properties/map.html', context)
from .models import Property, PropertyType, City, District, PropertyReview

def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    # زيادة عداد المشاهدات
    prop.views_count += 1
    prop.save()

    # إضافة تقييم
    if request.method == 'POST' and request.user.is_authenticated:
        rating  = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()

        if comment:
            PropertyReview.objects.update_or_create(
                property=prop,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            # تحديث متوسط التقييم
            reviews = prop.reviews.all()
            if reviews.exists():
                prop.avg_rating     = sum(r.rating for r in reviews) / reviews.count()
                prop.reviews_count  = reviews.count()
                prop.save()
            messages.success(request, 'تم إضافة تقييمك بنجاح! شكراً لك.')
            return redirect('properties:detail', pk=pk)

    reviews = prop.reviews.all().order_by('-created_at')
    similar = Property.objects.filter(
        city=prop.city,
        listing_type=prop.listing_type,
        status='available'
    ).exclude(pk=pk)[:4]

    # هل المستخدم قيّم من قبل؟
    user_review = None
    if request.user.is_authenticated:
        user_review = prop.reviews.filter(user=request.user).first()

    context = {
        'property'   : prop,
        'similar'    : similar,
        'reviews'    : reviews,
        'user_review': user_review,
    }
    return render(request, 'properties/detail.html', context)
def ai_estimator(request):
    return render(request, 'properties/ai_estimator.html')
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            import anthropic
            data = json.loads(request.body)
            messages = data.get('messages', [])

            client = anthropic.Anthropic(
                api_key=config('ANTHROPIC_API_KEY', default='')
            )

            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                system="""أنت مساعد ذكي متخصص في العقارات والبناء والتشطيبات في مصر.
مهمتك مساعدة المستخدمين في:
- تقدير تكلفة التشطيب والبناء بالجنيه المصري
- حساب كميات مواد البناء
- الإجابة على الأسئلة الهندسية
- اقتراح أفضل الخيارات حسب الميزانية
قواعد: أجب بالعربية دائماً، استخدم الجنيه المصري، قدم أرقاماً تقريبية واضحة.""",
                messages=messages
            )

            return JsonResponse({
                'success': True,
                'message': response.content[0].text
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Method not allowed'})