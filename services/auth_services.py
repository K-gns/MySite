from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from user_profile.models import MainCycle
from user_profile.forms import UserForm


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return redirect('../', {'user':user})
            return (True, 'index', {'user':user})
        else:
            return (False, 'login.html', {'invalid':True})
    else:
        return (False, 'login.html', {'invalid':False})


def user_logout(request):
    logout(request)
    return ('login')


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
                return (True, 'index.html', {'user':user})
        else:
            return (False, 'registration.html', {'alreadyTaken':True})
    else:
        return (False, 'registration.html', {'invalid':False})
