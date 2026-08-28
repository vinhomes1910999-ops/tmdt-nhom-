from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Product, Review, Comment


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        content = request.POST.get("content", "").strip()

        if not rating:
            messages.error(request, "Vui lòng chọn số sao.")
            return redirect("/")

        try:
            rating = int(rating)
        except ValueError:
            messages.error(request, "Số sao không hợp lệ.")
            return redirect("/")

        if rating < 1 or rating > 5:
            messages.error(request, "Số sao phải từ 1 đến 5.")
            return redirect("/")

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
            "Đã thêm/cập nhật đánh giá sản phẩm."
        )

    return redirect("/")


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
            return redirect("/")

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
            "Đã thêm bình luận."
        )

    return redirect("/")
