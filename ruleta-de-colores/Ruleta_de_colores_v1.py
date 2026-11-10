# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 00:03:43 2020

@author: alvar
"""
from random import choice

colores_iniciales = ["rojo", "blanco", "gris", "verde", "marron", "amarillo",
                     "negro", "naranja", "azul", "morado", "rosa", "marron"]
colores = [0,1,2,3,4] 

for i in range(0,5):
    color_random = choice(colores_iniciales)
    if color_random not in colores:
        colores[i] = color_random
    else:
        while color_random in colores:
            color_random = choice(colores_iniciales)
        colores[i] = color_random
    
probando = True
puntos = 0
lista_aciertos = []

while probando:
    color = input("Dime un color: ")
    if color in colores and color not in lista_aciertos:
        probando = True
        puntos += 1
        lista_aciertos = lista_aciertos + [color]
        print("Has acertado. Puntos: ", puntos)
        
        if len(lista_aciertos) == 5:
            print("Enhorabuena, has ganado!!")
            probando = False
        
    elif color not in colores: 
        probando = False
        print("Fallaste, has conseguido ", puntos, "puntos")
        print("los colores eran:", colores)
        
    elif color in lista_aciertos:
        probando = False
        print("Oops, ese color ya lo has dicho. Pierdes con ",puntos,"puntos")
        print("los colores eran:", colores)
    print("Aciertos: ", lista_aciertos)