from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count

from .models import Product, Category, Review, Comment, ProductImage


def home_view(request):
    """
    YaMe-inspired Homepage view:
    - Featured banner products
    - Flash Sale (products with discount)
    - Latest arrivals
    - Best-sellers
    - Root categories
    """
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    if not categories.exists():
        categories = Category.objects.all()

    # Flash Sale: products with sale_price
    flash_sale_products = Product.objects.filter(
        is_active=True,
        sale_price__isnull=False
    ).select_related('category').prefetch_related('images')[:8]

    # Latest products
    latest_products = Product.objects.filter(
        is_active=True
    ).select_related('category').prefetch_related('images').order_by('-created_at')[:8]

    # Best-selling products
    best_sellers = Product.objects.filter(
        is_active=True
    ).select_related('category').prefetch_related('images').order_by('-sold_count')[:8]

    # Featured reviews (5-star reviews)
    featured_reviews = Review.objects.filter(
        rating__gte=4
    ).select_related('user', 'product').order_by('-created_at')[:4]

    context = {
        'categories': categories,
        'flash_sale_products': flash_sale_products,
        'latest_products': latest_products,
        'best_sellers': best_sellers,
        'featured_reviews': featured_reviews,
    }
    return render(request, 'home.html', context)


def product_list(request, slug=None):
    """
    YaMe Product Listing & Collections view with rich filtering:
    - Category filter
    - Search keyword
    - Price range
    - Size filter
    - Color filter
    - Sorting
    - Pagination
    """
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    categories = Category.objects.all()

    current_category = None
    category_slug = slug or request.GET.get('category')
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        # Include children categories if any
        child_ids = list(current_category.children.values_list('id', flat=True))
        cat_ids = [current_category.id] + child_ids
        products = products.filter(category_id__in=cat_ids)

    # Search keyword
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(material__icontains=query)
        )

    # Price range filtering
    price_range = request.GET.get('price_range')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if price_range == 'under_200':
        products = products.filter(price__lt=200000)
    elif price_range == '200_350':
        products = products.filter(price__gte=200000, price__lte=350000)
    elif price_range == '350_500':
        products = products.filter(price__gte=350000, price__lte=500000)
    elif price_range == 'over_500':
        products = products.filter(price__gt=500000)
    else:
        if min_price:
            try:
                products = products.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                products = products.filter(price__lte=float(max_price))
            except ValueError:
                pass

    # Size filter
    selected_size = request.GET.get('size', '').strip()
    if selected_size:
        products = products.filter(sizes__icontains=selected_size)

    # Color filter
    selected_color = request.GET.get('color', '').strip()
    if selected_color:
        products = products.filter(colors__icontains=selected_color)

    # Sorting
    sort_by = request.GET.get('sort_by', 'newest')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'best_seller':
        products = products.order_by('-sold_count')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    else: # 'newest'
        products = products.order_by('-created_at')

    # Pagination (12 items per page)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Common sizes & colors for filter sidebar
    available_sizes = ['S', 'M', 'L', 'XL', 'XXL', '29', '30', '31', '32', '34']
    available_colors = [
        {'name': 'Đen', 'hex': '#111827'},
        {'name': 'Trắng', 'hex': '#FFFFFF', 'border': True},
        {'name': 'Xám', 'hex': '#9CA3AF'},
        {'name': 'Xanh Navy', 'hex': '#1E3A8A'},
        {'name': 'Be', 'hex': '#E5D0BA'},
        {'name': 'Nâu', 'hex': '#78350F'},
        {'name': 'Đỏ', 'hex': '#DC2626'},
    ]

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'current_category': current_category,
        'total_count': paginator.count,
        'query': query,
        'sort_by': sort_by,
        'price_range': price_range,
        'selected_size': selected_size,
        'selected_color': selected_color,
        'available_sizes': available_sizes,
        'available_colors': available_colors,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """
    YaMe Product Detail view:
    - Multi-image gallery
    - Size & Color options
    - Related products
    - Reviews and comment threads
    """
    # Try finding by slug or id
    product = Product.objects.filter(slug=slug, is_active=True).select_related('category').first()
    if not product and slug.isdigit():
        product = Product.objects.filter(id=int(slug), is_active=True).select_related('category').first()
    if not product:
        product = get_object_or_404(Product, slug=slug)

    images = list(product.images.all())

    # Related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).select_related('category').prefetch_related('images')[:4]

    # Split sizes & colors into list for interactive swatches
    sizes_list = [s.strip() for s in product.sizes.split(',') if s.strip()] if product.sizes else []
    colors_list = [c.strip() for c in product.colors.split(',') if c.strip()] if product.colors else []

    # Reviews and comments
    reviews = product.reviews.select_related('user').order_by('-created_at')
    comments = product.comments.filter(parent__isnull=True).select_related('user').prefetch_related('replies__user').order_by('-created_at')

    # Rating statistics
    avg_rating = product.average_rating
    total_reviews = reviews.count()

    context = {
        'product': product,
        'images': images,
        'sizes_list': sizes_list,
        'colors_list': colors_list,
        'related_products': related_products,
        'reviews': reviews,
        'comments': comments,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        content = request.POST.get("content", "").strip()

        if not rating:
            messages.error(request, "Vui lòng chọn số sao.")
            return redirect(request.META.get('HTTP_REFERER', f"/products/{product.slug}/"))

        try:
            rating = int(rating)
        except ValueError:
            messages.error(request, "Số sao không hợp lệ.")
            return redirect(request.META.get('HTTP_REFERER', f"/products/{product.slug}/"))

        if rating < 1 or rating > 5:
            messages.error(request, "Số sao phải từ 1 đến 5.")
            return redirect(request.META.get('HTTP_REFERER', f"/products/{product.slug}/"))

        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                "rating": rating,
                "content": content,
            }
        )

        messages.success(
            request,
            "Cảm ơn bạn! Đã ghi nhận đánh giá sản phẩm."
        )

    return redirect(request.META.get('HTTP_REFERER', f"/products/{product.slug}/"))


@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        parent_id = request.POST.get("parent_id")

        if not content:
            messages.error(
                request,
                "Nội dung bình luận không được để trống."
            )
            return redirect(request.META.get('HTTP_REFERER', f"/products/{product.slug}/"))

        parent = None
        if parent_id:
            parent = get_object_or_404(
                Comment,
                id=parent_id,
                product=product
            )

        Comment.objects.create(
            product=product,
            user=request.user,
            parent=parent,
            content=content
        )

        messages.success(
            request,
            "Đã đăng bình luận thành công."
        )

    return redirect(request.META.get('HTTP_REFERER', f"/products/{product.slug}/"))
