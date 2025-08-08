from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Opções de família
FAMILIAS = [
    ("Quimicos", "Químicos"),
    ("Fibras", "Fibras"),
    ("Aditivos", "Aditivos"),
]

class Produto(models.Model):
    codigo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255)
    ncm = models.CharField(max_length=20, blank=True, null=True)
    unidade = models.CharField(max_length=20)
    preco = models.DecimalField(max_digits=10, decimal_places=3)
    foto = models.ImageField(upload_to='produtos/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    familia = models.CharField(max_length=30, choices=FAMILIAS, blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class Status(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Tag(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

#-------------------------------------------------------------------------
class StatusCliente(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        db_table = 'core_status_cliente'

    def __str__(self):
        return self.nome
#-------------------------------------------------------------------------

class Cliente(models.Model):
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=150)
    nome_fantasia = models.CharField(max_length=150, blank=True)
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    observacoes = models.TextField(blank=True)
    vendedores = models.ManyToManyField("Vendedor", blank=True, related_name="clientes")  # ✅ NOVO CAMPO


    status = models.ForeignKey("StatusCliente", on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes")
    tags = models.ManyToManyField("Tag", blank=True, related_name="clientes")

    class Meta:
        db_table = 'core_cliente'

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"

#-------------------------------------------------------------------------

class Contato(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE, related_name="contatos", null=True, blank=True)
    nome = models.CharField(max_length=80)
    cargo = models.CharField(max_length=50)
    telefone1 = models.CharField(max_length=20, blank=True)
    telefone2 = models.CharField(max_length=20, blank=True)
    email_contato = models.EmailField(max_length=100, blank=True)
    observacoes = models.TextField(blank=True)

    PERFIL_CHOICES = [
        ('DOMINANTE', 'Dominante'),
        ('INFLUENTE', 'Influente'),
        ('ESTAVEL', 'Estável'),
        ('CONFORME', 'Conforme'),
    ]

    perfil = models.CharField(
        max_length=20,
        choices=PERFIL_CHOICES,
        default='INFLUENTE',
        verbose_name='Perfil'
    )


    def __str__(self):
        return self.nome

#-------------------------------------------------------------------------

class Obra(models.Model):
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=200)
    responsaveis = models.ManyToManyField("Cliente", blank=True,related_name="obras")
    data_inicio = models.DateField(null=True, blank=True)
    data_termino = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True, related_name='obras')
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, choices=[
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'),
        ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'),
        ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'),
        ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'),
        ('SE', 'SE'), ('TO', 'TO')
    ], blank=True, null=True)
    observacoes_obra = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class ObraAnexo(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='obras/anexos/')

    class Meta:
        db_table = 'core_obra_anexo'

    def __str__(self):
        return self.arquivo.name
#-------------------------------------------------------------------------

class Vendedor(models.Model):
    nome = models.CharField(max_length=60)
    funcao = models.CharField(max_length=60)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome
    
#------------------------PROPOSTA-------------------------------------------------

class Proposta(models.Model):
    numero = models.CharField(max_length=20, default='TEMP')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True)
    contato = models.ForeignKey(Contato, on_delete=models.SET_NULL, null=True, blank=True)
    perfil_contato = models.CharField(max_length=20, blank=True)

    STATUS_OPCOES = [
        ('aberto', 'Em Aberto'),
        ('fechada', 'Fechada (Pedido)'),
        ('standby', 'Stand By'),
        ('perdida', 'Perdida'),
        ('cancelada', 'Cancelada'),
    ]
    status_proposta = models.CharField(max_length=20, choices=STATUS_OPCOES, default='aberto')

    transportadora = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='propostas_transportadora')
    tipo_frete = models.CharField(max_length=20, choices=[
        ('CIF', 'CIF'),
        ('FOB', 'FOB'),
        ('Terceiros', 'Terceiros')
    ], blank=True)

    peso_liquido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    quantidade_volumes = models.PositiveIntegerField(null=True, blank=True)

    frete_tech4con = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    frete_cliente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    condicao_pagamento = models.CharField(max_length=100, blank=True, null=True)
    parcelas_condicao = models.CharField(max_length=255, blank=True, null=True)

    endereco_proposta = models.CharField(max_length=255, blank=True, null=True)
    numero_proposta = models.CharField(max_length=20, blank=True, null=True)
    complemento_proposta = models.CharField(max_length=100, blank=True, null=True)
    bairro_proposta = models.CharField(max_length=100, blank=True, null=True)
    cep_proposta = models.CharField(max_length=20, blank=True, null=True)
    cidade_proposta = models.CharField(max_length=100, blank=True, null=True)
    estado_proposta = models.CharField(max_length=2, choices=[
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'),
        ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'),
        ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'),
        ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'),
        ('SE', 'SE'), ('TO', 'TO'),
    ], blank=True, null=True)

    observacoes_proposta = models.TextField(blank=True, null=True)

    produtos_json = models.TextField(blank=True, null=True)  # ✅ Novo campo

    data_inclusao = models.DateTimeField(default=timezone.now)
    nome_entrega = models.CharField(max_length=100, blank=True, null=True)
    prazo_entrega = models.CharField(max_length=100, blank=True, null=True)



    def __str__(self):
        return f"Proposta {self.numero} - {self.cliente.nome_fantasia}"

    @property
    def total_produtos(self):
        import json
        try:
            produtos = json.loads(self.produtos_json or "[]")
            return sum(float(p.get("subtotal", 0)) for p in produtos)
        except:
            return 0
#------------------------LOGIN -------------------------------------------------

class UsuarioPersonalizado(AbstractUser):
    username = None  # <- desativa o campo padrão
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone']

    def __str__(self):
        return self.email
    
#------------------------PRODUTOS PROPOSTA-------------------------------------------------

class ProdutoProposta(models.Model):
    proposta = models.ForeignKey(Proposta, on_delete=models.CASCADE, related_name="produtos")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    unidade = models.CharField(max_length=10)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    observacao_produto_proposta = models.TextField(blank=True, null=True)
    imagem_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'core_produto_proposta'