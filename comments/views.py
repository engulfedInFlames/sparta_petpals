from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CommentModel
from .forms import CommentForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from posts.views import post_detail

# Create your views here.
# /post/<int:post_id>/detail < 글 상세보기 경로


@login_required
@csrf_exempt
def comment_view(request):
    if request.method == "GET":  # -> posts쪽에 병합하는것으로
        # 게시글 내용이 뜰때 같이 가져옴
        # 여기 경로 이름 확인해야함
        all_comments = CommentModel()
        if not all_comments:
            message = "아직 댓글이 없습니다."
            return {"error_message": message}
        elif all_comments:
            return render(
                request, "post/<int:post_id>/detail", {"comments": all_comments}
            )
    else:
        raise NotImplementedError()


def comment_post(request):
    if request.method == "POST":
        # 코멘트 쓰기, 업로드
        write_comments = CommentForm(request.POST)

        if not write_comments.content:
            # 댓글 내용이 없을 경우
            # 가능하다면 html에 {{error_message}} 띄워주기
            message = "댓글 내용을 적어주세요"
            return render(
                request, "comments/comment_create.html", {"error_message": message}
            )
            # commnet/note.html 넣어주기

        elif write_comments.is_valid():
            write_comments.save()
            return redirect("/post/<int:post_id>/detail")
    else:
        return HttpResponse("댓글 포스트에 실패하였습니다")


def comment_delete_post(request):
    comment = CommentModel.objects.get(id=id)
    comment.delete
    return redirect("/post/<int:post_id>/detail")


def my_comment_view(request, cmt_page=1):
    if request.method == "GET":
        # 내 댓글 불러오기, author정보기반
        author = CommentModel.author
        my_comment = CommentModel.objects.all(author=author).order_by("-created")

        comment_title = "내 댓글 목록"

        paginator = Paginator(my_comment, 10)
        cmt_page = request.GET.get("page")
        cmt_page_obj = paginator.page(cmt_page)

        # return HttpResponse ('[%s]' % commnet_title)
        return render_to_response(
            "comments/comment_mycmt.html",
            {"my_comment": my_comment, "cmt_page_obj": cmt_page_obj},
        )
