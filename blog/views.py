from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('id')
        return render(request, 'blog/index.html', {
            'post_data': post_data
        })

class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'blog/post_detail.html', {
            'post_data': post_data
        })

class CreatePostView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'blog/post_form.html', {
            'form': form
        })
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', post_data.id)
        return render(request, 'blog/post_form.html', {
            'form': form
        })