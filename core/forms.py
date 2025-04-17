from decimal import Decimal
from django import forms
from .models import Produto
from .models import Status, Tag, StatusCliente
from .models import Contato
from .models import Obra
from django.utils.translation import gettext_lazy as _
from .models import Cliente





#------------------------------------------------------------------------------------
class ProdutoForm(forms.ModelForm):
    preco = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'id_preco',
    }))

    class Meta:
        model = Produto
        fields = '__all__'
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_foto'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'familia': forms.Select(attrs={'class': 'form-select'}),
            'ncm': forms.TextInput(attrs={'class': 'form-control'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    #COLOCA A VIRGULA NO PREÇO AO INVES DO PONTO 
    def clean_preco(self):
        preco_str = self.cleaned_data.get('preco')
        if preco_str:
            preco_str = preco_str.replace(',', '.')
            try:
                preco_decimal = Decimal(preco_str)
                return preco_decimal
            except:
                raise forms.ValidationError("Informe um valor numérico válido (ex: 78,90)")
        raise forms.ValidationError("Este campo é obrigatório.")

#------------------------------------------------------------------------------------
class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nome'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cargo'}),
            'telefone1': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

   
#------------------------------------------------------------------------------------

ESTADOS_BRASILEIROS = [
    ('AC', _('Acre')),
    ('AL', _('Alagoas')),
    ('AP', _('Amapá')),
    ('AM', _('Amazonas')),
    ('BA', _('Bahia')),
    ('CE', _('Ceará')),
    ('DF', _('Distrito Federal')),
    ('ES', _('Espírito Santo')),
    ('GO', _('Goiás')),
    ('MA', _('Maranhão')),
    ('MT', _('Mato Grosso')),
    ('MS', _('Mato Grosso do Sul')),
    ('MG', _('Minas Gerais')),
    ('PA', _('Pará')),
    ('PB', _('Paraíba')),
    ('PR', _('Paraná')),
    ('PE', _('Pernambuco')),
    ('PI', _('Piauí')),
    ('RJ', _('Rio de Janeiro')),
    ('RN', _('Rio Grande do Norte')),
    ('RS', _('Rio Grande do Sul')),
    ('RO', _('Rondônia')),
    ('RR', _('Roraima')),
    ('SC', _('Santa Catarina')),
    ('SP', _('São Paulo')),
    ('SE', _('Sergipe')),
    ('TO', _('Tocantins')),
]


class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['nome', 'endereco', 'cidade', 'estado', 'responsaveis', 'data_inicio', 'data_termino', 'status', 'tags']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'responsaveis': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=ESTADOS_BRASILEIROS, attrs={'class': 'form-select'}),
        }

#------------------------------------------------------------------------------------

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StatusClienteForm(forms.ModelForm):
    class Meta:
        model = StatusCliente
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }


#--------------------------------------------------------------------------------
class ClienteForm(forms.ModelForm):
    class Meta:
       model = Cliente
       fields = '__all__'
       widgets = {
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=[
                ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'),
                ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'),
                ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'),
                ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
                ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'),
                ('SE', 'SE'), ('TO', 'TO')
            ], attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'})

         }
