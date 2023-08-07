from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm

from pybo.pcwk_logging import logger2 as plog  # logger

# Create your views here.


def signup(request):
    """
    회원가입
    """

    # POST(회원가입) / GET(회원가입 signup.html)

    plog.debug('1. request.method : ', request.method)

    if 'POST' == request.method:
        plog.debug('2. POST')
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            plog.debug('3. username : {}'.format(username))
            plog.debug('4. password1 : {}'.format(password1))

            user = authenticate(username=username, password=password1)
            plog.debug('5. user : {}'.format(user))
            login(request, user)
            return redirect('index')

    else:
        plog.debug('2. GET')
        form = UserForm()

    return render(request, 'common/signup.html', {'form': form})

