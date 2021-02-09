from itertools import combinations

def verificacion(numero,color):
    if(int(numero)>13 or int(numero) <1):
        return False
    if(color=="V"):
        color="verde"
    elif(color=="A"):
        color="azul"
    elif(color=="R"):
        color="rojo"
    elif(color=="N"):
        color="negro"
    else:
        return False
    return (numero,color)

def cargar_tablero():
    tablero = []#lista de listas
    try:
        archivo = open("tablero.txt",'rt')
        for linea in archivo:
            linea = linea[:-1] #Elimina el salto de linea
            jugada = linea.split(',')
            aux=[] #lista de fichas xd
            for ficha in jugada: #x=(1|v)
                valor,color=ficha.split('|')
                valor=valor[1:]
                color=color[-2]
                aux2=verificacion(valor,color)
                if(aux2):
                    aux.append(aux2)
                else:
                    return False
            tablero.append(aux)
        archivo.close()
    except FileNotFoundError:
        print("juego vacio")
    return tablero

def verificar_fichas_v2(tablero): # Verifica que no haya mas de dos fichas iguales
    lista_de_todas_las_fichas = []
    for jugada in tablero:
        for ficha in jugada:
            lista_de_todas_las_fichas.append(ficha)
    fichas = set(lista_de_todas_las_fichas) #Se crea un conjunto en el cual hay una de cada ficha
    for actual in fichas:
        if lista_de_todas_las_fichas.count(actual) > 2: #No puede haber mas de dos copias de una ficha
            return False #configuracion invalida
    return True #configuracion valida

def verificar_corrida2(jugada): #Verifica si el juego es una escalera
    for i in range(len(jugada)-1):
        if (((int(jugada[i][0])+1)) != (int(jugada[i+1][0]))): #Compara si la ficha actual en su "campo" valor + 1 es igual a la siguente en su "campo" valor
            return False #De no ser cierto quiere decir que no es escalera
    return "E" #Es escalera, Se utiliza un codigo de letras

def verificar_TC(jugada): #Verifica si es una Tercia o una cuarteta
    if len(jugada)==3: #Es una jugada de 3 fichas
        for i in range(len(jugada)-1) :
            if (((int(jugada[i][0]))) != (int(jugada[i+1][0]))): #Compara si la ficha en su "campo" valor es igual es igual a la ficha siguente en su "campo" valor
                return False #Es un juego de tres fichas pero NO es tercia
        return "T" #Es una tercia, se utiliza un código de letras
    elif len(jugada)==4: #Es una jugada de cuatro fichas
        for i in range(len(jugada)-1) :
            if (((int(jugada[i][0]))) != (int(jugada[i+1][0]))): #Compara si la ficha en su "campo" valor es igual es igual a la ficha siguente en su "campo" valor
                return False #Es una jugada de cuatro fichas pero NO es cuarteta
        return "C" #Es una cuarteta , se utiliza un codigo de letras
    return False #No es ni cuarteta ni tercia


def verificar_jugada_FV(jugada):#Centraliza las dos funciones anteriores
    x={}
    aux2=len(jugada) #Se almacena en aux2 el numero de fichas de la jugada
    for ficha in jugada: #Analiza ficha por ficha de la jugadas
        x[ficha[1]]=ficha[0]
    if(len(x)==0):
        print("La jugada no tiene elementos")
        return True
    elif(aux2<3): #Es una jugada con menos de tres fichas (no valida)
        return False
    elif(len(jugada)==len(x)): #Puede ser una tercia o una cuarteta
        return verificar_TC(jugada)
    elif(len(x)==1): #todas las fichas son del mismo color por lo tanto PUEDE SER una escalera
        return verificar_corrida2(jugada) #verifica si realmente es una escalera
    return False

def verificacion_chida_del_tablero(tablero):#esta funcion debe ser cambiada con las funciones alternativas
    for jugadas in tablero:
        aux1=verificar_jugada_FV(jugadas)#aux1 puede tomar cuatro valores posibles E,T,C (código de letras) o False en caso de que la jugada no sea valida
        if(aux1==False):
            return False #La jugada no es valida y por ende la configuración de tablero no es valida
    aux=verificar_fichas_v2(tablero) #Verifica que no halla mas de dos fichas
    if(aux==False):
        return False #Tablero invalido
    return True #Hasta este punto ha pasado todos los filtros


def ingresar_ficha():
    ficha = True
    while ficha==True:
        numero = input("Ingrese el número de la ficha que deseas ingresar: ")
        print("Colores disponibles:\nVerde = V\nRojo = R\nAzul = A\nNegro = N\n")
        color = input("Ingresa la primera letra del color de tu ficha: ")
        ficha = verificacion(numero,color.upper()) #convertiremos la letra (en caso de ser minúscula) a MAYÚSCULA
        if(ficha == False):
            print("Ficha no válida")
    return ficha


def dividir(jugada, tablero, ficha):
    while True:
        P_jugada=[]
        p = int(input("Quieres agregar ficha:\n0.Antes\n1.Después "))
        F= input("Numero de la ficha:")
        P_jugada=jugada[:]
        P_jugada.insert(p+P_jugada.index((F,P_jugada[0][1])),ficha)
        print(P_jugada)
        a = input("Después de que ficha quieres hacer el corte?")
        try:
            C = P_jugada[P_jugada.index((a,jugada[0][1]))+1:] #[primer lista]
            D = P_jugada[:P_jugada.index((a,jugada[0][1]))+1]
        except ValueError:
            print("ficha no encontrada")
        print(C)
        print(D)
        if verificar_jugada_FV(C) and verificar_jugada_FV(D):#Cambiar funcion
            print("Jugada válida")
            tablero.pop(tablero.index(jugada))
            tablero.append(C)
            tablero.append(D)
            return tablero
        else:
            print("Jugada no válida")
            return False

def recibir_jugada(tablero,ficha):
    print("Configuración actual del tablero\n")
    num = 1
    for x in tablero:
        print(num,".- ",x)
        num = num+1
    print("\nQué quieres hacer?\na)Agregar ficha\nb)Reordenar el juego")
    respuesta = input()
    while respuesta != 'a' and respuesta != 'b':
        print("Opción no válida, ingrese la letra a ó b")
        print("\nQué quieres hacer?\na)Agregar ficha\nb)Reordenar el juego")
        respuesta = input()
    if respuesta == 'a':
        print("Dónde quieres agregar la ficha? (indica el número de la lista)")
        jugada = int(input())
        print("Indica la ubicación a colocar (índice dentro de la lista)")
        ubi = int(input())
        jugada_mod = tablero[jugada-1]
        jugada_mod.insert(ubi,ficha)
        if verificar_jugada_FV(jugada_mod) == False and verificar_fichas_v2(tablero) == False:
            print("Esa jugada no es válida")
            print(jugada_mod)
            jugada_mod.remove(ficha)
            return tablero
        print("Jugada válida")
        print(jugada_mod)
        return tablero
    if respuesta == 'b':
        print("\nQué quieres hacer?\na)Dividir jugada\nb)Mover ficha")
        res = input()
        while res !='a' and res != 'b':
            print("Opción no válida, ingrese la letra a ó b")
            print("\nQué quieres hacer?\na)Dividir jugada\nb)Mover ficha")
            res = input()
        print("Dónde quieres realizar el movimiento? (indica el número de la lista)")
        jugada = int(input())
        if res == 'a':
            dividir(tablero[jugada-1],tablero,ficha)
            return tablero
        if res == 'b':
            print("Indica la ubicación de la ficha a mover (índice dentro de la lista)")
            ubi = int(input())
            jugada_mod = tablero[jugada-1]
            ficha_aux = jugada_mod[ubi]
            jugada_mod.remove(ficha_aux)
            print("Dónde quieres colocar la ficha? (indica el número de la lista)")
            jugada = int(input())
            print("Indica la ubicación a colocar (índice dentro de la lista)")
            ubi = int(input())
            jugada_mod = tablero[jugada-1]
            jugada_mod.insert(ubi,ficha_aux)
            if verificar_jugada_FV(jugada_mod) == False and verificar_fichas_v2(tablero) == False:
                print("Esa jugada no es válida")
                print(jugada_mod)
                jugada_mod.remove(ficha_aux)
                return tablero
            print("Jugada válida")
            print(jugada_mod)
            return tablero

def integrar_Ficha(jugadaProblematica,copia_del_tablero,lista_de_intocables,pilaSolucion):
    i = 0 #contador de movimiento (auxiliar)
    jugadaProblematica_aux = jugadaProblematica[:]
    for ficha in jugadaProblematica_aux:
        for jugada in copia_del_tablero:
            posible_jugada = posible_insercion(jugada,ficha,lista_de_intocables)
            if posible_jugada != False  and ficha not in lista_de_intocables:     # La ficha se ingresó correctamente
                for y in range(len(copia_del_tablero)):
                    if jugadaProblematica == copia_del_tablero[y]:      # Si es igual, la jugada problemática se encuentra en el índice actual del tablero
                        ubi = copia_del_tablero.index(copia_del_tablero[y])     # Guardamos la ubicación de la jugada problemática dentro del tablero
                if jugada in copia_del_tablero[ubi]:        # Si la ficha que se agregó está en la jugada problemática del tablero
                    copia_del_tablero[ubi].remove(ficha)        # Borramos dicha ficha porque ya se agregó a otra jugada
                jugadaProblematica.remove(ficha)
                if len(jugadaProblematica) == 0:        # si la lista de la jugada problemática está vacía
                    copia_del_tablero.remove(jugadaProblematica)    # Retiramos esa lista vacía del tablero porque ya no nos sirve
                nuevo_tablero = copiar_tablero(copia_del_tablero)
                pilaSolucion.append(nuevo_tablero)
                lista_de_intocables.append(ficha)
                i = i + 1 #Cada que hay un movimiento de fichas se agrega
    return verificacion_De_Movimiento(i)

def robar_Ficha(jugadaProblematica,copia_del_tablero,lista_de_intocables,pilaSolucion):
    if len(jugadaProblematica) == 1: #caso en el que sólo es una ficha
        posibles_robos =  posibles_robadas_inicial(jugadaProblematica[0])
        for jugada in copia_del_tablero:
            for fichita in posibles_robos:
                if fichita in jugada and fichita not in lista_de_intocables:     
                    insercion_a_incompleta(jugada,jugadaProblematica,fichita,lista_de_intocables)
                    nuevo_tablero = copiar_tablero(copia_del_tablero)
                    pilaSolucion.append(nuevo_tablero)
                    posibles_robadas_actualizar(jugadaProblematica,posibles_robos)
                    return True
    if len(jugadaProblematica) == 2:       # La jugada es de dos fichas
        posibles_robos = [] #inicia como lista vacia
        posibles_robadas_actualizar(jugadaProblematica,posibles_robos)
        for jugada in copia_del_tablero:
            for fichita in posibles_robos:
                if fichita in jugada and fichita not in lista_de_intocables:
                    insercion_a_incompleta(jugada,jugadaProblematica,fichita,lista_de_intocables)
                    nuevo_tablero = copiar_tablero(copia_del_tablero)
                    pilaSolucion.append(nuevo_tablero)
                    return True
    return False

def actualizar_Jugada_Problematica(copia_del_tablero):
    for jugadaActual in copia_del_tablero:
        if verificar_jugada_FV(jugadaActual) == False:
            return jugadaActual #En esta jugada se va a detener, ya que no paso la verificación

def verificacion_De_Movimiento(contador_de_movimiento):
    if contador_de_movimiento:
        return True
    return False

def backTrack(copia_del_tablero,pilaSolucion):
    copia_del_tablero = pilaSolucion[len(pilaSolucion)-2]     # penúltimo tablero
    pilaSolucion.pop()
    return copia_del_tablero

def prediccion(tablero,pilaSolucion,ficha):
    lista_de_intocables = []    #se inicializa la lista pa que funcione :v
    copia_del_tablero = copiar_tablero(tablero)
    jugadaProblematica = copia_del_tablero[-1]
    while True:
        while True:
            x = integrar_Ficha(jugadaProblematica,copia_del_tablero,lista_de_intocables,pilaSolucion)
            if x == False:
                y = robar_Ficha(jugadaProblematica,copia_del_tablero,lista_de_intocables,pilaSolucion)
            if verificar_jugada_FV(jugadaProblematica):
                break #La jugada ya es correcta por lo tanto sale del ciclo
            if x == False and y == False:
                copia_del_tablero = backTrack(copia_del_tablero,pilaSolucion)
                jugadaProblematica = actualizar_Jugada_Problematica(copia_del_tablero)
                if tablero == pilaSolucion[-1]:
                    print("\nNo es posible agregar la ficha\n")
                    return  # Definitivo
        if verificacion_chida_del_tablero(copia_del_tablero):
            print("Si es posible agregar la ficha")
            print("Configuración final:")
            imprimir_tablero(pilaSolucion[-1])
            print("")
            print("")
            return
        else:
            jugadaProblematica = actualizar_Jugada_Problematica(copia_del_tablero) #Actualizar jugada problematica
    return


def posibles_robadas_inicial(ficha):
    fichasNecesarias = [] #fichas próximas para generar jugada (3 fichas)
    colores = ["azul","rojo","negro","verde"] #Lista con todos los colores
    if int(ficha[0]) == 1: #Caso ESPECIAL inicio
        valor1 = int(ficha[0])+1
        valor2 = int(ficha[0])+2
        fichasNecesarias.append((str(valor1),ficha[1]))
        fichasNecesarias.append((str(valor2),ficha[1]))
        colores.remove(ficha[1]) #Se elimina el color de la ficha
        for colorActual in colores:
            fichasNecesarias.append((ficha[0],colorActual))
        return fichasNecesarias

    if int(ficha[0]) == 13: #Caso ESPECIAL final
        valor1 = int(ficha[0])-2
        valor2 = int(ficha[0])-1
        fichasNecesarias.append((str(valor1),ficha[1]))
        fichasNecesarias.append((str(valor2),ficha[1]))
        colores.remove(ficha[1])
        for colorActual in colores:
            fichasNecesarias.append((ficha[0],colorActual))
        return fichasNecesarias

    #Para cualquier otro caso
    valor1 = int(ficha[0])-1
    valor2 = int(ficha[0])+1
    fichasNecesarias.append((str(valor1),ficha[1]))
    fichasNecesarias.append((str(valor2),ficha[1]))
    colores.remove(ficha[1])
    for colorActual in colores:
        fichasNecesarias.append((ficha[0],colorActual))
    return fichasNecesarias

def posibles_robadas_actualizar(jugada,fichasParaActualizar):
    FichasJugada = []
    cabeza = jugada[0] #cabeza va a ser la primera fica
    talon = jugada[-1]
    if cabeza == talon: #La jugada unicaménte consta de una ficha
        return posibles_robadas_inicial(cabeza)

    color = jugada[0][1]
    if color == jugada[1][1]: #Es una escalera en potencia
        fichasParaActualizar.clear()
        if int(cabeza[0]) < int(talon[0]) and int(cabeza[0]) != 1 and int(talon[0]) != 13:
            valor1 = int(cabeza[0])-1
            valor2 = int(talon[0])+1
            ficha_robo = (str(valor1),cabeza[1])
            ficha_robo2 = (str(valor2),talon[1])
            fichasParaActualizar.append(ficha_robo)
            fichasParaActualizar.append(ficha_robo2)
            return
        elif int(cabeza[0]) == 1: #Caso ESPECIAL
            valor = int(talon[0])+1
            ficha_robo = (str(valor),talon[1])
            fichasParaActualizar.append(ficha_robo)
            return fichasParaActualizar
        else:       # Caso 13
            valor = int(cabeza[0])-1
            ficha_robo = (str(valor),cabeza[1])
            fichasParaActualizar.append(ficha_robo)
            return fichasParaActualizar

    fichasParaActualizar.clear()
    FichasJugada = ficha_Faltante_De_Jugada(jugada)
    for ficha in FichasJugada:
        fichasParaActualizar.append(ficha)
    return

def ficha_Faltante_De_Jugada(jugada):
    colores_de_la_jugada = []
    fichas_faltantes = []
    for ficha in jugada:
        colores_de_la_jugada.append(ficha[1])
    if "azul" not in colores_de_la_jugada:
        fichas_faltantes.append((str(ficha[0]),"azul"))
    if "rojo" not in colores_de_la_jugada:
        fichas_faltantes.append((str(ficha[0]),"rojo"))
    if "negro" not in colores_de_la_jugada:
        fichas_faltantes.append((str(ficha[0]),"negro"))
    if "verde" not in colores_de_la_jugada:
        fichas_faltantes.append((str(ficha[0]),"verde"))
    return fichas_faltantes

def posible_insercion(jugada,ficha,lista_de_intocables): #perdon umu
    x = ficha #porque las fichas pueden ser 2, x analizaría una ficha . si solo es una ficha x sería esa ficha
    P_jugada = jugada[:]
    if ficha not in lista_de_intocables:
        juego = verificar_jugada_FV(P_jugada)
        if(juego =="E"): #Escalera
            P_jugada.append(x)
            if(verificar_jugada_FV(P_jugada)):
                jugada.append(x)
                return jugada
            P_jugada.remove(x)
            P_jugada.insert(0,x)
            if(verificar_jugada_FV(P_jugada)):
                jugada.insert(0,x)
                return jugada
            P_jugada.remove(x)
        elif (juego == "T"): #Tercia
            P_jugada.append(x)
            if(verificar_jugada_FV(P_jugada)): 
                jugada.append(x)
                return jugada
    return False #No se puede hacer la modificacion

def insercion_a_incompleta(jugadaOrigen,jugadaDestino,fichaAInsertar,lista_de_intocables):
    if fichaAInsertar not in lista_de_intocables:
        jugadaOrigen.remove(fichaAInsertar)
        jugadaDestino.append(fichaAInsertar)
        convertir_jugada_int(jugadaDestino)
        jugadaDestino.sort()
        convertir_jugada_str(jugadaDestino)
        lista_de_intocables.append(fichaAInsertar)
        return True #Insercion exitosa
    return False 

def copiar_tablero(tablero):
    copia_tablero = []
    for jugada in tablero:
        copia_tablero.append(jugada[:])
    return copia_tablero

def convertir_ficha_entero(numero,color): #Cambia del formato (valor,"Letra") a (valor,"color")
        if(int(numero)>13 or int(numero) <1):
            return False
        if(color=="verde"):
            color="V"
        elif(color=="azul"):
            color="A"
        elif(color=="rojo"):
            color="R"
        elif(color=="negro"):
            color="N"
        else:
            return False
        return (int(numero),color) #transforma a entero y el color lo regresa en forma de letra mayuscula|


def convertir_jugada_str(jugada):
    for ficha in jugada:
        ficha = verificacion(ficha[0],ficha[1])


def convertir_jugada_int(jugada): #(str(valor),str(color))->(int(valor),(color{n}))
    for ficha in jugada:
        ficha = convertir_ficha_entero(ficha[0],ficha[1])

def imprimir_tablero(tablero):
    contador=0
    for jugada in tablero:
        print("\n")
        contador +=1
        print("jugada "+str(contador)+":",end="")
        for ficha in jugada:
            print (ficha,end="")
    return

def menu():
    ops = ['Cargar Tablero', 'Agregar ficha', 'Predicción de una jugada', 'Secuencia de movimientos','Salir']
    while True:
        for i in range(len(ops)):
            print( i+1, ") ", ops[i] )
        seleccion = int(input("Opción "))
        if seleccion>=1 and seleccion<=5:
            return seleccion
        print("Opción inválida!!")

if __name__ == "__main__":
    print("\nBienvenido al proyecto final, elige una opción: \n ")
    tablero = []
    pilaSolucion = [] #Va a contener Tableros
    while True:
        eleccion = menu()
        if eleccion == 1:
            tablero = cargar_tablero()
            if verificacion_chida_del_tablero(tablero) != True:
                print("La configuración es incorrecta")
            else:
                print("El tablero se ha cargado con éxito")
        elif eleccion ==2 and len(tablero) != 0:
            ficha = ingresar_ficha()
            recibir_jugada(tablero,ficha)
        elif eleccion ==3 and len(tablero) != 0:
            ficha = ingresar_ficha()
            ficha_sola = []
            ficha_sola.append(ficha)
            tablero.append(ficha_sola)
            pilaSolucion.append(tablero)
            prediccion(tablero,pilaSolucion,ficha)
        elif eleccion == 4 and len(tablero) != 0:
            print("Configuración inicial:")
            imprimir_tablero(pilaSolucion[0])
            pilaSolucion.remove(pilaSolucion[0])
            num = 1
            for x in pilaSolucion:
                print("\n\nMovimiento #",num,"")
                imprimir_tablero(x)
                num = num + 1
            print("")
            print("")
        elif eleccion == 5:
            print("Hasta luego :)")
            break
        else:
            print("No hay tablero cargado")
    pass