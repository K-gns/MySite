from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from user_profile.forms import UserForm
from user_profile.models import MainCycle
import services
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    relocate, template, params = services.clicker_services.main_page(request)
    if relocate:
        return redirect(template)
    return render(request, template, params)


def user_login(request):
    relocate, template, params = services.auth_services.user_login(request)
    if relocate:
        return redirect(template)
    return render(request, template, params)

def user_logout(request):
    template = services.auth_services.user_logout(request)
    return redirect(template)


def user_registration(request):
    if request.method == "POST":
        username = request.POST["username"]
        form = UserForm(request.POST)
        existing_user = User.objects.filter(username=username)
        if len(existing_user) == 0:
            numbers = "123456789"
            uppercase = "QWERTYUIOPASDFGHJKLZXCVBNM"
            specialSymbols = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
            NoNumbers = False
            NoUppercase = False
            NoSpecial = False
            UsernameTooShort = False
            if len(username) < 4: UsernameTooShort = True #длина юзернейма
            password = request.POST["password"]
            if not [s for s in password if s in numbers]: NoNumbers = True #Проверка на содержание символов
            if not [s for s in password if s in uppercase]: NoUppercase = True
            if not [s for s in password if s in specialSymbols]: NoSpecial = True
            passwordRepeat = request.POST["passwordRepeat"]
            PasswordNotMatch = False
            if password != passwordRepeat: PasswordNotMatch = True #проверка совпадания паролей
            if PasswordNotMatch or UsernameTooShort or NoNumbers or NoUppercase or NoSpecial:
                return render(request, 'registration.html', {'passNotMatch':PasswordNotMatch, 'usernameTooShort':UsernameTooShort, 'noNumbers': NoNumbers, 'noUppercase':NoUppercase, 'noSpecial': NoSpecial})
            else:
                #user = User.objects.create_user(username, '', password)
                form.username = username
                form.password = password
                user = form.save()
                #user.save()
                maincycle = MainCycle()
                maincycle.user = user
                maincycle.save();
                user = authenticate(request, username=username, password=password)
                login(request, user)
                #return HttpResponseRedirect(request, 'index.html', {'user':user})
                return HttpResponseRedirect('../', {'user':user})
        else:
            return render(request, 'registration.html', {'alreadyTaken':True})
    else:
        return render(request, 'registration.html', {'invalid':False})
