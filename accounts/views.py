from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválido.', 'alert-danger')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login com sucesso!', 'alert-success')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(
            request, 'Nenhum campo pode estar vazio.', 'alert-danger')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Email inváido.', 'alert-danger')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.error(
            request, 'Senha precisa ser maior que 6 caracteres.', 
            'alert-danger')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.error(
            request, 'Usuário precisa ser maior que 6 caracteres.', 
            'alert-danger')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.error(
            request, 'Senhas não confere.', 'alert-danger')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(
            request, 'Usuário já existe.', 'alert-danger')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(
            request, 'E-mail já existe.', 'alert-danger')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Registrado com sucesso! Agora faça o login.',
                     'alert-success')

    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid:
        messages.error(request, 'Erro ao enviar formulário.', 'alert-danger')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(
            request, 'Descrição precisa term mais que 5 caracteres.', 
            'alert-danger')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, 
                     f'Contato {request.POST.get("nome")}\ salvo com sucesso.', 
                     'alert-success')
    return redirect('dashboard')
