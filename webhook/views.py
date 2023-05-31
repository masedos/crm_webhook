import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from webhook.models import Aluno

# Create your views here.


# @csrf_exempt
# @require_http_methods(["GET", "POST"])
# def event(request):
#     print(json.loads(request.body)) 
   
#     return HttpResponse('success')

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def event(request):
    data = json.loads(request.body)
    
    # Check if student already exists
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
