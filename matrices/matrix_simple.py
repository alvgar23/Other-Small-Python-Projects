# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:10:45 2020

@author: alvar
"""

def matrix(rows, columns):
    
    matriz = []
    for fil in range(rows):
        matriz.append([])
        for col in range(columns):
            matriz[fil].append("_")
    
    for filas in matriz:
        print(filas)
    
    print()
    
    return matriz



def fill_matrix(matriz):
    
    for fil in range(len(matriz)):
        print("Fill the row", fil)
        for col in range(len(matriz[fil])):
            print("Row", fil, "& Column", col,": ")
            matriz[fil][col] = float(input("==> "))
            print()

    for fila in matriz:
        print("[", end=" ")
        for elemento in fila:
            print("{:8.2f}".format(elemento), end=" ")
        print("]")



rows = int(input("Rows: "))
columns = int(input("Columns: "))

matriz = matrix(rows, columns)
fill_matrix(matriz)
