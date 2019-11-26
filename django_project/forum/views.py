from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django.http import HttpResponse
from forum.models import *

def home(request):

    postagens = Postagem.objects.all().order_by('data_publicacao')
    #postagens = postagens | Discussao.objects.all()

    context = { 'postagens': postagens }
    return render(request, 'forum/home.html', context)


class PostagemListView(ListView):
    model = Postagem
    template_name = 'forum/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'postagens'
    ordering = ['-data_publicacao']


class PostagemDetailView(DetailView):
    model = Postagem


class PostagemCreateView(CreateView, LoginRequiredMixin):
    model = Postagem
    template_name = 'forum/postagem_form.html'
    fields = ['titulo', 'tipo','mensagem']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PostagemUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Postagem
    template_name = 'forum/postagem_form.html'
    fields = ['titulo', 'mensagem']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.autor:
            return True
        return False


class PostagemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Postagem
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.autor:
            return True
        return False


class RespostaCreateView(CreateView, LoginRequiredMixin):
    model = Resposta
    template_name = 'forum/postagem_detail.html'
    fields = ['mensagem', 'postagem']

    def form_valid(self, form):
        print(form.instance.mensagem)
        form.instance.autor = self.request.user
        return super().form_valid(form)


class RespostaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resposta
    
    def test_func(self):
        resp = self.get_object()
        self.success_url = f'/postagem/{resp.postagem.id}'
        if self.request.user == resp.autor:
            return True
        return False


class RespostaUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Resposta
    template_name = 'forum/postagem_form.html'
    fields = ['mensagem']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.data_edicao = timezone.now()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        self.success_url = f'/postagem/{resp.postagem.id}'
        if self.request.user == post.autor:
            return True
        return False


class PostagemMarcarResposta(View):

    def post(self, request, *args, **kwargs):
        pergunta = self.request.POST.get('id_pergunta', False)
        resposta = self.request.POST.get('id_resposta', False)
        
        pergunta = Postagem.objects.get(id=pergunta)

        if pergunta and resposta:
            resposta = Resposta.objects.get(id=resposta)

            pergunta.responder(resposta)

            messages.success(request, f'Pergunta respondida com sucesso!')
        
        return redirect(pergunta)


def about(request):
    context = { 'titulo': 'Sobre'}
    return render(request, 'forum/sobre.html', context)