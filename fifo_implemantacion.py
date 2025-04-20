"""
Implementación del algoritmo FIFO para reemplazo de páginas
Sistema con segmentación y paginación (8 bits de dirección)
Cada dirección es traducida correctamente según la tabla de segmentos
"""

class MemorySystem:
    def __init__(self):
        self.segments = {
            '.text': {'base': 0x00, 'limit': 0x1A},
            '.data': {'base': 0x40, 'limit': 0x28},
            '.heap': {'base': 0x80, 'limit': 0x1F},
            '.stack': {'base': 0xC0, 'limit': 0x22}
        }
      
        self.page_size = 16
        
        self.physical_frames = 3
        
        
        self.frames = [None] * self.physical_frames
        
        
        self.fifo_queue = []
        
        self.page_faults = 0
        
    def get_segment_and_offset(self, address):
        
        for name, segment in self.segments.items():
            base = segment['base']
            limit = segment['limit']
            
            
            if base <= address < base + limit:
                offset = address - base
                return name, offset
                
        return None, None
    
    def get_page_number(self, offset):
        
        return offset // self.page_size
    
    def get_page_offset(self, offset):
        
        return offset % self.page_size
    
    def access_memory(self, address):
        
        segment, offset = self.get_segment_and_offset(address)
        
        if segment is None:
            return f"Error de segmentación: Dirección 0x{address:02X} fuera de los límites de los segmentos"
        
        page_number = self.get_page_number(offset)
        page_offset = self.get_page_offset(offset)
        
        
        page_id = f"{segment}:{page_number}"
        

        if page_id in self.frames:
            frame_index = self.frames.index(page_id)
            return f"Acceso a 0x{address:02X} -> {segment} (offset {offset}), Página {page_number}, Desplazamiento {page_offset} -> En marco {frame_index}, No hay fallo de página"
        
        self.page_faults += 1
        
        
        if None in self.frames:
            frame_index = self.frames.index(None)
            self.frames[frame_index] = page_id
            self.fifo_queue.append(page_id)
            return f"Acceso a 0x{address:02X} -> {segment} (offset {offset}), Página {page_number}, Desplazamiento {page_offset} -> Cargada en marco {frame_index}, Fallo de página #{self.page_faults}"
        
        
        victim_page = self.fifo_queue.pop(0)
        frame_index = self.frames.index(victim_page)
        self.frames[frame_index] = page_id
        self.fifo_queue.append(page_id)
        
        return f"Acceso a 0x{address:02X} -> {segment} (offset {offset}), Página {page_number}, Desplazamiento {page_offset} -> Reemplaza página {victim_page} en marco {frame_index}, Fallo de página #{self.page_faults}"

def main():
    memory = MemorySystem()
    
    references = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
    
    print("Simulación de algoritmo FIFO para reemplazo de páginas")
    print("Sistema con 3 marcos físicos")
    print("=================================================\n")
    
    print("Información de segmentos:")
    print("  .text:  Base 0x00, Límite 0x1A")
    print("  .data:  Base 0x40, Límite 0x28")
    print("  .heap:  Base 0x80, Límite 0x1F")
    print("  .stack: Base 0xC0, Límite 0x22")
    print("Tamaño de página: 16 palabras (2 bytes por palabra)\n")
    
    print("Estado inicial: Marcos físicos vacíos\n")
    
 
    for i, ref in enumerate(references):
        result = memory.access_memory(ref)
        print(f"Referencia #{i+1}: {result}")
        print(f"  Estado de marcos: {memory.frames}")
        print(f"  Cola FIFO: {memory.fifo_queue}\n")
    
    print(f"Total de fallos de página: {memory.page_faults}")

if __name__ == "__main__":
    main()
