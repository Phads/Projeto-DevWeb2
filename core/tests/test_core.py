import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from core.forms import UserRegistrationForm

@pytest.mark.django_db
def test_registro_view_get_exibe_formulario():
    client = Client()
    url = reverse("core:registro")
    
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context  # Confirma que o formulário foi passado ao template
    assert b"<form" in response.content  # Confirma que o HTML contém um <form>

@pytest.mark.django_db
def test_registro_usuario_com_dados_validos(client):
    url = reverse("core:registro")
    data = {
        "username": "usuario_teste",
        "first_name": "João",
        "email": "teste@email.com",
        "password": "senha1234",
        "password2": "senha1234",
    }
    response = client.post(url, data)

    # Verifica se houve redirecionamento
    assert response.status_code == 302

    # Verifica se o usuário foi criado
    assert User.objects.filter(username="usuario_teste").exists()

@pytest.mark.django_db
def test_registro_usuario_com_username_invalido():
    client = Client()
    url = reverse("core:registro")
    data = {
        "username": "", # Campo obrigatório username em branco (inválido)
        "first_name": "João",
        "email": "teste@email.com",
        "password": "senha1234",
        "password2": "senha1234",
    }
    response = client.post(url, data)

    assert response.status_code == 200  # Formulário deve ser recarregado
    assert b'form' in response.content  # Deve conter o formulário
    assert not User.objects.exists()

@pytest.mark.django_db
def test_registro_usuario_com_email_invalido():
    client = Client()
    url = reverse("core:registro")
    data = {
        "username": "usuario_teste", 
        "first_name": "João",
        "email": "xxxxx", # Campo email inválido
        "password": "senha1234",
        "password2": "senha1234",
    }
    response = client.post(url, data)

    assert response.status_code == 200  # Formulário deve ser recarregado
    assert b'form' in response.content  # Deve conter o formulário
    assert not User.objects.exists()

@pytest.mark.django_db
def test_registro_usuario_com_senhas_diferentes():
    client = Client()
    url = reverse("core:registro")
    data = {
        "username": "usuario_teste", 
        "first_name": "João",
        "email": "teste@email.com", 
        "password": "senha12345", 
        "password2": "senha1234", # senha diferente
    }
    response = client.post(url, data)

    assert response.status_code == 200  # Formulário deve ser recarregado
    assert b'form' in response.content  # Deve conter o formulário
    assert not User.objects.exists()

@pytest.mark.django_db
def test_clean_email_ja_existente():
    # Cria um usuário com um e-mail já existente
    User.objects.create_user(
        username="existente",
        password="senha123",
        email="email@teste.com"
    )

    # Tenta registrar outro usuário com o mesmo e-mail
    form_data = {
        "username": "novo_usuario",
        "first_name": "João",
        "email": "email@teste.com",  # Mesmo e-mail
        "password": "senha123",
        "password2": "senha123",
    }
    
    form = UserRegistrationForm(data=form_data)

    # O formulário deve ser inválido e conter erro no campo "email"
    assert not form.is_valid()
    assert "email" in form.errors
    assert form.errors["email"] == ["Este e-mail já está em uso. Escolha outro."]



@pytest.mark.django_db
def test_user_update_view_get(client, django_user_model):
    user = django_user_model.objects.create_user(
        username='teste', password='senha123', email='teste@email.com'
    )
    client.login(username='teste', password='senha123')

    url = reverse('core:editar_perfil')
    response = client.get(url)

    assert response.status_code == 200
    assert b'Editar' in response.content

@pytest.mark.django_db
def test_user_update_view_post(client, django_user_model):
    user = django_user_model.objects.create_user(username='teste', password='123456', email='a@a.com')
    client.login(username='teste', password='123456')

    url = reverse('core:editar_perfil')
    data = {
        'username': 'novo_nome',
        'first_name': 'Novo',
        'email': 'novo@email.com',
    }
    response = client.post(url, data)

    user.refresh_from_db()
    assert user.username == 'novo_nome'
    assert user.first_name == 'Novo'
    assert user.email == 'novo@email.com'
    assert response.status_code == 302
    assert response.url == reverse('home')
