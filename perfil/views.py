from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum
from datetime import datetime

from .models import Conta, Categoria
from extrato.models import Valores
from .utils import calcula_total, calcula_equilibrio_financeiro


def home(request):
    context = {}
    contas = Conta.objects.all()
    total_contas = calcula_total(contas, 'valor')
    
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()
    
    
    context['gastos_essenciais'] = int(percentual_gastos_essenciais)
    context['gastos_nao_essenciais'] = int(percentual_gastos_nao_essenciais)
    context['contas'] = contas
    context['contas'] = contas
    context['entradas'] = entradas
    context['saidas'] = saidas
    context['total_contas'] = total_contas
    context['total_entradas'] = total_entradas
    context['total_saidas'] = total_saidas
    return render(request, 'home.html', context)

def gerenciar(request):
    context = {}
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    # total_contas = 0
    # total_contas = contas.aggregate(Sum('valor'))['valor__sum']
    total_contas = calcula_total(contas, 'valor')
    # for conta in contas:
    #     total_contas += conta.valor
    context['contas'] = contas
    context['total_contas'] = total_contas
    context['categorias'] = categorias
    return render(request, 'gerenciar.html', context)

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    conta = Conta(
        apelido = apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso')
    # return HttpResponse(conta)
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    
    if len(nome.strip()) == 0 or isinstance(essencial, bool):
        messages.add_message(request, constants.ERROR, 'Preencha os campos corretamente')
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    messages.add_message(request, constants.SUCCESS, 'Categoria atualizada com sucesso')
    categoria.save()

    return redirect('/perfil/gerenciar/')

def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valores.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})