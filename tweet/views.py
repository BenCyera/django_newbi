from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content', '')  # 글 작성이 되지 않았다면 빈칸으로
        tags = request.POST.get('tag', '').split(',')

        if content == '':  # 글이 빈칸이면 기존 tweet과 에러를 같이 출력
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)  # 글 저장을 한번에!
            for tag in tags:
                tag = tag.strip()
                if tag != '':  # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')


def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


def detail_tweet(request, id):
    if request.method == 'GET':
        this_tweet = TweetModel.objects.get(id=id)
        comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
        return render(request, 'tweet/tweet_detail.html', {'tweet': this_tweet, 'comment': comment})


def write_comment(request, id):
    if request.method == 'POST':
        this_tweet = TweetModel.objects.get(id=id)

        my_comment = TweetComment()
        my_comment.tweet = this_tweet
        my_comment.author = request.user
        my_comment.comment = request.POST.get('comment', '')
        my_comment.save()

        return redirect('/tweet/' + str(id))


def delete_comment(request, id):
    my_comment = TweetComment.objects.get(id=id)
    in_tweet = my_comment.tweet.id
    my_comment.delete()
    return redirect('/tweet/' + str(in_tweet))


# ----- v django-taggit 모듈에서 정해놓은 규칙 v -----


# TagCloudTV 클래스 = 태그들을 모아놓은 태그클라우드
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


# TaggedObjectLV 클래스 = 태그들을 모아서 화면에 전달
class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
