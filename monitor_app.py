"""Analiza las descargas y los estados de las mismas de Rutas en bici"""

from typing import Final

# Añadid aquí las importaciones que necesitéis.
import logging
# ---------------------------------------------------------------------------
# Datos de la aplicación. Sustituid los del ejemplo APP-00 por los vuestros.
# ---------------------------------------------------------------------------
CODIGO: Final[str] = "APP-00"
NOMBRE: Final[str] = "Agenda Escolar"
# Una posición por semana, de la 1 a la 12. 0 descargas: app retirada.
DESCARGAS: Final = [1_600, 1_590, 0, 1_460, 1_520, 1_640,
                    1_580, 1_560, 1_610, 1_600, 1_790, 1_730]
CAIDAS: Final = [23, 15, 0, 33, 18, 20,
                13, 6, 6, 30, 5, 6]


# ---------------------------------------------------------------------------
# Datos del programa. Solo hay que cambiar AUTORES.
# ---------------------------------------------------------------------------
VERSION_PROGRAMA: Final[str] = "1.0.0"
AUTORES: Final[str] = "[usuario] · [usuario]"
PENDIENTE: Final[str] = "  (opción pendiente de implementar)"

# ---------------------------------------------------------------------------
# Constantes comunes.
# ---------------------------------------------------------------------------
ANCHO: Final[int] = 44
POR_MIL: Final[int] = 1_000
UMBRAL_ESTABLE: Final[float] = 5.0       # caídas por cada mil descargas
UMBRAL_ACEPTABLE: Final[float] = 10.0
UMBRAL_REVISAR: Final[float] = 15.0
OPCION_SALIR: Final[int] = 9

# ---------------------------------------------------------------------------
# Constantes de la pareja. Todo valor fijo del programa va aquí, con nombre.
# ---------------------------------------------------------------------------
UMBRAL_MINIMO: Final[float] = 0.0
UMBRAL_MAXIMO: Final[float] = 1000.0
MAX_OBJETIVO: Final[int] = 1_000_000
CRECIMIENTO_MINIMO: Final[float] = 0.5
CRECIMIENTO_MAXIMO: Final[float] = 50.0
MAX_SEMANAS_PREVISION: Final[int] = 104
PORCENTAJE: Final[int] = 100

# ---------------------------------------------------------------------------
# Excepciones propias de la pareja. Aquí va SemanaNoValida (opción 7).
# ---------------------------------------------------------------------------
class SemanaNoValida(ValueError):
    """ Error cuando el usuario introduce una semana no válida"""
    pass

# ---------------------------------------------------------------------------
# Funciones auxiliares. tasa_caidas viene hecha; el resto, con su docstring,
# las completáis vosotros. No cambiéis sus cabeceras.
# ---------------------------------------------------------------------------
def tasa_caidas(descargas: int, caidas: int) -> float:
    """Devuelve las caídas por cada mil descargas.

    Lanza ZeroDivisionError si la semana no tiene descargas.
    """
    return caidas / descargas * POR_MIL


def estado(descargas: int, caidas: int) -> str:
    """Devuelve el estado de una semana según su tasa de caídas.
    Se usa un primer condicional para retornar mantenimiento y después con tasa caidas vamos
    usando if y elif para ir devolviendo los estados. Se usa '<' porque los umbrales dicen menos de"""
    if descargas == 0:
        return "Mantenimiento"
    tasa = tasa_caidas(descargas, caidas)
    if tasa < UMBRAL_ESTABLE:
        return "Estable"
    elif tasa < UMBRAL_ACEPTABLE:
        return "Aceptable"
    elif tasa < UMBRAL_REVISAR:
        return "Revisar"
    else:
        return "Crítica"                  


def pedir_entero(mensaje: str, minimo: int, maximo: int) -> int:
    """Pide un entero entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un entero o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        try:
            entero = int(input(mensaje))
        except ValueError:
            print("Error: Debes introducir un número entero")
            continue

        if minimo <= entero <= maximo:
            return entero
        else:
            print(f"Error: Introduce un número entre {minimo} y {maximo}")


def pedir_real(mensaje: str, minimo: float, maximo: float) -> float:
    """Pide un número real entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un número o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        texto = input(mensaje)
        try:
            valor = float(texto)
        except ValueError:
            print(f" '{texto}' no es un número. ")
            continue
        if minimo <= valor <= maximo:
            return valor
        
        print(f" Escribe un valor entre {minimo:.1f} y {maximo:.1f}")                   


def semana_valida(texto: str) -> int:
    """Comprueba que el número de semana sea válido."""
    try:
        semana = int(texto)
    except ValueError:
        raise SemanaNoValida("Debes introducir un número entero")

    if 1 <= semana <= len(DESCARGAS):
        return semana
    else:
        raise SemanaNoValida("La semana introducida no existe")


def comprobar_datos() -> int:
    """Revisa los datos semanales y devuelve el número de errores.

    Registra cada error con logging.error y cada semana de mantenimiento
    con logging.warning.
    """
    errores = 0

    if len(DESCARGAS) != len(CAIDAS):
        logging.error("Las listas no tienen la misma cantidad de semanas")
        errores += 1

    for semana, (descargas, caidas) in enumerate(zip(DESCARGAS, CAIDAS), start=1):

        if descargas < 0 or caidas < 0:
            logging.error(f"semana {semana}: hay valores negativos")
            errores += 1

        if caidas > descargas:
            logging.error(f"semana {semana}: más caídas que descargas")
            errores += 1

        if descargas == 0 and caidas == 0:
            logging.warning(f"semana {semana}: sin descargas (mantenimiento)")

    return errores    



# ---------------------------------------------------------------------------
# Menú y opciones. La opción 1 viene hecha y la 2 tiene dos errores.
# ---------------------------------------------------------------------------
def mostrar_menu() -> None:
    """Esta funcion nos mostrara nuestro menu y sus opciones"""
    print("=" * ANCHO)
    print(f"MONITOR DE {CODIGO} · {NOMBRE}".center(ANCHO))
    print("=" * ANCHO)
    print("1. Listado semanal")
    print("2. Resumen")
    print("3. Estabilidad por semana")
    print("4. Primera semana que alcanza un umbral")
    print("5. Mejor racha sin problemas")
    print("6. Previsión de crecimiento")
    print("7. Consultar una semana")
    print("8. Comprobar los datos")
    print("9. Salir")


def opcion_1_listado() -> None:
    """Muestra las descargas, las caídas y la tasa de cada semana."""
    print(f"{'Semana':>6}{'Descargas':>11}{'Caídas':>8}{'Tasa ‰':>9}")
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        try:
            tasa = f"{tasa_caidas(descargas, caidas):.1f}"
        except ZeroDivisionError:
            tasa = "—"
        print(f"{semana:>6}{descargas:>11}{caidas:>8}{tasa:>9}")


def opcion_2_resumen() -> None:
    """Muestra los totales, la media y las semanas extremas."""
    total_descargas = 0
    total_caidas = 0
    activas = 0
    mas = 0
    semana_mas = 0
    menos = float('inf')
    semana_menos = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        activas += 1
        total_descargas += descargas
        total_caidas += caidas
        if descargas > mas:
            mas = descargas
            semana_mas = semana 
        if descargas < menos:
            menos = descargas
            semana_menos = semana
    media = total_descargas / activas
    tasa = tasa_caidas(total_descargas, total_caidas)
    print(f"Semanas activas:     {activas} de {len(DESCARGAS)}")
    print(f"Total de descargas:  {total_descargas}")
    print(f"Media semanal:       {media:1f}")
    print(f"Más descargas:       semana {semana_mas} ({mas})")
    print(f"Menos descargas:     semana {semana_menos} ({menos})")
    print(f"Total de caídas:     {total_caidas}")
    print(f"Tasa global:         {tasa:1f} ‰")


def opcion_3_estabilidad() -> None:
    """Muestra el estado de cada semana y cuántas hay de cada estado"""
    contador_estables = 0
    contador_aceptables = 0
    contador_revisar = 0
    contador_criticas = 0
    contador_mantenimiento = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        estado_semana = estado(descargas, caidas)
        print(f"Semana {semana}: {estado_semana}")
        match estado_semana:
            case "Estable":
                contador_estables += 1
            case "Aceptable":
                contador_aceptables += 1
            case "Revisar":
                contador_revisar += 1
            case "Crítica":
                contador_criticas += 1
            case "Mantenimiento":
                contador_mantenimiento += 1
    
    print("-" * ANCHO)
    print(f"Estables: {contador_estables}")
    print(f"Aceptables: {contador_aceptables}")
    print(f"Revisar: {contador_revisar}")
    print(f"Críticas: {contador_criticas}")
    print(f"Mantenimiento: {contador_mantenimiento}")


def opcion_4_umbral() -> None:
    """Muestra la primera semana en la que la tasa iguala o supera un umbral"""
    umbral = pedir_real("Umbral en caídas (*1000): ",UMBRAL_MINIMO, UMBRAL_MAXIMO)
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        tasa = tasa_caidas(descargas, caidas)
        if tasa >= umbral:
            print(f"Primera semana: {semana} --> ({tasa:.1f})%")
            break
        
    else:
        print(f"Ninguna semana alcanza el {umbral:.1f}%")


def opcion_5_racha() -> None:
    """Muestra la racha más larga Estable o Aceptable"""
    racha_actual = 0
    semana_inicio_actual = 0
    mejor_racha = 0
    semana_inicio_mejor = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        estado_semana = estado(descargas, caidas)
        if estado_semana == "Mantenimiento":
            continue
        match estado_semana:
            case "Estable" | "Aceptable":
                if racha_actual == 0:
                    semana_inicio_actual = semana
                racha_actual += 1
                if racha_actual > mejor_racha:
                    mejor_racha = racha_actual
                    semana_inicio_mejor = semana_inicio_actual
            case "Revisar" | "Crítica":
                racha_actual = 0
    if mejor_racha == 0:
        print("No ha habido ninguna semana que no haya tenido problemas")
    else:
        print(f"Mejor racha: {mejor_racha} semanas, " f"desde la semana {semana_inicio_mejor}")


def opcion_6_prevision() -> None:
    """Calcula las semanas necesarias para alcanzar un objetivo de descargas."""
    ultima_descarga = 0

    for descargas in DESCARGAS:
        if descargas > 0:
            ultima_descarga = descargas

    print(f"Descargas de la última semana activa: {ultima_descarga}")

    objetivo = pedir_entero(
        "Objetivo semanal de descargas: ",
        minimo=ultima_descarga + 1,
        maximo=MAX_OBJETIVO
    )

    crecimiento = pedir_real(
        "Crecimiento semanal en %: ",
        minimo=CRECIMIENTO_MINIMO,
        maximo=CRECIMIENTO_MAXIMO
    )

    descargas_previstas = float(ultima_descarga)
    semanas = 0

    while descargas_previstas < objetivo:

        if semanas >= MAX_SEMANAS_PREVISION:
            break

        aumento = descargas_previstas * crecimiento / PORCENTAJE

        descargas_previstas += aumento

        semanas += 1

    if descargas_previstas >= objetivo:
        print(
            f"Se alcanza en {semanas} semanas "
            f"({descargas_previstas:.0f} descargas)"
        )
    else:
        print(
            f"No se alcanza el objetivo en "
            f"{MAX_SEMANAS_PREVISION} semanas."
        )



def opcion_7_consulta() -> None:
    """Muestra los datos y el estado de una semana."""

    texto = input(f"Semana (1-{len(DESCARGAS)}): ")

    try:
        semana = semana_valida(texto)
    except SemanaNoValida as error:
        print(f"Error: {error}")
        return

    for numero, (descargas, caidas) in enumerate(zip(DESCARGAS, CAIDAS), start=1):
        if numero == semana:

            estado_semana = estado(descargas, caidas)

            match estado_semana:
                case "Estable":
                    accion = "Sin acciones"
                case "Aceptable":
                    accion = "Vigilar en la próxima versión"
                case "Revisar":
                    accion = "Revisar los informes de errores"
                case "Crítica":
                    accion = "Publicar una versión correctora urgente"
                case "Mantenimiento":
                    accion = "La app no estuvo publicada esa semana"
                case _:
                    accion = "Estado desconocido"

            print(f"Semana: {numero}")
            print(f"Descargas: {descargas}")
            print(f"Caídas: {caidas}")
            print(f"Estado: {estado_semana}")
            print(f"Acción: {accion}")

            break



def opcion_8_comprobar() -> None:
    """Comprueba si los datos de la aplicación son correctos."""

    errores = comprobar_datos()

    if errores == 0:
        print(f"Datos correctos: {len(DESCARGAS)} semanas")
    else:
        print("Los datos tienen errores: corrígelos antes de continuar.")



def main() -> None:
    """Funcion principal que se encarga de ejecutar las diferentes funciones que hemos ido creando"""
    
    while(True):
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opcion: "))
        except ValueError:
            print("Error: Debes introducir un numero entero")
            continue
        except KeyboardInterrupt:
            print("Saliendo del programa...")
            break
        if opcion < 1 or opcion > OPCION_SALIR:
            print("Error: La opción introducida no existe")
            continue

        if(opcion == 1):
            opcion_1_listado()
        elif(opcion == 2):
            opcion_2_resumen()
        elif(opcion == 3):
            opcion_3_estabilidad()
        elif(opcion == 4):
            opcion_4_umbral()
        elif(opcion == 5):
            opcion_5_racha()
        elif(opcion == 6):
            opcion_6_prevision()
        elif(opcion == 7):
            opcion_7_consulta()
        elif(opcion == 8):
            opcion_8_comprobar()
        elif(opcion == 9):
            print("SALIENDO...")
            break



if __name__ == "__main__":
    main()
