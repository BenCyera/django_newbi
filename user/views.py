from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
# user/views.py


# ----- submit시 에러 발생 sign_up_view -----
# 회원가입 시 빈칸으로 submit시 에러가 나는 이유. POST.get 뒤 2개의 매개변수 값 중 두 번째 값이 None이기 때문에

# def sign_up_view(request):
#     if request.method == 'GET':
#         user = request.user.is_authenticated  # 로그인 된 사용자가 요청하는지 검사
#         if user:  # 로그인이 되어있다면
#             return redirect('/')
#         else:  # 로그인이 되어있지 않다면
#             return render(request, 'user/signup.html')
#     elif request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         password2 = request.POST.get('password2', None)
#         bio = request.POST.get('bio', None)
#
#         if password != password2:
#             return render(request, 'user/signup.html')
#         else:
#             exist_user = get_user_model().objects.filter(username=username)
#             if exist_user:
#                 return render(request, 'user/signup.html')  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
#             else:
#                 UserModel.objects.create_user(username=username, password=password, bio=bio)
#                 return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동

# ----- ^ submit시 에러 발생 sign_up_view ^ -----


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 로그인 된 사용자가 요청하는지 검사
        if user:  # 로그인이 되어있다면
            return redirect('/')
        else:  # 로그인이 되어있지 않다면
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            # 패스워드가 다르다는 에러가 필요합니다. {'error':'에러문구'} 를 만들어서 전달합니다.
            return render(request, 'user/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                # 사용자 저장을 위한 username과 password가 필수라는 것을 얘기 해 줍니다.
                return render(request, 'user/signup.html', {'error': '사용자 이름과 패스워드는 필수 값 입니다'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html',
                              {'error': '사용자가 존재합니다.'})  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")

        me = auth.authenticate(request, username=username, password=password)  # 사용자 불러오기
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/')
        else:
            # html에 사용될 error값에 대한 출력 문구 처리
            return render(request, 'user/signin.html', {'error': '유저이름 혹은 패스워드를 확인 해 주세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # user_list 변수선언 = UserModel.objects를 /.all() 전부 불러와서 / exclude로 제외하기 / request.user.username을 / 즉, 본인만 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    # request.user = 현재 로그인 한 사용자.
    # 변수를 me로 선언 후 로그인 한 사용자를 넣어줌
    me = request.user
    # click_user 변수 선언, UserModel.objects에서 / 변수에 맞는 (html과 연결) / get(id=id) 특정 id를 갖고옴.
    click_user = UserModel.objects.get(id=id)
    # if me 만약 사용자(내)가 / in 선택한 유저의 팔로잉 목록에 있다면
    if me in click_user.followee.all():
        # 선택한 유저의 팔로잉 목록에서 / .remove 사용자(나)를 지워라
        click_user.followee.remove(request.user)
    # 아니라면
    else:
        # 선택한 유저의 팔로잉 목록에서 / .add 사용자(나)를 추가해라
        click_user.followee.add(request.user)
    return redirect('/user')
