from django.db import models

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
    email = models.EmailField(blank=True)
    observacoes = models.TextField(blank=True)

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
