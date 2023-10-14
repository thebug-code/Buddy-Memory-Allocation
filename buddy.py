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


from math import floor, ceil, log2


class MemoryManager:

    def __init__(self, memory_block_num: int):
        # Verifica que la cantidad de bloques de memoria sea un entero positivo
        # y que sea una potencia de dos
        if memory_block_num < 1:
            raise ValueError("El numero de bloques de memoria debe ser un entero positivo")
        elif not (memory_block_num & (memory_block_num - 1) == 0):
            raise ValueError("El numero de bloques de memoria debe ser una potencia de dos")

        max_pow_of_two = ceil(log2(memory_block_num))

        # Lista de listas de tuplas para trackear los bloques de memoria libres
        # block_list = [[]] * max_pow_of_two
        block_list = [[]]
        for i in range(max_pow_of_two):
            block_list += [[]]
        
        # El primer bloque de memoria libre es el bloque completo
        block_list[max_pow_of_two].append((0, memory_block_num - 1))

        # Propiedades de la clase
        self.block_list_s = block_list
        self.memory_block_num_s = memory_block_num
        self.name_list = {}

    def run_simulation(self):
        memory_block_num = self.memory_block_num_s
        print("Manejador de memoria con el algoritmo Buddy System\n")
        print("Hay {} bloques de memoria\n".format(memory_block_num))
        self.memory_block_num_s = memory_block_num

        # Inicia el ciclo de simulacion
        while True:
            action = input("Ingrese una accion: ")
            param = action.split(" ")
            first_param = param[0].upper()

            match first_param:
                case "LIBERAR":
                    if len(param) == 2:
                        # Si el nombre existe, se libera el espacio
                        if param[1] in self.name_list:
                            self.buddy_free(param[1])
                        else:
                            print("Error: El nombre no existe")
                    else:
                        print("Error: Los parametros no son validos, debe ser LIBERAR <nombre>")

                case "RESERVAR":
                    if len(param) == 3 and param[1].isdigit():
                        # Si el nombre no existe, se reserva el espacio
                        if param[1] not in self.name_list:
                            self.buddy_alloc((int(param[1]), param[2]))
                        else:
                            print("Error: El nombre ya existe")
                    else:
                        print("Error: Los parametros no son validos, debe ser RESERVAR <cantidad> <nombre>")

                case "MOSTRAR":
                    self.display()

                case "SALIR":
                    break

                case _:
                    print("Error: La accion no es valida")


    def buddy_alloc(self, cnt: int, name: str):
        block_list_s = self.block_list_s

        # Verifica que cnt sea un entero
        if not isinstance(cnt, int):
            print("Error: Cantidad debe ser un entero")
            return
        elif cnt < 1:
            print("Error: Cantidad debe ser un entero positivo")
            return

        # Busca el primer bloque libre del tamaño correcto
        listToFit = floor(ceil(log2(cnt)))

        # Si hay un bloque libre del tamaño correcto, se reserva el espacio
        if len(block_list_s[listToFit]) != 0:
            # Elimina el bloque de la lista de bloques libres
            allocatedBlock = block_list_s[listToFit].pop(0)
            # Agrega el bloque a la lista de bloques reservados con el nombre
            self.name_list[name] = allocatedBlock
            print("\nEl bloque {} fue reservado en {}\n".format(name, allocatedBlock))
            return

        i = listToFit + 1
        
        # Si no hay un bloque libre del tamaño correcto, busca un bloque mas grande
        while i < len(block_list_s) and len(block_list_s[i]) == 0:
            i += 1

        if i == len(block_list_s):
            print("No hay bloques libres del tamaño correcto")
            return

        # Elimina el bloque de la lista de bloques libres
        blockToSplit = block_list_s[i].pop(0)
        i -= 1

        # Separa el bloque en dos partes y las agrega a la lista de bloques
        # libres. La primera parte es el bloque a dividir o a reservar y la
        # segunda parte es el nuevo bloque libre
        while i >= listToFit:
            lb = blockToSplit[0]
            rb = blockToSplit[1]

            new_block1 = (lb, lb + (rb - lb) // 2)
            new_block2 = (lb + (rb - lb + 1) // 2, rb)

            block_list_s[i].append(new_block1)
            block_list_s[i].append(new_block2)

            blockToSplit = block_list_s[i].pop(0)
            i -= 1

        print("\nEl bloque {} fue reservado en {}\n".format(name, blockToSplit))

        self.name_list[name] = blockToSplit


    def buddy_free(self, name: str):
        block_list_s = self.block_list_s
        name_list = self.name_list

        # Verifica que el nombre exista
        if name not in self.name_list:
            print("Error: Solicitud de liberacion invalida, el nombre: {} no esta reservado".format(name))
            return

        lb = name_list[name][0]
        rb = name_list[name][1]
        block_size = rb - lb + 1

        # Obtiene la lista que trackea los bloques libres de este tamaño
        list_to_free = int(ceil(log2(block_size)))
        block_list_s[list_to_free].append((lb, lb + (int(2 ** list_to_free) - 1)))

        print("\nBloque {} liberado\n".format(name))

        # buddyNumber and buddyAddrs
        buddy_num = lb / block_size

        if buddy_num % 2 != 0:
            buddy_addr = lb - int(2 ** list_to_free)
        else:
            buddy_addr = lb + int(2 ** list_to_free)


        # Busca el buddy en la lista de bloques libres
        i = 0
        while i < len(block_list_s[list_to_free]):

            # Si el buddy esta en la lista de bloques libres
            if block_list_s[list_to_free][i][0] == buddy_addr:

                # Buddy esta despues del bloque con esta direccion base
                if buddy_num % 2 == 0:
                    # Agrega el bloque a la lista de bloques libres
                    block_list_s[list_to_free + 1].append((lb, lb + (int(2 ** list_to_free) - 1)))
                    print("Se realizo la fusion de bloques que comienzan en " + str(lb) + " y " + str(buddy_addr) + "\n")

                # Buddy es el bloque antes del bloque con esta direccion base
                else:
                    # Agrega el bloque a la lista de bloques libres
                    block_list_s[list_to_free + 1].append((buddy_addr, buddy_addr + 2 * int(2 ** list_to_free) - 1))
                    print("Se realizo la fusion de bloques que comienzan en {} y {}\n".format(buddy_addr, lb))

                # Elimina el bloque de la lista de bloques libres
                block_list_s[list_to_free].pop(i)
                block_list_s[list_to_free].pop()
                break
            i += 1

        name_list.pop(name)

    # Muestra una representacion grafica de la memoria
    def display(self):
        print("\nMemoria:")
        print("\nBloques de memoria permitidos:")
        print("Lista de bloques: {}".format(self.block_list_s))
        print("Nombre de bloques reservados, direccion base, direccion final:")
        print("Lista de nombres: {}".format(self.name_list))
