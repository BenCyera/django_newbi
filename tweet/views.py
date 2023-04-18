from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required


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
        my_tweet = TweetModel()
        my_tweet.author = user
        my_tweet.content = request.POST.get('my-content', '')
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
