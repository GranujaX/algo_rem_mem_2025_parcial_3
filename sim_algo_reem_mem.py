page_size = 16 

def procesar(segmentos, reqs, marcos_libres):
    tabla_segmentos = {nombre: {"base": base, "limit": limit} for (nombre, base, limit) in segmentos}
    marcos_ocupados = {}  
    fifo_queue = []       
    resultados = []

    for req in reqs:
        segmento_actual = None
        offset = None

        for nombre, info in tabla_segmentos.items():
            base = info["base"]
            limit = info["limit"]
            if base <= req < base + limit:
                segmento_actual = nombre
                offset = req - base
                break

        if segmento_actual is None:
            resultados.append((req, 0x1FF, "Segmentation Fault"))
            continue

        # Calcular página y desplazamiento
        num_pagina = offset // page_size
        desplazamiento = offset % page_size
        page_id = f"{segmento_actual}:{num_pagina}"

        if page_id in marcos_ocupados:
            marco = marcos_ocupados[page_id]
            direccion_fisica = (marco * page_size) + desplazamiento
            resultados.append((req, direccion_fisica, "Marco ya estaba asignado"))
            continue

       
        if marcos_libres:
            marco_asignado = marcos_libres.pop(0)
            marcos_ocupados[page_id] = marco_asignado
            fifo_queue.append(page_id)
            direccion_fisica = (marco_asignado * page_size) + desplazamiento
            resultados.append((req, direccion_fisica, "Marco libre asignado"))
            continue


        pagina_victima = fifo_queue.pop(0)
        marco_victima = marcos_ocupados[pagina_victima]
        del marcos_ocupados[pagina_victima]

        marcos_ocupados[page_id] = marco_victima
        fifo_queue.append(page_id)

        direccion_fisica = (marco_victima * page_size) + desplazamiento
        resultados.append((req, direccion_fisica, "Marco asignado"))

    return resultados


if __name__ == "__main__":
    marcos_libres = [0x0, 0x1, 0x2]
    reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
    segmentos = [
        ('.text', 0x00, 0x1A),
        ('.data', 0x40, 0x28),
        ('.heap', 0x80, 0x1F),
        ('.stack', 0xC0, 0x22)
    ]

    resultados = procesar(segmentos, reqs, marcos_libres)
    for req, direccion, accion in resultados:
        print(f"Req: 0x{req:02x} Direccion Fisica: 0x{direccion:02x} Acción: {accion}")
