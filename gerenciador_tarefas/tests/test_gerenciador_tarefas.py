# gerenciador_tarefas/tests/test_tarefas.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client # Já está sendo importado em seus testes 'core'
from datetime import date, timedelta

# Importe os modelos e formulários do seu app gerenciador_tarefas
from gerenciador_tarefas.models import Tarefa, Comentario
from gerenciador_tarefas.forms import TarefaForm, ComentarioForm


# --- Fixtures úteis para os testes ---

@pytest.fixture
def create_user():
    """Fixture para criar um usuário de teste."""
    def _create_user(username="testuser", password="testpassword", email="test@example.com"):
        return User.objects.create_user(username=username, password=password, email=email)
    return _create_user

@pytest.fixture
def auth_client(client, create_user):
    """Fixture para um cliente autenticado."""
    user = create_user()
    client.login(username=user.username, password="testpassword")
    return client, user # Retorna o cliente e o usuário logado

@pytest.fixture
def create_tarefa(create_user):
    """Fixture para criar uma tarefa para um usuário específico."""
    def _create_tarefa(user, titulo="Tarefa de Teste", descricao="Descrição da tarefa", data_entrega=None):
        if data_entrega is None:
            data_entrega = date.today() + timedelta(days=10) # Data futura padrão
        return Tarefa.objects.create(
            usuario=user,
            titulo=titulo,
            descricao=descricao,
            data_entrega=data_entrega,
            email=user.email, # O campo email é obrigatório no seu modelo
        )
    return _create_tarefa

# --- Testes para TarefaCreateView (Cadastro de Tarefas) ---

@pytest.mark.django_db
def test_tarefa_create_view_get_exibe_formulario(auth_client):
    """Verifica se a página de criação de tarefas exibe o formulário corretamente."""
    client, _ = auth_client
    url = reverse("tarefa_form") # Sua URL é 'tarefa_form'
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert isinstance(response.context["form"], TarefaForm)
    assert b"<form" in response.content

@pytest.mark.django_db
def test_tarefa_create_view_post_dados_validos(auth_client):
    """Verifica o cadastro bem-sucedido de uma nova tarefa com dados válidos."""
    client, user = auth_client
    url = reverse("tarefa_form")
    data_entrega_futura = date.today() + timedelta(days=7)
    
    data = {
        "titulo": "Comprar pão",
        "data_entrega": data_entrega_futura.strftime("%Y-%m-%d"),
        "descricao": "Pão francês integral",
    }
    
    response = client.post(url, data, follow=True) # follow=True para seguir o redirecionamento

    # Verifica redirecionamento para a 'home' (sucesso_url)
    assert response.status_code == 200 # Após redirecionamento
    assert response.request["PATH_INFO"] == reverse("home")

    # Verifica se a tarefa foi criada no banco de dados
    assert Tarefa.objects.count() == 1
    tarefa_criada = Tarefa.objects.first()

    assert tarefa_criada.titulo == "Comprar pão"
    assert tarefa_criada.descricao == "Pão francês integral"
    assert tarefa_criada.data_entrega == data_entrega_futura
    assert tarefa_criada.usuario == user
    assert tarefa_criada.email == user.email # Verifica o campo email, que é preenchido na view

    # Verifica se a tarefa é exibida na página 'home' (lista de tarefas)
    assert b"Comprar p\xc3\xa3o" in response.content # Conteúdo decodificado para UTF-8

@pytest.mark.django_db
def test_tarefa_create_view_post_titulo_vazio(auth_client):
    """Verifica falha ao tentar criar tarefa com título vazio."""
    client, _ = auth_client
    url = reverse("tarefa_form")
    data_entrega_futura = date.today() + timedelta(days=7)
    
    data = {
        "titulo": "", # Título vazio
        "data_entrega": data_entrega_futura.strftime("%Y-%m-%d"),
        "descricao": "Alguma descrição",
    }
    
    response = client.post(url, data)

    assert response.status_code == 200 # Deve permanecer na mesma página com erros
    assert b"Este campo \xc3\xa9 obrigat\xc3\xb3rio." in response.content # Erro de campo obrigatório
    assert Tarefa.objects.count() == 0 # Nenhuma tarefa deve ser criada

@pytest.mark.django_db
def test_tarefa_create_view_post_data_entrega_passada(auth_client):
    """Verifica falha ao tentar criar tarefa com data de entrega no passado."""
    client, _ = auth_client
    url = reverse("tarefa_form")
    data_entrega_passada = date.today() - timedelta(days=1)
    
    data = {
        "titulo": "Tarefa no Passado",
        "data_entrega": data_entrega_passada.strftime("%Y-%m-%d"),
        "descricao": "Descrição antiga",
    }
    
    response = client.post(url, data)

    assert response.status_code == 200 # Deve permanecer na mesma página com erros
    assert b"A data de entrega n\xc3\xa3o pode ser anterior \xc3\xa0 data de hoje." in response.content
    assert Tarefa.objects.count() == 0 # Nenhuma tarefa deve ser criada

# --- Testes para TarefaUpdateView (Atualização de Tarefas) ---

@pytest.mark.django_db
def test_tarefa_update_view_get_exibe_formulario_pre_preenchido(auth_client, create_tarefa):
    """Verifica se a página de edição exibe o formulário pré-preenchido com os dados da tarefa."""
    client, user = auth_client
    tarefa = create_tarefa(user=user) # Cria uma tarefa para o usuário logado

    url = reverse("tarefa_uptade", args=[tarefa.pk])
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert isinstance(response.context["form"], TarefaForm)
    assert b'value="Tarefa de Teste"' in response.content # Verifica se o título está no formulário

@pytest.mark.django_db
def test_tarefa_update_view_post_dados_validos(auth_client, create_tarefa):
    """Verifica a atualização bem-sucedida de uma tarefa com dados válidos."""
    client, user = auth_client
    tarefa = create_tarefa(user=user)

    url = reverse("tarefa_uptade", args=[tarefa.pk])
    nova_data_entrega = date.today() + timedelta(days=20)
    
    data = {
        "titulo": "Título Atualizado",
        "data_entrega": nova_data_entrega.strftime("%Y-%m-%d"),
        "descricao": "Nova descrição da tarefa",
    }
    
    response = client.post(url, data, follow=True)

    assert response.status_code == 200 # Após redirecionamento para 'home'
    assert response.request["PATH_INFO"] == reverse("home")

    tarefa.refresh_from_db() # Recarrega a tarefa do banco para pegar os dados atualizados
    assert tarefa.titulo == "Título Atualizado"
    assert tarefa.descricao == "Nova descrição da tarefa"
    assert tarefa.data_entrega == nova_data_entrega

@pytest.mark.django_db
def test_tarefa_update_view_post_dados_invalidos(auth_client, create_tarefa):
    """Verifica que a atualização de tarefa com dados inválidos não ocorre e exibe erros."""
    client, user = auth_client
    tarefa = create_tarefa(user=user)

    url = reverse("tarefa_uptade", args=[tarefa.pk])
    data_entrega_passada = date.today() - timedelta(days=1)
    
    data = {
        "titulo": "Título Atualizado Inválido",
        "data_entrega": data_entrega_passada.strftime("%Y-%m-%d"), # Data inválida
        "descricao": "Nova descrição inválida",
    }
    
    response = client.post(url, data)

    assert response.status_code == 200 # Permanece na página de edição com erros
    assert b"A data de entrega n\xc3\xa3o pode ser anterior \xc3\xa0 data de hoje." in response.content

    tarefa.refresh_from_db() # Recarrega para garantir que NÃO foi atualizada
    assert tarefa.titulo == "Tarefa de Teste" # Deve ser o título original, não o inválido

@pytest.mark.django_db
def test_tarefa_update_view_acesso_negado_outro_usuario(client, create_user, create_tarefa):
    """Verifica que um usuário não pode editar a tarefa de outro usuário."""
    owner_user = create_user(username="owner", email="owner@test.com")
    other_user = create_user(username="other", email="other@test.com")
    tarefa = create_tarefa(user=owner_user) # Tarefa do owner

    client.login(username=other_user.username, password="testpassword") # Loga como outro usuário

    url = reverse("tarefa_uptade", args=[tarefa.pk])
    response = client.get(url)

    assert response.status_code == 404 # Ou 403 Forbidden, dependendo da sua implementação (get_queryset com filter)
    # Sua view retorna 404 porque o get_queryset filtra pela tarefa do usuário logado.

# --- Testes para TarefaDeleteView (Exclusão de Tarefas) ---

@pytest.mark.django_db
def test_tarefa_delete_view_get_confirma_exclusao(auth_client, create_tarefa):
    """Verifica se a página de exclusão exibe a confirmação."""
    client, user = auth_client
    tarefa = create_tarefa(user=user)

    url = reverse("tarefa_delete", args=[tarefa.pk])
    response = client.get(url)

    assert response.status_code == 200
    assert b"Tem certeza que deseja excluir" in response.content
    assert b"Tarefa de Teste" in response.content # Título da tarefa deve aparecer

@pytest.mark.django_db
def test_tarefa_delete_view_post_exclui_tarefa(auth_client, create_tarefa):
    """Verifica se o POST na página de exclusão remove a tarefa."""
    client, user = auth_client
    tarefa = create_tarefa(user=user)
    assert Tarefa.objects.count() == 1 # A tarefa existe antes da exclusão

    url = reverse("tarefa_delete", args=[tarefa.pk])
    response = client.post(url, follow=True)

    assert response.status_code == 200 # Após redirecionamento para 'home'
    assert response.request["PATH_INFO"] == reverse("home")
    assert Tarefa.objects.count() == 0 # A tarefa deve ter sido excluída

@pytest.mark.django_db
def test_tarefa_delete_view_acesso_negado_outro_usuario(client, create_user, create_tarefa):
    """Verifica que um usuário não pode excluir a tarefa de outro usuário."""
    owner_user = create_user(username="owner", email="owner@test.com")
    other_user = create_user(username="other", email="other@test.com")
    tarefa = create_tarefa(user=owner_user)

    client.login(username=other_user.username, password="testpassword")

    url = reverse("tarefa_delete", args=[tarefa.pk])
    response = client.get(url) # Acessa a página de confirmação
    assert response.status_code == 404 # Ou 403 Forbidden

    # Tenta fazer o POST de exclusão
    response = client.post(url)
    assert response.status_code == 404 # Ou 403 Forbidden
    assert Tarefa.objects.count() == 1 # A tarefa não deve ter sido excluída


# --- Testes para adicionar_comentario (Comentários) ---

@pytest.mark.django_db
def test_adicionar_comentario_post_dados_validos(auth_client, create_tarefa):
    """Verifica se um comentário é adicionado com sucesso."""
    client, user = auth_client
    tarefa = create_tarefa(user=user)

    url = reverse("adicionar_comentario", args=[tarefa.pk])
    data = {
        "conteudo": "Este é um novo comentário."
    }
    response = client.post(url, data, follow=True)

    # Verifica o redirecionamento para a página de detalhes da tarefa
    assert response.status_code == 200
    assert response.request["PATH_INFO"] == reverse("tarefa_detalhe", args=[tarefa.pk])

    # Verifica se o comentário foi criado no banco de dados
    assert Comentario.objects.count() == 1
    comentario_criado = Comentario.objects.first()

    assert comentario_criado.conteudo == "Este é um novo comentário."
    assert comentario_criado.tarefa == tarefa
    assert comentario_criado.usuario == user

    # Verifica se o comentário aparece na página de detalhes da tarefa
    assert b"Este \xc3\xa9 um novo coment\xc3\xa1rio." in response.content

@pytest.mark.django_db
def test_adicionar_comentario_post_conteudo_vazio(auth_client, create_tarefa):
    """Verifica se um comentário com conteúdo vazio não é adicionado."""
    client, user = auth_client
    tarefa = create_tarefa(user=user)

    url = reverse("adicionar_comentario", args=[tarefa.pk])
    data = {
        "conteudo": "" # Conteúdo vazio
    }
    response = client.post(url, data)

    assert response.status_code == 200 # Permanece na mesma página
    assert b"Este campo \xc3\xa9 obrigat\xc3\xb3rio." in response.content
    assert Comentario.objects.count() == 0 # Nenhum comentário criado

# --- Testes para TarefasListView (Listagem de Tarefas) ---

@pytest.mark.django_db
def test_tarefas_list_view_exibe_apenas_tarefas_do_usuario_logado(auth_client, create_user, create_tarefa):
    """Verifica se a lista de tarefas exibe apenas as tarefas do usuário logado."""
    client, user1 = auth_client # user1 é o usuário logado
    user2 = create_user(username="other_user", email="other@example.com")

    # Cria tarefas para ambos os usuários
    tarefa1_user1 = create_tarefa(user=user1, titulo="Minha Tarefa 1")
    tarefa2_user1 = create_tarefa(user=user1, titulo="Minha Tarefa 2")
    tarefa_user2 = create_tarefa(user=user2, titulo="Tarefa do Outro Usuário")

    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200
    
    # Verifica se as tarefas do usuário logado estão presentes
    assert b"Minha Tarefa 1" in response.content
    assert b"Minha Tarefa 2" in response.content

    # Verifica se a tarefa do outro usuário NÃO está presente
    assert b"Tarefa do Outro Usu\xc3\xa1rio" not in response.content

@pytest.mark.django_db
def test_tarefas_list_view_nao_exibe_tarefas_para_usuario_deslogado(client, create_user, create_tarefa):
    """Verifica se a lista de tarefas redireciona usuários deslogados."""
    user = create_user()
    tarefa = create_tarefa(user=user)

    url = reverse("home")
    response = client.get(url)

    # LoginRequiredMixin deve redirecionar para a página de login
    assert response.status_code == 302
    assert "login" in response.url # Redireciona para a URL de login