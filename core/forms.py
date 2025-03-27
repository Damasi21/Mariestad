from django import forms
from .models import Produto
from .models import Obra
from .models import Contato


#-----------------PRODUTO ------------------------------------------------------------------------

class ProdutoForm(forms.ModelForm):
    produto_id = forms.CharField(widget=forms.HiddenInput(), required=False)  # Campo oculto para edição

    class Meta:
        model = Produto
        fields = ['produto_id', 'foto', 'codigo', 'descricao', 'ncm', 'unidade', 'preco', 'observacoes']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'ncm': forms.TextInput(attrs={'class': 'form-control'}),
            'unidade': forms.Select(attrs={'class': 'form-select'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

#-----------------OBRA ------------------------------------------------------------------------

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['nome_obra', 'localizacao', 'cidade', 'estado']
        widgets = {
            'nome_obra': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nome_obra'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_localizacao'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_estado'}),
        }


#--------------------CONTATO---------------------------------------------------------------------

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'telefone1', 'telefone2', 'email', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone1': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
