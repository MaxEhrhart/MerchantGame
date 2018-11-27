# -*- encoding: utf-8 -*-
from collections import namedtuple, Iterable
from operator import itemgetter
from itertools import groupby
from sys import exit, version_info


CAMINHO_RECURSOS=r"./recursos.csv"
CAMINHO_EQUIPAMENTOS_E_MATERIAIS=r"./equipamentos.csv"
Item = namedtuple("Item", ["nome", "tipo", "receita"])
# nome = nome do item.
# tipo = "Recurso" ou "Equipamento/Material".
# receita = lista items necessarios para criação do item, se recurso, None.

if version_info > (3, 0):
    raw_input = input


def flatten(l):
    for el in l:
        if isinstance(el, list) and not isinstance(el, (str, bytes)):
            for sub in flatten(el):
                yield sub
        else:
            yield el


def receita_item(ITEM, receita,delimiter="|"):
    receita = [tuple(item.split("x ",1)) for item in receita.split(delimiter)]
    #print receita
    items = []

    for item in receita:
        quantidade = int(item[0])
        nome_item = item[1]
        for _ in range(quantidade):
            items.append(ITEM[nome_item])
    receita = items
    return receita


def carrega_dicionario_de_itens(ITEM):

    with open(CAMINHO_RECURSOS,"r") as f:
        itens_recursos = f.readlines()[1:]
        f.close()

    for linha in itens_recursos:
        nome_item = linha.rstrip("\n").split(";")[0]
        ITEM[nome_item] = Item(nome=nome_item, tipo="Recurso", receita=None)
        del linha

    with open(CAMINHO_EQUIPAMENTOS_E_MATERIAIS,"r") as f:
        itens_equipamentos = f.readlines()[1:]
        f.close()

    for linha in itens_equipamentos:
        linha=linha.rstrip("\n")
        nome_item, materiais = linha.split(";")
        ITEM[nome_item] = Item(nome=nome_item, tipo="Equipamento/Material", receita=receita_item(ITEM,materiais))

        del linha

    return



# FAZE RAGRUPADO
def print_list(lst, level=0):
    print('    ' * (level - 1) + '+---' * (level > 0) + lst[0].nome)
    for l in lst[1:]:
        aux = []
        if type(l) is list:
            print_list(l, level + 1)
        else:
            aux.append(l.nome)
            #print('    ' * level + '+---' + l.nome)
    if len(aux) > 0:
        print(aux)
        imprime_item_agrupado(aux,tab=level+1)


def imprime_item_agrupado(lista,tab=0):
    d = {}
    for item in lista:
        if item not in d:
            d[item] = 0
        d[item] += 1
    for item in d.keys():
        print("{0}{1}x {2}".format(" "*tab*4, d[item], item))


def itens_receita(item,tab=0,imprimir=True):
    lista_itens = []
    if imprimir:
        print("{0}{1}x {2}".format(" "*tab*4, 1, item.nome))
    if item.tipo=="Recurso":
        return item
    else:
        lista_itens = [item]
        for item in item.receita:
            lista_itens += [itens_receita(item,1+tab)]
        return lista_itens


def receita_recursos(item):
    if item.tipo=="Recurso":
        return (item.nome,1)
    else:
        return [receita_recursos(item) for item in item.receita]


if __name__ == "__main__":
    ITEM = {}
    carrega_dicionario_de_itens(ITEM)
    entrada = raw_input()

    print("Recursos "+ITEM[entrada].nome + ":")
    recursos = list(flatten(receita_recursos(ITEM[entrada])))
    d = {}
    for k, v in recursos:
        if k not in d:
            d[k] = 0
        d[k] += v

    for recurso in d.items():
        print("    {0:02d}x {1}".format(recurso[1], recurso[0]))

    print("\n")
    print("Receita " + ITEM[entrada].nome + ":")
    receita = itens_receita(ITEM[entrada])
    print_list(receita)

