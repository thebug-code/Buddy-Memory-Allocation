# Programa que simula un manejador de memoria que implementa el buddy system.
#
# EL programa cumple las siguientes caracteristicas:
#
# 1. Recibe como argumento la cantidad de bloques de memoria que manejará.
# 2. Una vez iniciado el programa, pedirá repetidamente al usuario una acción para pro-
# ceder. Tal acción puede ser:
#
#   i. RESERVAR <cantidad> <nombre>
#
#   Esto representa una reserva de espacio de <cantidad> bloques, asociados al identifi-
#   cador <nombre>.
#
#   El programa reporta un error e ignora la acción si <nombre> ya tiene memoria
#   reservada o no hay un espacio libre contiguo suficientemente grande como para
#   satisfacer la petición.
#   
#   ii. LIBERAR <nombre>
#   
#   Esto representa una liberación del espacio que contiene el identificador <nombre>.
#   El programa reporta un error e ignorar la acción si <nombre> no tiene memoria
#   reservada
#   
#   iii. MOSTRAR
#
#   Muestra una representación gráfica (en texto) de las listas de bloques libres,
#   así como la información de nombres y la memoria que tienen asociada a los mismos.
#
#   iv. SALIR
#   
#   salir del simulador.
#
#   Al finalizar la ejecución de cada acción, el programa pide la siguiente acción
#   al usuario.
