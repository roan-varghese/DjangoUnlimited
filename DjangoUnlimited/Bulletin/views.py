from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .forms import PostForm
from .models import Post

from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers

from django.core.paginator import Paginator


# The bulletin view for each individual
class BulletinView(TemplateView):
    template_name = 'bulletin/base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, args)


# Create the new bulletin posts
class CreatePostView(TemplateView):
    template_name = 'bulletin/base.html'

    def get(self, request, *args, **kwargs):
        form = PostForm()
        # Get the drafts of each user
        posts = Post.objects.filter(status=False, author_id=request.user.id)
        # Paginate the draft posts, 5 per page
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')  # < Get the page number
        posts = paginator.get_page(page)  #
        args = {'form': form, 'posts': posts}
        return render(request, self.template_name, args)

    # Save newly created post information to database
    def post(self, request):
        if request.method == "POST":
            form = PostForm(request.POST)
            # check if post is submitted
            if request.POST.get("submitbutton"):
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.author_updated = request.user
                    post.release_date = timezone.now()
                    post.update_date = timezone.now()
                    post.status = True  # post is published for everyone to view
                    post.save()
                    return redirect('post_new')
            # check if post is saved in draft mode
            elif request.POST.get("savebutton"):
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.author_updated = request.user
                    post.release_date = timezone.now()
                    post.update_date = timezone.now()
                    post.status = False  # post is in draft mode
                    post.save()
                    return redirect('post_new')


# Edit previously published bulletin posts
class EditBulletin(TemplateView):
    template_name = 'bulletin/post_edit.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=int(kwargs['pk']))  # get the post with that particular chosen ID
        pk = int(kwargs['pk'])
        posts = Post.objects.filter(status=False, author_id=request.user.id).exclude(id=pk)
        # Paginate the draft posts, 5 per page
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')  # < Get the page number
        posts = paginator.get_page(page)  #
        form = PostForm(instance=post)
        args = {'form': form, 'posts': posts}
        return render(request, self.template_name, args)

    # Edit post information and save changes to database
    def post(self, request, **kwargs):
        post = get_object_or_404(Post, pk=int(kwargs['pk']))
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            # submit the edited post
            if request.POST.get("submitbutton"):
                if form.is_valid():
                    if post.status:
                        post = form.save(commit=False)
                        post.author_updated = request.user
                        post.update_date = timezone.now()
                        post.status = True  # edited post is now published
                        post.save()
                        return redirect('post_new')
                    else:
                        post = form.save(commit=False)
                        post.author_updated = request.user
                        post.release_date = timezone.now()
                        post.update_date = timezone.now()
                        post.status = True  # edited post is now published
                        post.save()
                        return redirect('post_new')
            # check if post is saved in draft mode
            elif request.POST.get("savebutton"):
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author_updated = request.user
                    post.release_date = timezone.now()
                    post.update_date = timezone.now()
                    post.status = False
                    post.save()
                    return redirect('post_new')


# view the details of each published and created post
def PostDetailView(request, pk):
    context = {}

    if request.method == 'POST' and request.is_ajax():
        post_id = request.POST.get('post_id')
        print(post_id)

        post = Post.objects.get(pk=post_id)
        serialized_post = serializers.serialize('json', [post])
        return JsonResponse({'post': serialized_post}, safe=False)


def AllPosts(request):
    posts = Post.objects.filter(status=True)
    args = {'posts': posts}
    return render(request, 'bulletin/allPosts.html', args)

