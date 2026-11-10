# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 17:49:23 2020

@author: alvar
"""

valida = False
intentos = 5
numeros = False
longitud = False
especial = False
mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZÑ"
minusculas = "abcdefghijklmnopqrstuvwxyzñ"
especiales = "@#%&=&$*-+"
digitos = "0123456789"
may = False
minus = False

while valida == False:
    print("Tienes", intentos, "intentos.")
    contrasena = input("Introduce tu contraseña: ")
    
    # Un solo bloque para la longitud
    if len(contrasena) < 8:
        print("Contraseña demasiado corta. Debe tener al menos 4 caracteres")
        longitud = False
    elif len(contrasena) > 8:
        print("contrasena demasiado larga. No debe tener más de 4 caracteres")
        longitud = False
    else:
        longitud = True
    
    # bloque para números pero atentos a cuando sea falso (chequear final bucle)
    for i in range(0,10):
        if str(i) in contrasena:
            numeros = True
    if numeros == False:
        print("Tiene que haber al menos un número en la contraseña")
    
    # bloque para caracter especial
    for k in contrasena:
        if k in especiales:
            especial = True
    if especial == False:
        print("La contraseña debe incluir al menos un carácter especial", especiales)
        especial = False
    
    # bloque para tamaño 
    for j in contrasena:
        if j in mayusculas:
            may = True
        elif j in minusculas:
            minus = True    
    if may == False or minus == False:
        print("La contraseña debe contener una mayúscula y una minúscula")
        # aseguramos que may y minus sean False en caso de fallo
        may = False
        minus = False
    
    
    if longitud == True and numeros == True and especial == True and may == True and minus == True:
        print("Contraseña aceptada. Tu contraseña es:", contrasena )
        valida = True
    
    # restamos aquí los intentos antes del break
    intentos -= 1
    
    # evitamos que si acertamos en el último intento nos lo imprima añadiendo
    # valida a la condición
    if intentos == 0 and valida == False:
        print("No ha sido posible establecer la contraseña")
        break
    
    # inicializamos numeros a False por si fallamos
    # si no hacemos esto al entrar de nuevo al bucle tendremos numeros = True
    # y nos aceptaría contraseña sin número
    numeros = False


# Aquí tendremos el adivinador de contraseña que solo se activará si...
# ...si valida es True

from time import perf_counter, sleep

#Paramos 4 segundos para que nos de tiempo a ver el resultado de la primera parte
print("Procediendo a acertar la contraseña, espere por favor...")
sleep(4)

while valida == True:
    tiempo_inicial = perf_counter()
    nueva_contrasena = contrasena

    #Creamos una cadena con las opciones que podemos encontrar en la contrasena
    # la podemos recorrer 15 veces para encontrar los caracteres
    opciones = mayusculas + minusculas + especiales + digitos
    
    for a in opciones:
        for b in opciones:
            for c in opciones:
                for d in opciones:
                    for e in opciones:
                        for f in opciones:
                            for g in opciones:
                                for h in opciones:
                                    combinacion = str(a)+str(b)+str(c)+str(d)+str(e)+str(f)+str(g)+str(h)                                                         
                                    if combinacion == nueva_contrasena:
                                        break
                                if combinacion == nueva_contrasena:
                                    break
                            if combinacion == nueva_contrasena:
                                break
                        if combinacion == nueva_contrasena:
                            break
                    if combinacion == nueva_contrasena:
                        break
                if combinacion == nueva_contrasena:
                    break
            if combinacion == nueva_contrasena:
                break
        if combinacion == nueva_contrasena:
            break
    
                                                     
    #para hallar el tiempo final de ejecución
    tiempo_final = perf_counter()
    
    print("La contraseña es:",nueva_contrasena)
    print("Contraseña acertada en", tiempo_final-tiempo_inicial, "segundos.") 
    print((tiempo_final-tiempo_inicial)/60)
    
    #provisional break para salir del bucle
    break     