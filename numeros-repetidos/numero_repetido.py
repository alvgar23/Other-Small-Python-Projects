# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:52:23 2020

@author: alvar
"""

# Creamos lista aleatoria y comprobamos si algún número está repetido
from random import randint
lista = []

for i in range(100):
    aleatorio = randint(0,1000)
    lista.append(aleatorio)
print(lista)

# forma 1:
    
for i in range(len(lista)):
    #comparamos cada número con todos los que vienen después de sí mismo
    for j in range(i+1, len(lista)):
        if lista[i] == lista[j]:
            print("El",lista[i],"está repetido")


# forma 2:

no_repetidos = []
repetidos = []

for n in range(len(lista)):
    if lista[n] not in no_repetidos:
        no_repetidos.append(lista[n])
    elif lista[n] in no_repetidos and lista[n] not in repetidos:
        repetidos.append(lista[n])
print("Los repetidos son:", repetidos)           