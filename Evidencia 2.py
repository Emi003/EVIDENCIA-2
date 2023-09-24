import datetime
import csv
import pandas as pd

notas = []
notas_canceladas = set()
servicios_nota = []
ultimo_folio = 0

def generar_folio():
    global ultimo_folio
    ultimo_folio += 1
    return ultimo_folio

def calcular_monto(servicios_nota):
    total = sum(monto for _, monto in servicios_nota)
    return total

def validar_rfc_persona_fisica(rfc):
    rfc = rfc.strip().upper()
    if len(rfc) != 13:
        return False

    if not rfc[:4].isalpha():
        return False
    if not rfc[4:10].isdigit():
        return False
    if not (rfc[-1].isdigit() or rfc[-1] == 'A'):
        return False
    homoclave = rfc[10:12]
    if not homoclave.isalnum():
        return False
    rfc_sin_homoclave = rfc[:10] + rfc[11]

    return True

def validar_rfc_persona_moral(rfc):
    rfc = rfc.strip().upper()
    if len(rfc) != 12:
        return False

    if not rfc[:3].isalpha():
        return False
    if not rfc[3:9].isdigit():
        return False
    if not (rfc[-1].isdigit() or rfc[-1] == 'A'):
        return False
    homoclave = rfc[9:11]
    if not homoclave.isalnum():
        return False
    rfc_sin_homoclave = rfc[:9] + rfc[11]

    return True

def validar_correo(correo):
    if correo.count('@') != 1:
        return False
    usuario, dominio = correo.split('@')

    if not usuario or not dominio:
        return False
    if dominio.count('.') != 1 or not dominio.split('.')[1]:
        return False
    return True


while True:
    print("\nMenu:")
    print("1. Registrar una nota")
    print("2. Consultas y Reportes")
    print("3. Cancelar una nota")
    print("4. Recuperar una nota")
    print("5. Salir")

    opcion = input("Seleccione una opción de los numero que estan aqui; (1, 2, 3, 4, 5): ").strip()

    if opcion == "1":
        Nombre_Cliente = input("Introducir el nombre completo del Cliente: ")
        if not Nombre_Cliente.strip():
            break

        fecha_nota = input("Dame la fecha en este formato: dd/mm/aaaa: ")
        try:
            fecha_actual = datetime.date.today()
            fecha_procesada = datetime.datetime.strptime(fecha_nota, '%d/%m/%Y').date()
            if fecha_procesada > fecha_actual:
                print("La fecha no puede ser posterior a la fecha actual.")
                continue
        except ValueError:
            print("Formato de fecha incorrecto. Introduce la fecha en el formato dd/mm/aaaa.")
            continue

        tipo_cliente = input("¿Es persona física o moral? (F/M): ").strip().upper()
        RFC_Cliente = input("Introduce el RFC del cliente: ")
        
        if tipo_cliente == "F":
            if not validar_rfc_persona_fisica(RFC_Cliente):
                print("RFC de persona física no válido.")
                continue
        elif tipo_cliente == "M":
            if not validar_rfc_persona_moral(RFC_Cliente):
                print("RFC de persona moral no válido.")
                continue
        else:
            print("Opción no válida. Debe seleccionar F para persona física o M para persona moral.")
            continue

        Correo_Cliente = input("Introduce el correo electrónico del cliente: ")
        if not validar_correo(Correo_Cliente):
            print("Correo electrónico no válido.")
            continue

        servicios_nota = []
        while True:
            servicio = input("Ingrese el nombre del servicio: ")
            monto = None
            while monto is None:
                try:
                    monto = float(input("Ingrese el monto a pagar por el servicio: "))
                except ValueError:
                    print("Monto no válido. Ingrese un valor numérico.")
            
            servicios_nota.append((servicio, monto))
            
            folio_actual = generar_folio()
            notas.append({
            "Folio": folio_actual,
            "Nombre_Cliente": Nombre_Cliente,
            "RFC_Cliente": RFC_Cliente,
            "Correo_Cliente": Correo_Cliente,
            "Fecha": fecha_procesada.strftime('%d/%m/%Y'),
            "Servicios": servicios_nota,
            "Tipo_Cliente": tipo_cliente
            })
            
            agregar_otro = input("¿Desea agregar otro servicio o monto? (Sí/No): ").strip().lower()
            if agregar_otro != "si":
                break

        notas.append({
            "Folio": folio_actual,
            "Nombre_Cliente": Nombre_Cliente,
            "RFC_Cliente": RFC_Cliente,
            "Correo_Cliente": Correo_Cliente,
            "Fecha": fecha_procesada.strftime('%d/%m/%Y'),
            "Servicios": servicios_nota,
            "Tipo_Cliente": tipo_cliente
            })

    elif opcion == "2":
        while True:
            print("\nSubmenu - Consultas y Reportes:")
            print("1. Consultar nota por folio")
            print("2. Consultar Nota por Periodo de Fecha")
            print("3. Consultar por Cliente")
            print("4. Regresar al menú principal")

            opcion_consultas = input("Seleccione una opción para consultar (1, 2, 3, 4): ").strip()

            if opcion_consultas == "1":
                folio = input("Ingrese el folio de la nota a consultar: ")
                if folio.isdigit():
                    folio = int(folio)
                    if any(nota["Folio"] == folio for nota in notas) and folio not in notas_canceladas:
                        nota = next(nota for nota in notas if nota["Folio"] == folio)
                        print(f"Datos de la nota {folio}:")
                        print(f"Folio: {folio}")
                        print(f"Nombre del Cliente: {nota['Nombre_Cliente']}")
                        print(f"RFC del Cliente: {nota['RFC_Cliente']}")
                        print(f"Correo Electrónico del Cliente: {nota['Correo_Cliente']}")
                        print(f"Fecha: {datetime.datetime.strptime(nota['Fecha'], '%d/%m/%Y').date().strftime('%d/%m/%Y')}")
                        print("Servicios:")
                        for i, (servicio, monto) in enumerate(nota['Servicios'], start=1):
                            print(f"   {i}. {servicio}: ${monto}")
                    else:
                        print("La nota no existe o está cancelada.")
                else:
                    print("Entrada no válida. El folio debe ser un número entero.")


            elif opcion_consultas == "2":
                fecha_inicio = input("Ingrese la fecha de inicio en formato dd/mm/aaaa: ")
                fecha_fin = input("Ingrese la fecha de fin en formato dd/mm/aaaa: ")
                try:
                    fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%d/%m/%Y').date()
                    fecha_fin = datetime.datetime.strptime(fecha_fin, '%d/%m/%Y').date()
                    if fecha_inicio > fecha_fin:
                        print("La fecha de inicio no puede ser posterior a la fecha de fin.")
                        continue
                except ValueError:
                    print("Formato de fecha incorrecto. Introduce las fechas en el formato dd/mm/aaaa.")
                    continue
                notas_en_periodo = []
                for nota in notas:
                    fecha_nota = datetime.datetime.strptime(nota['Fecha'], '%d/%m/%Y').date()
                    if fecha_inicio <= fecha_nota <= fecha_fin and nota["Folio"] not in notas_canceladas:
                        notas_en_periodo.append((nota["Folio"], nota['Nombre_Cliente'], fecha_nota))
                if notas_en_periodo:
                    print("\nNotas en el período especificado:")
                    print("Folio   ", "Nombre del Cliente", "Fecha")
                    for folio, nombre, fecha in notas_en_periodo:
                        print(folio, nombre, fecha.strftime('%d/%m/%Y'))
                else:
                    print("\nNo hay notas emitidas para el período especificado.")
            
            elif opcion_consultas == "3":
                rfc_clientes = {}
                for nota in notas:
                    rfc = nota['RFC_Cliente']
                    if rfc in rfc_clientes:
                        rfc_clientes[rfc].append(nota)
                    else:
                        rfc_clientes[rfc] = [nota]
                print("\nListado de RFCs:")
                for i, rfc in enumerate(rfc_clientes.keys(), start=1):
                    print(f"{i}. {rfc}")
                rfc_seleccionado = input("Seleccione el número correspondiente al RFC a consultar o 'No' para cancelar: ").strip()
                if rfc_seleccionado.lower() == "no":
                    print("No se ha exportado ningún archivo.")
                elif rfc_seleccionado.isdigit():
                    rfc_seleccionado = int(rfc_seleccionado)
                    rfc_list = list(rfc_clientes.keys())
                    if 0 < rfc_seleccionado <= len(rfc_list):
                        rfc_elegido = rfc_list[rfc_seleccionado - 1]
                        
                        data = []
                        for nota in rfc_clientes[rfc_elegido]:
                            servicios = "\n".join([f"{i}. {servicio}: ${monto:.2f}" for i, (servicio, monto) in enumerate(nota['Servicios'], start=1)])
                            monto_total = calcular_monto(nota['Servicios'])
                            data.append([nota['Folio'], nota['Nombre_Cliente'], nota['Fecha'], servicios, monto_total])
                        df = pd.DataFrame(data, columns=["Folio", "Nombre Cliente", "Fecha", "Servicios", "Monto Total"])
                        fecha_hoy = datetime.date.today().strftime('%Y%m%d')
                        nombre_archivo = f"Reporte_{rfc_elegido}_{fecha_hoy}.xlsx"
                        exportar_a_excel = input(f"Desea exportar el reporte de {rfc_elegido} a Excel? (Sí/No): ").strip().lower()
                        if exportar_a_excel == "si":
                            df.to_excel(nombre_archivo, index=False)
                            print(f"Archivo exportado como {nombre_archivo}")
                        else:
                            print("No se ha exportado ningún archivo.")
                    else:
                        print("Número de RFC no válido.")
                else:
                    print("Entrada no válida. Seleccione un número de RFC válido.")
            elif opcion_consultas == "4":
                break
            else:
                print("Opción no válida. Seleccione 1, 2, 3 o 4.")
                
    elif opcion == "3":
        folio_cancelar = input("Ingrese el folio de la nota a cancelar: ")
        if folio_cancelar.isdigit() and int(folio_cancelar) in [nota["Folio"] for nota in notas]:
            folio_cancelar = int(folio_cancelar)
            if folio_cancelar in notas_canceladas:
                print("La nota ya está cancelada.")
            else:
                nota = next(nota for nota in notas if nota["Folio"] == folio_cancelar)
                print(f"Datos de la nota {folio_cancelar} a cancelar:")
                print(f"Folio: {folio_cancelar}")
                print(f"Nombre del Cliente: {nota['Nombre_Cliente']}")
                print(f"RFC del Cliente: {nota['RFC_Cliente']}")
                print(f"Correo Electrónico del Cliente: {nota['Correo_Cliente']}")
                print(f"Fecha: {nota['Fecha']}")
                print("Servicios:")
                for i, (servicio, monto) in enumerate(nota['Servicios'], start=1):
                    print(f"   {i}. {servicio}: ${monto}")
                    confirmacion = input("¿Desea cancelar esta nota? (Sí/No): ").strip().lower()
                    if confirmacion == "si":
                        notas_canceladas.add(folio_cancelar)
                        print(f"Nota {folio_cancelar} ha sido cancelada.")
                    else:
                        print(f"Nota {folio_cancelar} no ha sido cancelada.")
        else:
            print("Entrada no válida. El folio debe ser un número entero válido y corresponder a una nota existente.")
    
    elif opcion == "4":
        print("Notas actualmente canceladas:")
        notas_canceladas_tabla = [(folio, notas[folio]['Nombre_Cliente']) for folio in notas_canceladas]
        if notas_canceladas_tabla:
            print("Folio", "Nombre Cliente")
            for folio, nombre in notas_canceladas_tabla:
                print(folio, nombre)
            folio_recuperar = input("Ingrese el folio de la nota que desea recuperar, o escriba 'No' para cancelar: ").strip()
            if folio_recuperar.lower() == "no":
                print("No se ha recuperado ninguna nota.")
            elif folio_recuperar.isdigit():
                folio_recuperar = int(folio_recuperar)
                if folio_recuperar in notas_canceladas:
                    nota = next(nota for nota in notas if nota["Folio"] == folio_recuperar)
                    print(f"Detalle de la nota {folio_recuperar} a recuperar:")
                    print(f"Folio: {folio_recuperar}")
                    print(f"Nombre del Cliente: {nota['Nombre_Cliente']}")
                    print(f"RFC del Cliente: {nota['RFC_Cliente']}")
                    print(f"Correo Electrónico del Cliente: {nota['Correo_Cliente']}")
                    print(f"Fecha: {nota['Fecha']}")
                    print("Servicios:")
                    for i, (servicio, monto) in enumerate(nota['Servicios'], start=1):
                        print(f"   {i}. {servicio}: ${monto}")
                    confirmacion = input("¿Desea recuperar esta nota? (Sí/No): ").strip().lower()
                    if confirmacion == "si":
                        notas_canceladas.remove(folio_recuperar)
                        print(f"Nota {folio_recuperar} ha sido recuperada.")
                    else:
                        print(f"Nota {folio_recuperar} no ha sido recuperada.")
                else:
                    print("El folio no corresponde a una nota cancelada.")
            else:
                print("Entrada no válida. El folio debe ser un número entero.")
        else:
            print("No hay notas canceladas para recuperar.")


    elif opcion == "5":
        confirmacion_salir = input("¿Está seguro de que desea salir? (Sí/No): ").strip().lower()
        if confirmacion_salir == "si":
            with open("notas.csv", mode="w", newline="") as archivo_csv:
                escritor = csv.writer(archivo_csv)
                escritor.writerow(["Folio", "Nombre_Cliente", "RFC_Cliente", "Correo_Cliente", "Fecha", "Servicios"])
                for nota in notas:
                    folio = nota["Folio"]
                    nombre_cliente = nota["Nombre_Cliente"]
                    rfc_cliente = nota["RFC_Cliente"]
                    correo_cliente = nota["Correo_Cliente"]
                    fecha = nota["Fecha"]
                    servicios = "\n".join([f"{servicio}: ${monto:.2f}" for servicio, monto in nota["Servicios"]])
                    
                    escritor.writerow([folio, nombre_cliente, rfc_cliente, correo_cliente, fecha, servicios])
            print("Datos guardados en notas.csv")
            break
