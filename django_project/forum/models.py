from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Postagem(models.Model):
    mensagem = models.TextField()
    data_publicacao = models.DateTimeField(default=timezone.now)
    data_edicao = models.DateTimeField(null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default='')

    PERGUNTA = 'P'
    DISCUSSAO = 'D'

    TIPO_DE_POSTAGEM_CHOICES =[
        (PERGUNTA, 'Pergunta'),
        (DISCUSSAO, 'Discussão'),
    ]

    tipo = models.CharField(
        max_length=1,
        choices=TIPO_DE_POSTAGEM_CHOICES,
        default=DISCUSSAO
    )

    def get_absolute_url(self):
        return reverse('postagem-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'[{self.tipo}] {self.id} - {self.titulo}'

    def get_respostas(self):
        return Resposta.objects.filter(postagem=self)

    def responder(self, resposta):
        for r in self.get_respostas():
            r.is_resposta = False
            r.save()
        resposta.is_resposta = True
        resposta.save()

    @property
    def respondida(self):
        return self.get_respostas().filter(is_resposta=True).exists()


class Resposta(models.Model):
    mensagem = models.TextField(null=True, blank=True)
    data_publicacao = models.DateTimeField(default=timezone.now)
    data_edicao = models.DateTimeField(null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    # esta variavel representa a qual postagem esta resposta corresponde
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE,
                                 related_name='respostas')
    # esta variavel representa se esta resposta corresponde a alguma pergunta
    is_resposta = models.BooleanField(default=False, null=True)

    def get_absolute_url(self):
        return reverse('postagem-detail', kwargs={'pk': self.postagem.id})

    class Meta:
        ordering = ['-is_resposta','-data_publicacao']