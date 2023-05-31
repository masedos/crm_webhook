# Microsoft Dynamics: Usando Python/Django e Ngrok para implementar Webhook

Um webhook é uma forma de comunicação entre sistemas, onde um sistema pode enviar informações em tempo real para outro sistema através de requisições HTTP. Neste artigo, vamos explorar como criar um webhook em Python usando o framework Django e o serviço Ngrok para criar um túnel seguro e expor o servidor local para acesso externo.

## Configurando o ambiente
Antes de começar, é necessário ter o Python, Django e o Ngrok instalados no seu ambiente de desenvolvimento. Certifique-se de ter o Python na versão 3.x e instale o Django usando o gerenciador de pacotes pip. Execute o seguinte comando no terminal:

```console
pip install django ngrok
```

Além disso, precisaremos do Ngrok para criar um túnel seguro e expor o servidor local para acesso externo. O Ngrok é uma ferramenta que permite criar um URL público temporário que é redirecionado para o seu servidor local. Para que o mesmo funcione é necessário fazer um cadastro no site do Ngrok, acesse o site oficial (https://ngrok.com/) para criar uma token ao executar o serviço.

```console
ngrok config add-authtoken  seu token vai aqui
```


## Criando o projeto Django

Vamos começar criando um projeto Django básico. Abra o terminal e execute os seguintes comandos:
```python
django-admin startproject crm_webhook
cd crm_webhook
python manage.py startapp webhook
```

Isso criará um novo projeto Django chamado crm_webhook com um aplicativo chamado webhook_app.

Agora, abra o arquivo crm_webhook/settings.py e adicione 'webhook' à lista de aplicativos instalados:

```python
INSTALLED_APPS = [
    ...
    'webhook',
]
```

Em seguida, abra o arquivo crm_webhook/urls.py e adicione uma rota para o nosso webhook. Substitua o conteúdo do arquivo pelas seguintes linhas:


```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('webhook.urls'))
]
```


Aqui, estamos incluindo a rota do aplicativo  webhook a função event do arquivo webhook/urls.py que chamará essa função.


```python
from django.contrib import admin
from django.urls import path
from webhook.views import event
urlpatterns = [
    path('', event, name='event'),
]
```

## Definindo o modelo

No arquivo webhook/models.py, defina o modelo Aluno com os campos necessários:


```python
from django.db import models

class Aluno(models.Model):
    NumeroInscricao = models.CharField(blank=True, max_length=10)
    Oferta = models.CharField(blank=True, max_length=50)
    TurnoOfertado = models.CharField(blank=True, max_length=10)
    NomeCompleto = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return self.NumeroInscricao
```

Nesse exemplo, estamos criando um modelo chamado Aluno com os campos NumeroInscricao, Oferta, TurnoOfertado e NomeCompleto.

Em seguida, execute o comando python manage.py makemigrations para criar as migrações para o modelo e, em seguida, python manage.py migrate para aplicar as migrações ao banco de dados.

## Implementando o webhook
Agora, vamos implementar a função event no arquivo webhook/views.py para processar as requisições do webhook:


```python
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from webhook_app.models import Aluno

@csrf_exempt
@require_http_methods(["GET", "POST"])
def event(request):
    data = json.loads(request.body)

    # Verificar se o aluno já existe
    numero_inscricao = data['dados']['NumeroInscricao']
    oferta_nome = data['dados']['Oferta']['Nome']
    turno_ofertado = data['dados']['Oferta']['TurnoOfertado']
    nome_completo = data['dados']['LeadReferencia']['Nome']

    aluno, created = Aluno.objects.get_or_create(
        NumeroInscricao=numero_inscricao,
        Oferta=oferta_nome,
        TurnoOfertado=turno_ofertado,
        NomeCompleto=nome_completo
    )

    if created:
        print("Novo aluno cadastrado:", aluno)
    else:
        print("Aluno já cadastrado:", aluno)

    response_data = json.dumps(data)
    return HttpResponse(response_data, status=200)
```

Nesse exemplo, estamos utilizando os decoradores csrf_exempt e require_http_methods(["GET", "POST"]) para desativar a proteção CSRF e permitir apenas as requisições GET e POST.

A função event recebe a requisição HTTP e processa os dados recebidos. Aqui, estamos extraindo os campos relevantes do payload JSON recebido e utilizando o método get_or_create para verificar se o aluno já existe no banco de dados. Se o aluno não existir, ele será criado, caso contrário, apenas retornaremos a instância existente. Por fim, estamos retornando uma resposta HTTP com o payload JSON recebido.

## Executando o servidor Django

Agora, vamos iniciar o servidor Django para testar o webhook localmente. No terminal, execute o comando python manage.py runserver. O servidor será executado em http://localhost:8000/.

```console
python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 31, 2023 - 11:30:13
Django version 4.1.5, using settings 'crm_webhook.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Expondo o servidor local com o Ngrok
Para que o webhook seja acessível externamente, usaremos o Ngrok para criar um túnel seguro. Abra uma nova janela do terminal e navegue até o diretório onde o Ngrok foi instalado. Em seguida, execute o seguinte comando:

```console
ngrok http 8000
```

Isso criará um túnel seguro e fornecerá um URL público temporário que redireciona para o seu servidor local em http://localhost:8000/. Como mostra a figura abaixo.

Configurando o Ngrok no Microsoft Dynamics
Agora que temos o URL público do Ngrok, podemos configurá-lo no Microsoft Dynamics para receber as notificações do webhook. Acesse o Microsoft Dynamics e encontre a seção de configurações de webhook. Adicione o URL fornecido pelo Ngrok (por exemplo, https://2889-200-18-170-200.ngrok-free.app) como o endpoint do webhook.

Para este teste utilizei o CRM Educacional que roda no Microsoft Dynamics, onde o mesmo possui o campo expecifico para adicionar a URL como mostra a imagem abaixo.

A partir de agora, sempre que o candidato realizar uma inscrição e os requisitos de negócio cumpridos oo Microsoft Dynamics enviar uma requisição para o webhook, ele será recebido pelo seu servidor Django localmente e os dados serão processados e armazenados no banco de dados.

## Conclusão
Neste artigo, exploramos como criar um webhook em Python/Django usando o Ngrok para expor o servidor local. Implementamos a função de webhook no Django, configuramos o Ngrok para criar um túnel seguro e integramos o webhook com o Microsoft Dynamics.

Agora você tem as bases necessárias para implementar webhooks em seus porjetos