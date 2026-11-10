# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 01:52:20 2020

@author: alvar
"""


def pedir_denominadores():
    
    """
    Introducir por teclado denominadores para calcular su común denominador.
    Devuelve una lista con los denominadores
    """
    
    denominadores = int(input("Cuántos denominadores vas a introducir? "))
    list_denominadores = []
    
    for i in range(denominadores):
        numero = int(input("Introduce denominador: "))
        list_denominadores.append(numero)
    
    print(list_denominadores)
    
    return list_denominadores



def borrar_repetidos(list_denominadores):
    
    """
    Borra los repetidos de la lista y los ordena de mayor a menor
    """
    
    repetidos = []
    for i in range(len(list_denominadores)):
        for j in range(i+1, len(list_denominadores)):
            if list_denominadores[i] == list_denominadores[j]:
                repetidos.append(list_denominadores[i])
    
    print(repetidos)
    for i in repetidos:
        list_denominadores.remove(i)
    
    list_denominadores.sort(reverse=True)
    print(list_denominadores)
    
    return list_denominadores



def reducir(list_denominadores):
    
    """
    Divide todos los números de la lista entre sí y elimina aquellos que
    puedan simplificarse (ejemplo, 4 y 2, elimina 2, 16 y 8, elimina 8)
    """
    
    borrar = []
    for i in range(len(list_denominadores)):
        for j in range(i+1, len(list_denominadores)):
            if list_denominadores[i] % list_denominadores[j] == 0:
                borrar.append(list_denominadores[j])
    
    for i in borrar:
        if i in list_denominadores:
            list_denominadores.remove(i)
    print(list_denominadores)
    
    return list_denominadores
    


def simplificar(list_denominadores):
    
    """
    Divide los denominadores pares entre 2, una sola vez.
    """
    
    for i in range(len(list_denominadores)):
        if int(list_denominadores[i]) % 2 == 0:
            list_denominadores[i] = int(list_denominadores[i] / 2)
        
    print(list_denominadores)
    
    return list_denominadores



def mcm_fun(list_denominadores):
    
    """
    Multiplica los números que quedan en lalista entre sí, 
    pues es el común denominador
    """
    
    mcm = 1
    for i in list_denominadores:
        mcm = mcm * i
    return mcm

den = pedir_denominadores()
denominadores = borrar_repetidos(den)
reducida = reducir(denominadores)
simplificada = simplificar(reducida)
mcm = mcm_fun(simplificada)
print(mcm)