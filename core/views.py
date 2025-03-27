import requests
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Status
from .models import Tag
from .models import Produto
from .forms import ProdutoForm
from .models import Obra
from .forms import ObraForm
from .models import Contato
from .forms import ContatoForm

from django.db.models import Q  # Import necessário para busca dinâmica


def index(request):
    return render(request, 'index.html')

#---CADASTROS : ------------------------------------------------------------------------

def cadastro_clientes(request):
    return render(request, 'cadastro_clientes.html')

#-------------------------CADASTRO TAGS------------------------------------------------

def cadastro_tags(request):
    query = request.GET.get('q', '')  # Captura o termo digitado na busca
    tags = Tag.objects.all()  # Lista todas as tags por padrão

    if query:
        tags = tags.filter(
            Q(nome_tag__icontains=query)  # Filtra se a tag contém o termo digitado
        )
    return render(request, "cadastro_tags.html", {"tags": tags, "query": query})

#----------------------CADASTRO STATUS ---------------------------------------------------

def cadastro_status(request):
    query = request.GET.get('q', '')  
    status_list = Status.objects.all()  

    if query:
        status_list = status_list.filter(
            Q(nome_status__icontains=query)  
        )

    return render(request, "cadastro_status.html", {"status_list": status_list, "query": query})

#---------------CADASTRO PRODUTOS----------------------------------------------------------

def cadastro_produto(request):
    query = request.GET.get('q', '')  
    produtos = Produto.objects.all()

    if query:
        produtos = produtos.filter(
            Q(codigo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(preco__icontains=query)
        )

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cadastro_produto')
    else:
        form = ProdutoForm()

    return render(request, "cadastro_produto.html", {
        "form": form,
        "produtos": produtos,
        "query": query
    })

#----------CADASTRO OBRAS--------------------------------------------------------------

def cadastro_obras(request):
    query = request.GET.get('q', '')
    obras = Obra.objects.all()

    if query:
        obras = obras.filter(
            Q(nome_obra__icontains=query) |
            Q(localizacao__icontains=query) |
            Q(cidade__icontains=query) |
            Q(estado__icontains=query)
        )

    form = ObraForm(request.POST or None)
    if request.method == 'POST':
        obra_id = request.POST.get('obra_id')
        if form.is_valid():
            if obra_id:
                obra = Obra.objects.get(id=obra_id)
                for field in form.cleaned_data:
                    setattr(obra, field, form.cleaned_data[field])
                obra.save()
            else:
                form.save()
            return redirect('cadastro_obras')

    return render(request, 'cadastro_obra.html', {
        'form': form,
        'obras': obras,
        'query': query
    })


#-----CADASTRO CONTATOS --------------------------------------------------------------------

def cadastro_contatos(request):
    query = request.GET.get('q', '')
    contatos = Contato.objects.all()

    if query:
        contatos = contatos.filter(
            Q(nome__icontains=query) |
            Q(email__icontains=query) |
            Q(telefone1__icontains=query)
        )

    contato_id = request.POST.get('contato_id')
    form = ContatoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if contato_id:
            contato = Contato.objects.get(id=contato_id)
            for field in form.cleaned_data:
                setattr(contato, field, form.cleaned_data[field])
            contato.save()
        else:
            form.save()
        return redirect('/cadastro_contatos/?sucesso=1')

    return render(request, 'cadastro_contato.html', {
        'form': form,
        'contatos': contatos,
        'query': query
    })


#--#BUSCAR CNPJ: ---------------------------------------------------------------------------

def buscar_dados_empresa(request):
    cnpj = request.GET.get('cnpj', '').strip()  # Remove espaços extras

    if not cnpj:
        return JsonResponse({'error': 'CNPJ não fornecido.'}, status=400)

    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    headers = {'Accept': 'application/json'}

    try:
        response = requests.get(url, headers=headers, timeout=5)  # Timeout de 5 segundos

        if response.status_code == 200:
            dados_empresa = response.json()
            return JsonResponse(dados_empresa)
        else:
            return JsonResponse({'error': 'Erro ao consultar a API da ReceitaWS.'}, status=response.status_code)

    except requests.Timeout:
        return JsonResponse({'error': 'A API da ReceitaWS demorou muito para responder. Tente novamente mais tarde.'}, status=504)

    except requests.RequestException as e:
        return JsonResponse({'error': f'Erro na requisição: {str(e)}'}, status=500)
    
#---VER, EDITAR E EXCLUIR :  --------------------------------------------------------------------------

# VER STATUS
def status_view(request):
    """Exibe a página de status e a lista de status cadastrados."""
    statuses = Status.objects.all()  # Busca todos os status no banco
    return render(request, "cadastro_status.html", {"statuses": statuses})
#-------------------------------------------------------------------------
# SALVAR STATUS
def salvar_status(request):
    """Salva um novo status garantindo que ele seja único."""
    if request.method == "POST":
        nome_status = request.POST.get("nome_status").strip()  # Remove espaços extras

        if Status.objects.filter(nome_status__iexact=nome_status).exists():
            return JsonResponse({"error": "Status já cadastrado com este nome!"}, status=400)

        novo_status = Status.objects.create(nome_status=nome_status)

        # Retorna a lista atualizada
        statuses = list(Status.objects.values())
        return JsonResponse({"statuses": statuses})

    return JsonResponse({"error": "Requisição inválida"}, status=400)
#-------------------------------------------------------------------------
# EDITAR STATUS
def editar_status(request, id):
    status = get_object_or_404(Status, id=id)

    if request.method == "POST":
        novo_nome = request.POST.get("nome_status")
        if novo_nome:
            status.nome_status = novo_nome
            status.save()
            return JsonResponse({"success": True, "id": status.id, "nome_status": status.nome_status})

    return JsonResponse({"error": "Requisição inválida"}, status=400)
#-------------------------------------------------------------------------
# EXCLUIR STATUS
def excluir_status(request, id):
    status = get_object_or_404(Status, id=id)

    if request.method == "POST":
        status.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Requisição inválida"}, status=400)

#-----------------------------------------------------------------------------

# VER TAGS
def tags_view(request):
    """Exibe a página de tags e a lista de tags cadastradas."""
    tags = Tag.objects.all()  # Busca todos as tags no banco
    return render(request, "cadastro_tags.html", {"tags": tags})
#-------------------------------------------------------------------------
# SALVAR TAGS
def salvar_tags(request):
    """Salva uma nova tag garantindo que ela seja única."""
    if request.method == "POST":
        nome_tag = request.POST.get("nome_tag").strip()  # Remove espaços extras

        if Tag.objects.filter(nome_tag__iexact=nome_tag).exists():
            return JsonResponse({"error": "Tag já cadastrada com este nome!"}, status=400)

        nova_tag = Tag.objects.create(nome_tag=nome_tag)

        # Retorna a lista atualizada
        tags = list(Tag.objects.values())# Obtém todas as tags
        return JsonResponse({"tags": tags})  # Retorna "tags" no JSON

    return JsonResponse({"error": "Requisição inválida"}, status=400)
#-------------------------------------------------------------------------
# EDITAR TAGS 
def editar_tags(request, id):
    tag = get_object_or_404(Tag, id=id)

    if request.method == "POST":
        novo_nome = request.POST.get("nome_tag")
        if novo_nome:
            tag.nome_tag= novo_nome
            tag.save()
            return JsonResponse({"success": True, "id": tag.id, "nome_tag": tag.nome_tag})

    return JsonResponse({"error": "Requisição inválida"}, status=400)
#-------------------------------------------------------------------------
# EXCLUIR TAGS 
def excluir_tags(request, id):
    tag = get_object_or_404(Tag, id=id)

    if request.method == "POST":
        tag.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Requisição inválida"}, status=400)

#-------------------------------------------------------------------------------
# EXCLUIR PRODUTOS 

def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    return redirect('cadastro_produto')  # Redireciona para a lista após excluir

#-------------------------------------------------------------------------------
# EXCLUIR OBRAS 

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def excluir_obra(request, id):
    obra = get_object_or_404(Obra, id=id)
    if request.method == 'POST':
        obra.delete()
        return redirect('cadastro_obras')
    
#-------------------------------------------------------------------------------
# EDITAR CONTATOS

def editar_contato(request, id):
    contato = get_object_or_404(Contato, id=id)
    if request.method == "POST":
        contato.nome = request.POST.get("nome")
        contato.telefone1 = request.POST.get("telefone1")
        contato.telefone2 = request.POST.get("telefone2")
        contato.email = request.POST.get("email")
        contato.observacoes = request.POST.get("observacoes")
        contato.save()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Requisição inválida"}, status=400)

#-------------------------------------------------------------------------------
# EXCLUIR CONTATOS

@csrf_exempt
def excluir_contato(request, id):
    contato = get_object_or_404(Contato, id=id)
    if request.method == "POST":
        contato.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Requisição inválida"}, status=400)




