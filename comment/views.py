from django.shortcuts import render
from about.models import AboutPost
from common.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.http.response import JsonResponse
from comment.models import Comment
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from blog.models import Post
from comment.forms import CommentForm
from django.utils.translation import gettext_lazy as _

@ajax_required
@login_required
@require_POST
def c_comment_like(request):
    comment_id = request.POST.get('id')
    action = request.POST.get('action')
    if comment_id and action:
        try:
            comment = Comment.objects.get(id=comment_id)
            if action == 'like':
                comment.users_like.add(request.user)
            else:
                comment.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def edit_comment(request, pk, aid):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(
        AboutPost,
        id=aid
    )
    form = CommentForm(
        request.POST or None,
        instance=comment
    )
    if request.user.id == comment.commentor_id:
        if request.method == 'POST':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post_id = post.id
                comment.commentor_id = request.user.id
                comment.save()
                return redirect(post.get_absolute_url())
        else:
            form = CommentForm(instance=comment)
        return render(
            request,
            'blog/comment/update.html', {
                'form': form,
                'post': post
            }
        )
    else:
        return HttpResponseRedirect(reverse('404'))


@login_required
def delete_comment(request, pk, aid):
    comment = get_object_or_404(Comment, pk=pk)
    comment.body = _('deleted')
    comment.save()
    post = get_object_or_404(
        AboutPost,
        id=aid
    )
    form = CommentForm(
        request.POST or None,
        instance=comment
    )
    if request.user.id == comment.commentor_id:
        if request.method == 'POST':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post_id = post.id
                comment.commentor_id = request.user.id
                comment.save()
                return redirect(post.get_absolute_url())
        else:
            form = CommentForm(instance=comment)
        return render(
            request,
            'blog/comment/update.html', {
                'form': form,
                'post': post
            }
        )
    else:
        return HttpResponseRedirect(reverse('404'))
