from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from .models import Space, SpaceImage, SpaceType, City
from .forms import SpaceForm, SpaceImageForm


def space_list(request):
    spaces = Space.objects.filter(status='available').select_related('owner').prefetch_related('images')

    # Search with Q objects (OR across title, description, address)
    query = request.GET.get('q', '')
    if query:
        spaces = spaces.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )

    # Filters
    space_type = request.GET.get('type', '')
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if space_type:
        spaces = spaces.filter(space_type=space_type)
    if city:
        spaces = spaces.filter(city=city)
    if min_price:
        spaces = spaces.filter(price_per_day__gte=min_price)
    if max_price:
        spaces = spaces.filter(price_per_day__lte=max_price)

    # Annotate with average rating
    spaces = spaces.annotate(avg_rating=Avg('reviews__rating'), review_count=Count('reviews'))

    # Pagination
    paginator = Paginator(spaces, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'space_types': SpaceType.choices,
        'cities': City.choices,
        'selected_type': space_type,
        'selected_city': city,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'spaces/list.html', context)


def space_detail(request, pk):
    space = get_object_or_404(
        Space.objects.select_related('owner').prefetch_related('images', 'reviews__user'),
        pk=pk
    )
    user_review = None
    if request.user.is_authenticated:
        user_review = space.reviews.filter(user=request.user).first()

    context = {
        'space': space,
        'user_review': user_review,
        'avg_rating': space.average_rating(),
    }
    return render(request, 'spaces/detail.html', context)


@login_required
def space_add(request):
    if not request.user.profile.is_owner():
        messages.error(request, 'فقط أصحاب المساحات يمكنهم إضافة مساحات.')
        return redirect('spaces:list')

    if request.method == 'POST':
        form = SpaceForm(request.POST)
        image_form = SpaceImageForm(request.POST, request.FILES)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            if image_form.is_valid() and request.FILES.get('image'):
                img = image_form.save(commit=False)
                img.space = space
                img.is_main = True
                img.save()
            messages.success(request, 'تمت إضافة المساحة بنجاح.')
            return redirect('spaces:detail', pk=space.pk)
    else:
        form = SpaceForm()
        image_form = SpaceImageForm()

    return render(request, 'spaces/add.html', {'form': form, 'image_form': image_form})


@login_required
def space_edit(request, pk):
    space = get_object_or_404(Space, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = SpaceForm(request.POST, instance=space)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المساحة بنجاح.')
            return redirect('spaces:detail', pk=space.pk)
    else:
        form = SpaceForm(instance=space)

    return render(request, 'spaces/edit.html', {'form': form, 'space': space})


@login_required
def space_delete(request, pk):
    space = get_object_or_404(Space, pk=pk, owner=request.user)
    if request.method == 'POST':
        space.delete()
        messages.success(request, 'تم حذف المساحة بنجاح.')
        return redirect('accounts:dashboard')
    return render(request, 'spaces/confirm_delete.html', {'space': space})


@login_required
def space_add_image(request, pk):
    space = get_object_or_404(Space, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = SpaceImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.space = space
            img.save()
            messages.success(request, 'تمت إضافة الصورة.')
            return redirect('spaces:detail', pk=space.pk)
    else:
        form = SpaceImageForm()
    return render(request, 'spaces/add_image.html', {'form': form, 'space': space})
