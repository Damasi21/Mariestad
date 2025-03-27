from django.db import models


#status
class Status(models.Model):
    nome_status = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.nome_status
    
#----------------------------------------------------------------------
#tags
class Tag(models.Model):
    nome_tag = models.CharField(max_length=30, unique=True)  # Nome único para evitar duplicações

    def __str__(self):
        return self.nome_tag
#----------------------------------------------------------------------
#Produtos

class Produto(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    descricao = models.TextField(max_length=100)
    unidade = models.CharField(
        max_length=15,
        choices=[
            ('Unidade', 'Unidade'),
            ('Pacote', 'Pacote'),
            ('Caixa', 'Caixa'),
            ('Metro', 'Metro')
        ]
    )
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ncm = models.CharField(max_length=10, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"
    
 #----------------------------------------------------------------------
#Obras
    
class Obra(models.Model):
    nome_obra = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    def __str__(self):
        return self.nome_obra
    
#---------------------------------------------------------------------
#Contatos 

class Contato(models.Model):
    nome = models.CharField(max_length=70)
    telefone1 = models.CharField(max_length=20, blank=True, null=True)
    telefone2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
    

