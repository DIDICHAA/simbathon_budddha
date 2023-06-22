from django.shortcuts import render, redirect, get_object_or_404
from .models import Qna, QnaComment
from django.utils import timezone

# Create your views here.
def create(request):
    if request.user.is_authenticated:
        new_qna = Qna()
        new_qna.title = request.POST['title']
        new_qna.writer = request.user
        new_qna.pub_date = timezone.now()
        new_qna.body = request.POST['body']
        new_qna.save()
        return redirect('qnapage:qnalistrecent')
    else:
        return redirect('accounts:login')

def new(request):
    return render(request, 'qnapage/newqna.html')

def qnalistrecent(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        qnas = Qna.objects.all()
        return render(request, 'qnapage/qnalistrecent.html', {'qnas':qnas})

def qnalistpop(request):
    qnas = Qna.objects.all()
    return render(request, 'qnapage/qnalistpop.html', {'qnas':qnas})

def qnadetail(request, id):
    qna = get_object_or_404(Qna, pk = id)
    if request.method == 'GET':
        comments = QnaComment.objects.filter(qna = qna)
        return render(request, 'qnapage/qnadetail.html',{
            'qna':qna,
            'comments':comments
            })
    elif request.method == "POST":
        new_comment = QnaComment()
        # foreignkey > blog 객체 직접 넣어주기
        new_comment.qna = qna
        # foreignkey > request.user 객체 직접 넣어주기
        new_comment.content = request.POST['content']
        new_comment.writer = request.user
        new_comment.pub_date = timezone.now()
        new_comment.save()
        return redirect('qnapage:qnadetail', id)
    return render(request, 'qnapage/qnadetail.html', {'qna':qna})

def comment_likes(request, comment_id):
    qnacomment = get_object_or_404(QnaComment, id=comment_id)
    if request.user in qnacomment.comment_like.all():
        qnacomment.comment_like.remove(request.user)
        qnacomment.comment_like_count -= 1
        qnacomment.save()
    else:
        qnacomment.comment_like.add(request.user)
        qnacomment.comment_like_count += 1
        qnacomment.save()
    return redirect('qnapage:qnadetail', qnacomment.qna.id)

def comment_edit(request, comment_id):
    comment = get_object_or_404(QnaComment, id=comment_id)
    return render(request, 'qnapage/commentupdate.html', {'comment':comment})

def comment_update(request, comment_id):
    if request.user.is_authenticated:
        update_comment = QnaComment.objects.get(id=id)
        if request.user == update_comment.writer:
            update_comment.content = request.POST['content']
            update_comment.pub_date = timezone.now()
            update_comment.save()
            return redirect('main:detail', update_comment.id)
    return redirect('accounts:login')

def comment_delete(request, comment_id):
    comment = get_object_or_404(QnaComment, id=comment_id)
    qna_id = comment.qna.id
    comment.delete()
    return redirect('qnapage:qnadetail', qna_id)