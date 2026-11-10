# Other Small Python Projects

Colección de **seis ejercicios y pequeños programas en Python**, creados originalmente durante 2020 para practicar programación. Algunos se retomaron en noviembre de 2025 con nuevas versiones, incluida una interfaz gráfica. Se conservan los scripts originales para mostrar cómo fueron evolucionando.

No es una única aplicación: cada carpeta contiene un programa independiente. Esta documentación describe lo que hace el código, sin reescribirlo ni dar por probado su funcionamiento actual.

## Proyectos

| Proyecto | Archivos | Qué hace |
| --- | --- | --- |
| [Ruleta de colores](ruleta-de-colores/) | `Ruleta_de_colores_v1.py`, `v2.py`, `v3.py` | Juego para descubrir cinco colores elegidos al azar. |
| [Adivinar contraseña](adivinar-contrasena/) | `adivinar_contrasena_v1.py`, `v2.py` | Validación de contraseñas y demostración del coste de buscar combinaciones. |
| [Común denominador](comun-denominador/) | `comun_denominador.py` | Ejercicio para intentar obtener un denominador común a partir de varios números. |
| [Matrices](matrices/) | `matrix_simple.py` | Creación de matrices e introducción de sus valores por consola. |
| [Números repetidos](numeros-repetidos/) | `numero_repetido.py` | Dos formas de localizar números duplicados en una lista aleatoria. |
| [Conversor](conversor/) | `simple_converter.py` | Conversión entre pulgadas y centímetros, y entre segundos y horas/minutos/segundos. |

## Historia y evolución

### 1. Ruleta de colores

- **[v1](ruleta-de-colores/Ruleta_de_colores_v1.py) — octubre de 2020.** Juego de consola en español. Selecciona cinco colores sin repetir; el jugador intenta adivinarlos uno por uno. Un fallo o repetir un acierto termina la partida.
- **[v2](ruleta-de-colores/Ruleta_de_colores_v2.py) — actualización de noviembre de 2025.** Mantiene el juego en consola, pasa los mensajes al inglés y utiliza `random.sample` para escoger los colores únicos.
- **[v3](ruleta-de-colores/Ruleta_de_colores_v3.py) — noviembre de 2025.** Añade una ventana con **Tkinter**, botones de colores, puntuación, vidas, dificultad y nueva partida. Las dificultades ofrecen 5, 3, 2 o 0 vidas según la opción seleccionada.

### 2. Adivinar contraseña

- **[v1](adivinar-contrasena/adivinar_contrasena_v1.py) — noviembre de 2020.** Pide una contraseña, comprueba longitud, números, mayúsculas, minúsculas y símbolos, y después intenta encontrarla mediante ocho bucles anidados que recorren combinaciones. Es una demostración educativa de búsqueda exhaustiva, no una herramienta práctica para recuperar contraseñas.
- **[v2](adivinar-contrasena/adivinar_contrasena_v2.py) — noviembre de 2025.** Introduce una interfaz **Tkinter** para validar contraseñas y **simular** una búsqueda por fuerza bruta. Calcula el espacio de combinaciones y estima tiempos sin recorrer realmente todas las posibilidades.

### 3. Común denominador

**[comun_denominador.py](comun-denominador/comun_denominador.py) — diciembre de 2020.** Solicita varios denominadores, elimina repetidos, intenta reducir múltiplos y calcula un resultado mediante multiplicaciones. Es un ejercicio de operaciones con listas y divisibilidad.

**Limitación:** el procedimiento implementado no garantiza calcular correctamente el mínimo común múltiplo de cualquier conjunto de números. El resultado debe interpretarse como la salida del algoritmo original, no como un cálculo matemático fiable para todos los casos.

### 4. Matrices

**[matrix_simple.py](matrices/matrix_simple.py) — diciembre de 2020.** Pide el número de filas y columnas, crea una matriz inicialmente rellena de guiones bajos y solicita cada valor numérico. Finalmente imprime la matriz con dos decimales.

### 5. Números repetidos

**[numero_repetido.py](numeros-repetidos/numero_repetido.py) — noviembre de 2020.** Genera cien números aleatorios entre 0 y 1000 y busca duplicados mediante dos enfoques: comparaciones entre parejas de posiciones y seguimiento de valores ya encontrados.

### 6. Conversor

**[simple_converter.py](conversor/simple_converter.py) — noviembre de 2020.** Menú de consola con cuatro operaciones: pulgadas a centímetros, centímetros a pulgadas, segundos a horas/minutos/segundos y horas/minutos/segundos a segundos.

## Ejecución

Los programas están escritos en Python y se ejecutan **por separado** desde la raíz del repositorio. Por ejemplo:

```bash
python ruleta-de-colores/Ruleta_de_colores_v1.py
python ruleta-de-colores/Ruleta_de_colores_v3.py
python adivinar-contrasena/adivinar_contrasena_v2.py
python comun-denominador/comun_denominador.py
python matrices/matrix_simple.py
python numeros-repetidos/numero_repetido.py
python conversor/simple_converter.py
```

Los ejercicios de consola utilizan módulos incluidos con Python. Las versiones gráficas usan **Tkinter**, que debe estar disponible en la instalación de Python.

## Observaciones

- En la primera versión de **Adivinar contraseña**, la comprobación de longitud exige exactamente ocho caracteres, aunque los mensajes de error mencionan cuatro. También hay variables de validación cuyo estado no se reinicia completamente entre intentos.
- La búsqueda exhaustiva de esa primera versión puede requerir un tiempo descomunal; no conviene ejecutarla esperando un resultado rápido.
- La segunda versión de **Adivinar contraseña** es una simulación de tiempo y posiciones, no un ataque real.
- En **Ruleta de colores v3**, la dificultad «Impossible» empieza con cero vidas, pero el código no termina automáticamente la partida antes del primer intento.
- En **Conversor**, el texto del menú de la cuarta opción dice «to hours», aunque la función convierte a segundos.
- **Común denominador** contiene simplificaciones que no son matemáticamente válidas en todos los casos.

Estas observaciones proceden de una **lectura del código**. No se han ejecutado pruebas ni corregido los ejercicios: el objetivo es preservar el trabajo original y documentar su evolución.

## Estado

Repositorio histórico de prácticas de Python. Las versiones iniciales son de 2020 y las actualizaciones de Ruleta de colores y Adivinar contraseña están fechadas en noviembre de 2025. Los archivos se han agrupado por proyecto sin cambiar su contenido.
