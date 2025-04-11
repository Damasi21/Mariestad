import os
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .models import Produto
from .forms import ProdutoForm
from .models import Status, Tag
from .forms import StatusForm, TagForm
from .models import Contato
from .forms import ContatoForm
from .models import Obra, ObraAnexo
from .forms import ObraForm
from .models import StatusCliente
from .forms import StatusClienteForm
from django.conf import settings
 


from django.db.models import Q  # Import necessário para busca dinâmica


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

def configuracoes(request):
    status_form = StatusForm()
    tag_form = TagForm()
    status_cliente_form = StatusClienteForm()

    status_salvo = request.session.pop('status_salvo', False)
    tag_salvo = request.session.pop('tag_salvo', False)
    status_cliente_salvo = request.session.pop('status_cliente_salvo', False)

    if request.method == 'POST':
        if 'status_id' in request.POST or 'nome_status' in request.POST:
            if request.POST.get('status_id'):
                status = get_object_or_404(Status, id=request.POST.get('status_id'))
                status_form = StatusForm(request.POST, instance=status)
            else:
                status_form = StatusForm(request.POST)

            if status_form.is_valid():
                status_form.save()
                request.session['status_salvo'] = True
                return redirect('configuracoes')

        elif 'tag_id' in request.POST or 'nome_tag' in request.POST:
            if request.POST.get('tag_id'):
                tag = get_object_or_404(Tag, id=request.POST.get('tag_id'))
                tag_form = TagForm(request.POST, instance=tag)
            else:
                tag_form = TagForm(request.POST)

            if tag_form.is_valid():
                tag_form.save()
                request.session['tag_salvo'] = True
                return redirect('configuracoes')
            
        elif 'status_cliente_id' in request.POST or 'nome' in request.POST:
            if request.POST.get('status_cliente_id'):
                status_cliente = get_object_or_404(StatusCliente, id=request.POST.get('status_cliente_id'))
                status_cliente_form = StatusClienteForm(request.POST, instance=status_cliente)
            else:
                status_cliente_form = StatusClienteForm(request.POST)
     
            if status_cliente_form.is_valid():
                status_cliente_form.save()
                request.session['status_cliente_salvo'] = True
                return redirect('configuracoes')
       

    return render(request, 'configuracoes.html', {
        'status_form': status_form,
        'tag_form': tag_form,
        'status_cliente_form': status_cliente_form,
        'status_list': Status.objects.all(),
        'tag_list': Tag.objects.all(),
        'status_cliente_list': StatusCliente.objects.all(),
        'status_salvo': status_salvo,
        'tag_salvo': tag_salvo,
        'status_cliente_salvo': status_cliente_salvo,
    })



def excluir_status(request, id):
    status = get_object_or_404(Status, id=id)
    status.delete()
    request.session['status_salvo'] = True
    return redirect('configuracoes')

def excluir_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    tag.delete()
    request.session['tag_salvo'] = True
    return redirect('configuracoes')

def excluir_status_cliente(request, id):
    status = get_object_or_404(StatusCliente, id=id)
    status.delete()
    request.session['status_cliente_salvo'] = True
    return redirect('configuracoes')

#------------------------------------------------------------------------

def cadastro_contatos(request):
    form = ContatoForm()
    contato_salvo = request.session.pop('contato_salvo', False)

    if request.method == 'POST':
        if request.POST.get('contato_id'):
            contato = get_object_or_404(Contato, id=request.POST.get('contato_id'))
            form = ContatoForm(request.POST, instance=contato)
        else:
            form = ContatoForm(request.POST)

        if form.is_valid():
            form.save()
            request.session['contato_salvo'] = True
            return redirect('cadastro_contatos')

    lista = Contato.objects.all()

    return render(request, 'cadastro_contato.html', {
        'form': form,
        'lista': lista,
        'contato_salvo': contato_salvo
    })

def excluir_contato(request, id):
    contato = get_object_or_404(Contato, id=id)
    contato.delete()
    request.session['contato_salvo'] = True
    return redirect('cadastro_contatos')

#------------------------------------------------------------------------

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

    return render(request, 'cadastro_obra.html', {
        'form': form,
        'lista': lista,
        'obra_salva': obra_salva,
        'anexos': anexos
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
