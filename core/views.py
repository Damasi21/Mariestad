import os
import requests
import json
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from .models import Produto
from .forms import ProdutoForm
from .models import Status, Tag, StatusCliente
from .forms import StatusForm, TagForm, StatusClienteForm
from .models import Contato
from .models import Obra, ObraAnexo
from .forms import ObraForm
from django.conf import settings
from .models import Cliente
from .forms import ClienteForm
from django.db.models import Q  # Import necessário para busca dinâmica
from django.template.loader import render_to_string


def index(request):
    return render(request, 'index.html')

#------------------------------------------------------------------------
#PRODUTO 
def cadastro_produto(request):
    produtos = Produto.objects.all()
    salvo = request.session.pop('produto_salvo', False)
    excluido = request.session.pop('produto_excluido', False)

    if request.method == "POST":
        print(">>> Recebido POST")
        print("POST:", request.POST)
        print("FILES:", request.FILES)

        produto_id = request.POST.get('produto_id')
        if produto_id:
            produto = get_object_or_404(Produto, id=produto_id)
            form = ProdutoForm(request.POST, request.FILES, instance=produto)
        else:
            form = ProdutoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            print(">>> Formulário válido, salvando produto...")
            request.session['produto_salvo'] = True
            return redirect('cadastro_produto')
        else:
            print(">>> Formulário inválido:")
            print(form.errors)
    else:
        form = ProdutoForm()

    return render(request, "cadastro_produto.html", {
        "form": form,
        "produtos": produtos,
        "salvo": salvo,
        "excluido": excluido,
    })

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    request.session['produto_excluido'] = True
    return redirect('cadastro_produto')

#------------------------------------------------------------------------
#CONTATOS 

def cadastro_contatos(request):
    contatos = Contato.objects.select_related("cliente").all()
    return render(request, "cadastro_contato.html", {
        "contatos": contatos
    })



#------------------------------------------------------------------------
#OBRAS

def cadastro_obras(request):
    obra_salva = request.session.pop('obra_salva', False)
    lista = Obra.objects.all()
    anexos = []

    if request.method == 'POST':
        obra_id = request.POST.get('obra_id')

        if obra_id:
            obra = get_object_or_404(Obra, id=obra_id)
            anexos = ObraAnexo.objects.filter(obra=obra)
        else:
            obra = None
            anexos = []

        form = ObraForm(request.POST, request.FILES, instance=obra)

        if form.is_valid():
            nova_obra = form.save(commit=False)
            nova_obra.save()

            nova_obra.responsaveis.set(request.POST.getlist('responsaveis'))
            nova_obra.tags.set(request.POST.getlist('tags'))

            for file in request.FILES.getlist('arquivo'):
                ObraAnexo.objects.create(obra=nova_obra, arquivo=file)

            request.session['obra_salva'] = True
            return redirect('cadastro_obras')
    else:
        form = ObraForm()
        obra_id = request.GET.get('obra_id')
        if obra_id:
            obra = get_object_or_404(Obra, id=obra_id)
            anexos = ObraAnexo.objects.filter(obra=obra)

    # 🔧 Aqui a serialização correta dos clientes:
    clientes_queryset = Cliente.objects.prefetch_related("tags").all()
    clientes_serializados = json.dumps([
        {
            "id": cliente.id,
            "nome": cliente.nome_fantasia,
            "tag": cliente.tags.first().nome if cliente.tags.exists() else "Sem tag"
        }
        for cliente in clientes_queryset
    ], cls=DjangoJSONEncoder)

    return render(request, 'cadastro_obra.html', {
        'form': form,
        'obras': lista,
        'obra_salva': obra_salva,
        'anexos': anexos,
        'clientes': clientes_serializados  # agora corretamente serializado para o JS
    })


def excluir_obra(request, id):
    obra = get_object_or_404(Obra, id=id)
    obra.delete()
    request.session['obra_salva'] = True
    return redirect('cadastro_obras')

#anexar arquivos 
@csrf_exempt
def anexar_arquivos(request):
    if request.method == 'POST':
        obra_id = request.POST.get('obra_id')
        obra = get_object_or_404(Obra, id=obra_id)

        arquivos = request.FILES.getlist('arquivo')
        if not arquivos:
            return JsonResponse({'status': 'erro', 'mensagem': 'Nenhum arquivo enviado'}, status=400)

        for file in arquivos:
            ObraAnexo.objects.create(obra=obra, arquivo=file)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'erro'}, status=400)


def listar_anexos(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    anexos = obra.anexos.all()
    urls = [anexo.arquivo.url for anexo in anexos]
    return JsonResponse({'anexos': urls})

@csrf_exempt
def excluir_anexo(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        url = data.get('url', '')
        if not url:
            return JsonResponse({'status': 'erro', 'mensagem': 'URL inválida'}, status=400)

        relative_path = url.replace(settings.MEDIA_URL, '')
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        from .models import ObraAnexo
        try:
            anexo = ObraAnexo.objects.get(arquivo=relative_path)
            anexo.delete()
            if os.path.exists(full_path):
                os.remove(full_path)
            return JsonResponse({'status': 'ok'})
        except ObraAnexo.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Anexo não encontrado'}, status=404)

#-----------------------------------------------------------------------------------------------

# STATUS

def cadastro_status(request):
    lista = Status.objects.all()
    form = StatusForm()
    mensagem = request.session.pop('mensagem', None)  # ADICIONADO

    if request.method == 'POST':
        status_id = request.POST.get('status_id')
        instance = get_object_or_404(Status, id=status_id) if status_id else None
        form = StatusForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            request.session['mensagem'] = "Status salvo com sucesso!"
            return redirect('cadastro_status')

    return render(request, 'cadastro_status.html', {
        'form': form,
        'lista': lista,
        'mensagem': mensagem  # ADICIONADO
    })



def excluir_status(request, id):
    status = get_object_or_404(Status, id=id)
    status.delete()
    request.session['mensagem'] = "Status excluído com sucesso!"
    return redirect('cadastro_status')

# TAGS

def cadastro_tags(request):
    lista = Tag.objects.all()
    form = TagForm()
    mensagem = request.session.pop('mensagem', None)  # ADICIONADO

    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        instance = get_object_or_404(Tag, id=tag_id) if tag_id else None
        form = TagForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            request.session['mensagem'] = "Tag salva com sucesso!"
            return redirect('cadastro_tags')

    return render(request, 'cadastro_tags.html', {
        'form': form,
        'lista': lista,
        'mensagem': mensagem  # ADICIONADO
    })


def excluir_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    tag.delete()
    request.session['mensagem'] = "Tag excluída com sucesso!"
    return redirect('cadastro_tags')


# STATUS CLIENTE

def cadastro_status_cliente(request):
    lista = StatusCliente.objects.all()
    mensagem = request.session.pop('mensagem', None)

    status_cliente_id = request.POST.get('status_cliente_id') if request.method == 'POST' else None
    instance = StatusCliente.objects.filter(id=status_cliente_id).first() if status_cliente_id else None
    form = StatusClienteForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        request.session['mensagem'] = "Status de cliente salvo com sucesso!"
        return redirect('cadastro_status_cliente')

    return render(request, 'cadastro_status_clientes.html', {
        'form': form,
        'lista': lista,
        'mensagem': mensagem
    })




def excluir_status_cliente(request, id):
    status_cliente = get_object_or_404(StatusCliente, id=id)
    status_cliente.delete()
    request.session['mensagem'] = "Status de cliente excluído com sucesso!"
    return redirect('cadastro_status_cliente')


def configuracoes(request):
    return render(request, 'configuracoes.html')

#CLIENTES 

def cadastro_clientes(request):
    sucesso = request.session.pop("cliente_salvo", False)
    cliente_id = request.POST.get("cliente_id")
    instance = None

    if request.method == "POST" and cliente_id:
        try:
            instance = Cliente.objects.get(id=int(cliente_id))
        except (ValueError, Cliente.DoesNotExist):
            instance = None

    form = ClienteForm(request.POST or None, instance=instance)

    if request.method == "POST" and form.is_valid():
        cliente = form.save(commit=False)  # Salva parcialmente
        cliente.save()
        if hasattr(form, 'save_m2m'):
            form.save_m2m()  # Salva relacionamentos (tags)
        request.session["cliente_salvo"] = True
        return redirect("cadastro_clientes")

    clientes = Cliente.objects.all()

    return render(request, "cadastro_clientes.html", {
        "form": form,
        "clientes": clientes,
        "sucesso": sucesso
    })


#BUSCAR DADOS CLIENTES 

def buscar_dados_empresa(request):
    cnpj = request.GET.get("cnpj", "").replace(".", "").replace("/", "").replace("-", "")
    if not cnpj or len(cnpj) != 14:
        return JsonResponse({"error": "CNPJ inválido"}, status=400)

    try:
        response = requests.get(f"https://www.receitaws.com.br/v1/cnpj/{cnpj}", headers={"Accept": "application/json"})

        if response.status_code == 429:
            return JsonResponse({"error": "Limite de consultas excedido. Tente novamente mais tarde."}, status=429)

        data = response.json()

        if data.get("status") == "ERROR":
            return JsonResponse({"error": data.get("message", "Erro ao buscar CNPJ")}, status=400)

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": "Erro interno ao consultar CNPJ"}, status=500)

#LISTAR CONTATOS DOS CLIENTES 

def listar_contatos_cliente(request):
    cliente_id = request.GET.get("cliente_id")
    if not cliente_id:
        return JsonResponse([], safe=False)

    contatos = Contato.objects.filter(cliente_id=cliente_id).values(
        "id", "nome", "cargo", "telefone1", "telefone2", "email", "observacoes"
    )

    return JsonResponse(list(contatos), safe=False)

@csrf_exempt
def salvar_contato(request):
    if request.method == "POST":
        from .models import Cliente

        cliente_id = request.POST.get("cliente_id")
        cliente = get_object_or_404(Cliente, id=cliente_id)

        contato = Contato.objects.create(
            cliente=cliente,
            nome=request.POST.get("nome"),
            cargo=request.POST.get("cargo"),
            telefone1=request.POST.get("telefone1"),
            telefone2=request.POST.get("telefone2"),
            email=request.POST.get("email"),
            observacoes=request.POST.get("observacoes"),
        )

        return JsonResponse({"status": "ok", "id": contato.id})
    return JsonResponse({"status": "erro", "mensagem": "Método não permitido"}, status=405)

#EXCLUIR CONTATOS DOS CLIENTES 

@csrf_exempt
@require_http_methods(["DELETE"])
def excluir_contato(request, id):
    try:
        contato = Contato.objects.get(id=id)
        contato.delete()
        return JsonResponse({"status": "ok"})
    except Contato.DoesNotExist:
        return JsonResponse({"status": "erro", "mensagem": "Contato não encontrado"}, status=404)

#EDITAR CONTATOS DE CLIENTES 

# Retorna os dados de um contato específico (GET)
def contato_por_id(request, id):
    try:
        contato = Contato.objects.get(id=id)
        data = {
            "id": contato.id,
            "cliente_id": contato.cliente.id if contato.cliente else "",
            "nome": contato.nome,
            "cargo": contato.cargo,
            "telefone1": contato.telefone1,
            "telefone2": contato.telefone2,
            "email": contato.email,
            "observacoes": contato.observacoes,
        }
        return JsonResponse(data)
    except Contato.DoesNotExist:
        return JsonResponse({"error": "Contato não encontrado"}, status=404)

# Edita um contato existente (POST)
@csrf_exempt
@require_http_methods(["POST"])
def editar_contato(request, id):
    try:
        contato = Contato.objects.get(id=id)
        contato.nome = request.POST.get("nome")
        contato.cargo = request.POST.get("cargo")
        contato.telefone1 = request.POST.get("telefone1")
        contato.telefone2 = request.POST.get("telefone2")
        contato.email = request.POST.get("email")
        contato.observacoes = request.POST.get("observacoes")
        contato.save()
        return JsonResponse({"status": "ok"})
    except Contato.DoesNotExist:
        return JsonResponse({"status": "erro", "mensagem": "Contato não encontrado"}, status=404)
    
#MAPAS

def clientes_mapa_json(request):
    clientes = Cliente.objects.select_related('status').all()
    dados = []

    for cliente in clientes:
        # Verifica se todos os campos obrigatórios estão preenchidos
        if all([cliente.endereco, cliente.numero, cliente.cidade, cliente.estado]):
            dados.append({
                'nome': cliente.razao_social,
                'endereco': cliente.endereco,
                'numero': cliente.numero,
                'cidade': cliente.cidade,
                'estado': cliente.estado,
                'status_nome': cliente.status.nome if cliente.status else 'Sem status'
            })

    return JsonResponse(dados, safe=False)


def mapa_clientes(request):
    return render(request, 'mapa_clientes.html')

#----------------------------------------------------------------------------

