import os
import requests
import json
import subprocess
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.contrib import messages
from django.db.models.functions import Coalesce
from django.conf import settings
from django.db.models import Sum, F, FloatField, Value,ExpressionWrapper,DecimalField
from .models import Produto
from .forms import ProdutoForm
from .models import Status, Tag, StatusCliente
from .forms import StatusForm, TagForm, StatusClienteForm
from .models import Contato
from .models import Obra, ObraAnexo
from .forms import ObraForm
from .models import Cliente
from .forms import ClienteForm
from django.db.models import Q  # Import necessário para busca dinâmica
from django.template.loader import render_to_string
from .models import Vendedor
from .forms import VendedorForm
from .models import Proposta
from .forms import PropostaForm
from django.db.models import Max
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.http import HttpResponse
from django.http import FileResponse, Http404
from babel.numbers import format_currency
from django.db.models.functions import Upper, Trim
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, CadastroForm
from django.contrib.auth.views import LoginView
from weasyprint import HTML, CSS
from .models import UsuarioPersonalizado
from .forms import UsuarioPersonalizadoForm
from django.urls import path
from . import views
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from math import ceil
from django.core.serializers import serialize

#------------------------------------------------------------------------


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

    # ✅ Aplicando paginação na listagem de obras
    obras_completas = Obra.objects.all().order_by('-data_inicio')  # ou outra ordenação
    paginador = Paginator(obras_completas, 15)  # 15 por página
    pagina = request.GET.get('page')
    obras = paginador.get_page(pagina)

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
#-----------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------------------------
#USUARIOS 
def cadastro_usuarios(request):
    usuarios = UsuarioPersonalizado.objects.all()
    mensagem = request.session.pop("mensagem", None)

    if request.method == 'POST':
        usuario_id = request.POST.get("usuario_id")
        instance = get_object_or_404(UsuarioPersonalizado, id=usuario_id) if usuario_id else None
        form = CadastroForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            request.session["mensagem"] = "Usuário salvo com sucesso!"
            return redirect("cadastro_usuarios")
    else:
        form = CadastroForm()

    return render(request, "cadastro_usuarios.html", {
        "form": form,
        "usuarios": usuarios,
        "mensagem": mensagem
    })

Usuario = get_user_model()

def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        form = UsuarioPersonalizadoForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('cadastro_usuarios')
    else:
        form = UsuarioPersonalizadoForm(instance=usuario)
    usuarios = Usuario.objects.all()
    return render(request, 'cadastro_usuarios.html', {'form': form, 'usuarios': usuarios})


def excluir_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.delete()
    return redirect('cadastro_usuarios')

#-----------------------------------------------------------------------------------------------
#CLIENTES 

def cadastro_clientes(request):
    clientes = Cliente.objects.select_related('status').prefetch_related('tags', 'vendedores').all()
    sucesso = False

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        instance = get_object_or_404(Cliente, id=cliente_id) if cliente_id else None

        form = ClienteForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            sucesso = True
            return redirect('cadastro_clientes')  # Pode usar mensagem com session se quiser feedback

    else:
        form = ClienteForm()

    # Lista paginada de clientes
    clientes_lista = Cliente.objects.select_related('status').prefetch_related('tags', 'vendedores').all()
    paginador = Paginator(clientes_lista, 50)  # 10 clientes por página

    pagina = request.GET.get('page')
    clientes = paginador.get_page(pagina)

    context = {
        'form': form,
        'clientes': clientes,
        'sucesso': sucesso
    }
    return render(request, 'cadastro_clientes.html', context)
#-------------------------------------------------------------------------------------------

@csrf_exempt
def excluir_cliente(request, cliente_id):
    if request.method == "POST":
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.delete()
            return JsonResponse({"mensagem": "Cliente excluído com sucesso."})
        except Cliente.DoesNotExist:
            return JsonResponse({"erro": "Cliente não encontrado."}, status=404)
    return JsonResponse({"erro": "Método não permitido."}, status=405)

#-------------------------------------------------------------------------------------------

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
        "id", "nome", "cargo", "telefone1", "telefone2", "email_contato", "observacoes", "perfil"
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
            email_contato=request.POST.get("email_contato"),
            perfil=request.POST.get("perfil"),
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
            "email_contato": contato.email_contato,
            "observacoes": contato.observacoes,
            "perfil": contato.perfil,  
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
        contato.email_contato = request.POST.get("email_contato")
        contato.observacoes = request.POST.get("observacoes")
        contato.perfil = request.POST.get("perfil")
        contato.save()
        return JsonResponse({"status": "ok"})
    except Contato.DoesNotExist:
        return JsonResponse({"status": "erro", "mensagem": "Contato não encontrado"}, status=404)
#MAPAS#-----------------------------------------------------------------------------------


def clientes_mapa_json(request):
    clientes = Cliente.objects.select_related('status').all()
    dados = []

    for cliente in clientes:
        if all([cliente.endereco, cliente.numero, cliente.cidade, cliente.estado]):
            dados.append({
                'id': cliente.id,
                'nome': cliente.razao_social,
                'endereco': cliente.endereco,
                'numero': cliente.numero,
                'cidade': cliente.cidade,
                'estado': cliente.estado,
                'cep': cliente.cep,
                'status_nome': cliente.status.nome if cliente.status else 'Sem status'
            })

    return JsonResponse(dados, safe=False)



def mapa_clientes(request):
    return render(request, 'mapa_clientes.html')

#------------------------MAPA OBRAS-----------------------------------------------------------


def obras_mapa_json(request):
    obras = Obra.objects.all()
    dados = []

    for obra in obras:
        if obra.endereco and obra.cidade and obra.estado:
            dados.append({
                'id': obra.id,
                'nome': obra.nome,
                'endereco': obra.endereco,
                'cidade': obra.cidade,
                'estado': obra.estado,
                'tipo': 'obra',
                'status_nome': obra.status.nome if obra.status else 'Sem status',
                'tags': [tag.nome for tag in obra.tags.all()]  # ✅
            })
    return JsonResponse(dados, safe=False)


#----------------------------------------------------------------------------

def cadastro_vendedores(request):
    lista = Vendedor.objects.all()
    form = VendedorForm()
    mensagem = request.session.pop('mensagem', None)  # ✅ para exibir após salvar

    if request.method == 'POST':
        vendedor_id = request.POST.get('vendedor_id')
        instance = get_object_or_404(Vendedor, id=vendedor_id) if vendedor_id else None
        form = VendedorForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            request.session['mensagem'] = "Vendedor salvo com sucesso!"
            return redirect('cadastro_vendedores')

    return render(request, 'cadastro_vendedores.html', {
        'form': form,
        'lista': lista,
        'mensagem': mensagem
    })


def excluir_vendedor(request, id):
    vendedor = get_object_or_404(Vendedor, id=id)
    vendedor.delete()
    request.session["mensagem"] = "Vendedor excluído com sucesso!"
    return redirect('cadastro_vendedores')

#------------------PROPOSTAS ----------------------------------------------------------


def gerar_numero_proposta():
    ultimo = Proposta.objects.aggregate(maior=Max('numero'))['maior']
    if not ultimo:
        return '00001'
    else:
        return str(int(ultimo) + 1).zfill(5)

#--------------------------------------------------------------------------

def cadastro_propostas(request):
    todas_propostas = Proposta.objects.order_by('-data_inclusao')
    paginator = Paginator(todas_propostas, 50)
    page_number = request.GET.get('page')
    propostas = paginator.get_page(page_number)

    clientes = Cliente.objects.all()
    obras = Obra.objects.all()
    produtos = Produto.objects.all()
    contatos = Contato.objects.all()

    if request.method == 'POST':
        proposta_id = request.POST.get('proposta_id')
        if proposta_id:
            proposta = get_object_or_404(Proposta, id=proposta_id)
            form = PropostaForm(request.POST, instance=proposta)
        else:
            proposta = Proposta(numero=gerar_numero_proposta())
            form = PropostaForm(request.POST, instance=proposta)

        if form.is_valid():
            proposta = form.save(commit=False)
            produtos_data = json.loads(request.POST.get("produtos_json", "[]"))
            produtos_com_imagem = []

            for item in produtos_data:
                try:
                    produto_db = Produto.objects.get(id=item["id_produto"])
                    item["imagem"] = produto_db.foto.name if produto_db.foto else ""
                except Produto.DoesNotExist:
                    item["imagem"] = ""

                produtos_com_imagem.append(item)

            proposta.produtos_json = json.dumps(produtos_com_imagem, cls=DjangoJSONEncoder)

            # Define o vendedor automaticamente com base no cliente, se não foi informado
            if not request.POST.get('vendedor') and proposta.cliente:
                primeiros_vendedores = proposta.cliente.vendedores.all()
                if primeiros_vendedores.exists():
                    proposta.vendedor = primeiros_vendedores.first()

            proposta.save()
            form.save_m2m()
            return redirect('cadastro_propostas')
    else:
        form = PropostaForm()

    contexto = {
        'form': form,
        'propostas': propostas,
        'clientes': clientes,
        'obras': obras,
        'produtos': produtos,
        'contatos': contatos,
    }
    return render(request, 'cadastro_proposta.html', contexto)


#--------------------------------------------------------------------------

def carregar_obras_por_cliente(request, cliente_id):
    obras = Obra.objects.filter(responsaveis__id=cliente_id).distinct()
    dados = [{
        'id': obra.id,
        'nome': f"{obra.nome} - {obra.cidade}/{obra.estado}"
    } for obra in obras]
    return JsonResponse({'obras': dados})

#-----------------------------carregar as observacoes da obra na proposta---------------------------------------------

def observacoes_obra_ajax(request, obra_id):
    try:
        obra = Obra.objects.get(id=obra_id)
        return JsonResponse({'observacoes': obra.observacoes_obra or ''})
    except Obra.DoesNotExist:
        return JsonResponse({'observacoes': ''})


def carregar_contatos_por_cliente(request, cliente_id):
    contatos = Contato.objects.filter(cliente_id=cliente_id)
    dados = [{
        'id': c.id,
        'nome': c.nome,
        'perfil': c.perfil
    } for c in contatos]
    return JsonResponse({'contatos': dados})

#----------------------------BUSCAR INFO DE CLIENTES , OBRAS E TRANSPOSRTADORA NA PROPOSTA ----------------------

def buscar_clientes_ajax(request):
    termo = request.GET.get('q', '')
    clientes = Cliente.objects.filter(Q(nome_fantasia__icontains=termo))[:10]
    dados = [{'id': c.id, 'texto': f"{c.nome_fantasia} - {c.cidade}/{c.estado}"} for c in clientes]
    return JsonResponse(dados, safe=False)

def buscar_transportadoras_ajax(request):
    termo = request.GET.get('q', '')
    clientes = Cliente.objects.filter(Q(nome_fantasia__icontains=termo))[:10]
    dados = [{'id': c.id, 'texto': f"{c.nome_fantasia} - {c.cidade}/{c.estado}"} for c in clientes]
    return JsonResponse(dados, safe=False)

def buscar_obras_ajax(request):
    termo = request.GET.get('q', '')
    obras = Obra.objects.filter(Q(nome__icontains=termo))[:10]
    dados = [{'id': o.id, 'texto': f"{o.nome} - {o.cidade}/{o.estado}"} for o in obras]
    return JsonResponse(dados, safe=False)

def dados_cliente_ajax(request):
    cliente_id = request.GET.get('cliente_id')
    if not cliente_id:
        return JsonResponse({'erro': 'ID do cliente não informado'}, status=400)

    try:
        cliente = Cliente.objects.prefetch_related('vendedores').get(id=cliente_id)
        contatos = Contato.objects.filter(cliente_id=cliente.id)

        vendedores = [{'id': v.id, 'nome': v.nome} for v in cliente.vendedores.all()]
        contatos_list = [{'id': c.id, 'nome': c.nome, 'perfil': c.perfil} for c in contatos]

        return JsonResponse({
            'vendedores': vendedores,
            'contatos': contatos_list
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)
    

def produtos_json(request):
    produtos = Produto.objects.all()
    dados = [
        {
            'id': p.id,
            'codigo': p.codigo,  # Somente o código puro
            'descricao': p.descricao,
            'unidade': p.unidade,
            'preco': float(p.preco),
        }
        for p in produtos
    ]
    return JsonResponse(dados, safe=False)

#----------------------------EDITAR E EXCLUIR PROPOSTA NA LISTAGEM----------------------


def carregar_proposta(request, proposta_id):
    if request.method == "GET":
        try:
            proposta = Proposta.objects.get(id=proposta_id)
            dados = {
                "id": proposta.id,
                "cliente": {"id": proposta.cliente.id,"texto": f"{proposta.cliente.nome_fantasia} - {proposta.cliente.cidade}/{proposta.cliente.estado}"} if proposta.cliente else None,
                "obra": proposta.obra.id if proposta.obra else None,
                "contato": proposta.contato.id if proposta.contato else None,
                "perfil_contato": proposta.perfil_contato,
                "status_proposta": proposta.status_proposta,
                "transportadora": proposta.transportadora.id if proposta.transportadora else None,
                "tipo_frete": proposta.tipo_frete,
                "peso_liquido": str(proposta.peso_liquido or ""),
                "peso_bruto": str(proposta.peso_bruto or ""),
                "volume": proposta.volume,
                "quantidade_volumes": proposta.quantidade_volumes,
                "frete_tech4con": str(proposta.frete_tech4con or ""),
                "frete_cliente": str(proposta.frete_cliente or ""),
                "condicao_pagamento": proposta.condicao_pagamento,
                "parcelas_condicao": proposta.parcelas_condicao,
                "endereco_proposta": proposta.endereco_proposta,
                "numero_proposta": proposta.numero_proposta,
                "complemento_proposta": proposta.complemento_proposta,
                "bairro_proposta": proposta.bairro_proposta,
                "cep_proposta": proposta.cep_proposta,
                "cidade_proposta": proposta.cidade_proposta,
                "estado_proposta": proposta.estado_proposta,
                "nome_entrega": proposta.nome_entrega,  # ✅ Adicione esta linha
                "observacoes_proposta": proposta.observacoes_proposta,
                "produtos_json": proposta.produtos_json or "[]",
            }
            return JsonResponse(dados)
        except Proposta.DoesNotExist:
            return HttpResponseBadRequest("Proposta não encontrada.")
    return HttpResponseNotAllowed(["GET"])

@csrf_exempt
def excluir_proposta(request, proposta_id):
    if request.method == "POST":
        try:
            proposta = Proposta.objects.get(id=proposta_id)
            proposta.delete()
            return JsonResponse({"status": "ok"})
        except Proposta.DoesNotExist:
            return JsonResponse({"status": "erro", "mensagem": "Proposta não encontrada."})
    return HttpResponseNotAllowed(["POST"])


#------------------------------------------------------------------------------------


def buscar_propostas_ajax(request):
    termo = request.GET.get("q", "").strip()
    propostas = Proposta.objects.filter(numero__icontains=termo)[:10]

    resultado = []
    for p in propostas:
        resultado.append({
            "id": p.id,
            "numero": p.numero,
            "cliente": str(p.cliente) if p.cliente else "",
            "data": p.data_inclusao.strftime("%d/%m/%Y") if p.data_inclusao else "",
        })

    return JsonResponse(resultado, safe=False)

#------------------------------------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})

class LoginUsuarioView(LoginView):
    template_name = 'login.html'

#------------------------------------------------------------------------------------

def logout_view(request):
    logout(request)
    return redirect('login')


#----------------------------PDF DA PROPOSTA----------------------

def gerar_pdf_exemplo(request, proposta_id):
    try:
        proposta = get_object_or_404(Proposta, id=proposta_id)

        # Decodifica produtos JSON
        produtos = json.loads(proposta.produtos_json or "[]")
        for p in produtos:
            try:
                produto_id = p.get("id_produto") or p.get("id")
                produto_db = Produto.objects.get(id=produto_id)
                if produto_db.foto:
                    p["imagem_url"] = f"file:///C:/projeto_mariestad/apolux/media/{produto_db.foto.name}"
                else:
                    p["imagem_url"] = "https://via.placeholder.com/150x200"

                preco = float(p.get("preco", 0))
                subtotal = float(p.get("subtotal", 0))
                p["valor_unitario"] = format_currency(preco, "BRL", locale="pt_BR")
                p["subtotal_formatado"] = format_currency(subtotal, "BRL", locale="pt_BR")

            except Produto.DoesNotExist:
                p["imagem_url"] = "https://via.placeholder.com/150x200"
                p["valor_unitario"] = "-"
                p["subtotal_formatado"] = "-"

        # Paginar os produtos (4 por página)
        produtos_por_pagina = 4
        total_paginas = ceil(len(produtos) / produtos_por_pagina)
        paginas_produtos = [produtos[i:i+produtos_por_pagina] for i in range(0, len(produtos), produtos_por_pagina)]

        # Totais
        produtos_total = sum(float(p.get("subtotal", 0)) for p in produtos)
        frete = float(getattr(proposta, "frete_cliente", 0) or 0)
        total_geral = produtos_total + frete

        total_produtos_formatado = format_currency(produtos_total, "BRL", locale="pt_BR")
        frete_formatado = format_currency(frete, "BRL", locale="pt_BR")
        total_geral_formatado = format_currency(total_geral, "BRL", locale="pt_BR")

        context = {
            "proposta": proposta,
            "paginas_produtos": paginas_produtos,
            "total_paginas": total_paginas,
            "total_produtos": total_produtos_formatado,
            "frete": frete_formatado,
            "total_geral": total_geral_formatado,
        }

        html = render_to_string("propostacompleta_pdf.html", context)
        pdf_file = HTML(string=html, base_url="file:///C:/projeto_mariestad/apolux/media").write_pdf()

        return HttpResponse(pdf_file, content_type='application/pdf')

    except Exception as e:
        return HttpResponse(f"Erro: {e}", content_type="text/plain")
