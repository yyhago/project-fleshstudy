from django.shortcuts import render,redirect,get_object_or_404
from .models import Categoria, Flashcard, Desafio ,FlashcardDesafio
from django.http import HttpResponse
from django.contrib.messages import constants
from django.contrib import messages

def novo_flashcard(request):
  if not request.user.is_authenticated:
    return redirect('/usuarios/logar')
  
  if request.method == "GET":
    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    flashcards = Flashcard.objects.filter(user=request.user)

    categoria_filtrar = request.GET.get('categoria')
    dificuldade_filtrar = request.GET.get('dificuldade_filtrar')

    if categoria_filtrar:
      flashcards = flashcards.filter(categoria__id=categoria_filtrar)
    if dificuldade_filtrar:
      flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)

    return render(request, 'novo_flashcard.html',{'categorias': categorias, 'dificuldades': dificuldades, 'flashcards': flashcards});
  elif request.method == 'POST':
    pergunta = request.POST.get('pergunta')
    resposta = request.POST.get('resposta')
    categorias = request.POST.get('categoria')
    dificuldades = request.POST.get('dificuldade')

    if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
      messages.add_message(
      request,constants.ERROR,'Preencha os campos de pergunta e resposta',)
      return redirect('/flashcard/novo_flashcard')
      
    flashcard = Flashcard(
      user=request.user,
      pergunta=pergunta,
      resposta=resposta,
      categoria_id=categorias,
      dificuldade=dificuldades,
      )
      
    flashcard.save()
    messages.add_message(
    request, constants.SUCCESS, 'Flashcard criado com sucesso'
    )
    return redirect('/flashcard/novo_flashcard')
  
def deletar_flashcard(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)
    if flashcard.user != request.user:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para excluir este FlashCard.')
    else:
        flashcard.delete()
        messages.add_message(request, constants.SUCCESS, 'Seu FlashCard foi deletado com Sucesso!')

    return redirect('/flashcard/novo_flashcard/')

def iniciar_desafio(request):
  if request.method == "GET":
      categorias = Categoria.objects.all()
      dificuldades = Flashcard.DIFICULDADE_CHOICES
      return render (request, 'iniciar__desafio.html', {'categorias': categorias, 'dificuldades': dificuldades})

  elif request.method == "POST":
    titulo = request.POST.get('titulo')
    categorias = request.POST.getlist('categoria')
    dificuldade = request.POST.get('dificuldade')
    qtd_perguntas = request.POST.get('qtd_perguntas')

    desafio = Desafio(
      user=request.user,
      titulo=titulo,
      quantidade_perguntas=qtd_perguntas,
      dificuldade=dificuldade
    )

    desafio.save()

    for categoria in categorias:
       desafio.categoria.add(categoria)

    flashcards = Flashcard.objects.filter(user=request.user).filter(dificuldade=dificuldade).filter(categoria_id__in=categorias).order_by('?')
    if flashcards.count() < int(qtd_perguntas):
       return redirect('/flashcard/iniciar_desafio/')

    flashcards = flashcards[: int(qtd_perguntas)]

    return HttpResponse("Teste")