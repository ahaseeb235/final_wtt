# noticeboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def post_list(request):
    all_posts = Post.objects.all().order_by('-date_posted')

    # Pagination logic
    paginator = Paginator(all_posts, 3)  # Show 3 posts per page
    page = request.GET.get('page', 1)  # Get the current page number from the request

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        posts = paginator.page(paginator.num_pages)

    # Pass the posts to the template
    context = {
        'posts': posts,
    }
    return render(request, 'noticeboard/post_list.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('noticeboard:post_detail', pk=post.pk)  # Include the namespace
    else:
        form = PostForm()
    return render(request, 'noticeboard/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'noticeboard/post_detail.html', {'post': post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user and request.user.user_profile.position not in ["Manager", "System Admin"]:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('noticeboard:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('noticeboard:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'noticeboard/post_form.html', {'form': form, 'title': 'Edit Post'})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('noticeboard:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('noticeboard:post_list')
    return render(request, 'noticeboard/post_confirm_delete.html', {'post': post})

