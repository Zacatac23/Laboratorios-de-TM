import yaml
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import sys

@dataclass
class TapeState:
    """Representa el estado de la cinta en un momento dado"""
    content: List[str]
    head_position: int
    
    def __str__(self):
        tape_str = ""
        for i, symbol in enumerate(self.content):
            if i == self.head_position:
                tape_str += f"[{symbol if symbol else 'B'}]"
            else:
                tape_str += symbol if symbol else 'B'
        return tape_str

@dataclass
class InstantaneousDescription:
    """Descripción instantánea de la MT"""
    state: str
    tape: TapeState
    mem_cache: Optional[str]
    
    def __str__(self):
        left_part = ''.join([s if s else 'B' for s in self.tape.content[:self.tape.head_position]])
        current = self.tape.content[self.tape.head_position] if self.tape.head_position < len(self.tape.content) else 'B'
        right_part = ''.join([s if s else 'B' for s in self.tape.content[self.tape.head_position + 1:]])
        
        cache_str = f" (cache: {self.mem_cache if self.mem_cache else 'B'})" if self.mem_cache is not None else ""
        return f"{left_part}[q{self.state}]{current}{right_part}{cache_str}"

class TuringMachine:
    def __init__(self, config: Dict[str, Any]):
        """Inicializa la MT con la configuración del archivo YAML"""
        self.states = config['q_states']['q_list']
        self.initial_state = config['q_states']['initial']
        self.final_states = [config['q_states']['final']]
        self.alphabet = config['alphabet']
        self.tape_alphabet = config['tape_alphabet']
        self.delta = self._parse_transitions(config['delta'])
        self.blank_symbol = None  # Representado como None en Python
        
    def _parse_transitions(self, delta_list: List[Dict]) -> Dict[Tuple, Dict]:
        """Parsea las transiciones a un formato más accesible"""
        transitions = {}
        for trans in delta_list:
            params = trans['params']
            output = trans['output']
            
            # La clave es (estado_inicial, cache, input_cinta)
            key = (
                params['initial_state'],
                params.get('mem_cache_value'),
                params['tape_input']
            )
            
            value = {
                'next_state': output['final_state'],
                'mem_cache': output.get('mem_cache_value'),
                'tape_write': output['tape_output'],
                'movement': output['tape_displacement']
            }
            
            transitions[key] = value
            
        return transitions
    
    def _initialize_tape(self, input_string: str) -> List[str]:
        """Inicializa la cinta con el input"""
        # Agregar un blanco al inicio para que la MT pueda detectar el inicio
        tape = [None] + list(input_string)
        # Agregar espacios en blanco al final
        tape.extend([None] * 10)
        return tape
    
    def _get_transition(self, state: str, mem_cache: Optional[str], 
                       tape_symbol: Optional[str]) -> Optional[Dict]:
        """Busca una transición válida"""
        # Intentar con el símbolo exacto
        key = (state, mem_cache, tape_symbol)
        if key in self.delta:
            return self.delta[key]
        
        return None
    
    def simulate(self, input_string: str, max_steps: int = 1000) -> Tuple[bool, List[InstantaneousDescription]]:
        """Simula la ejecución de la MT con la cadena de entrada"""
        tape = self._initialize_tape(input_string)
        current_state = self.initial_state
        head_position = 1  # Empezar en posición 1 porque hay un blanco al inicio
        mem_cache = None
        
        ids_list = []
        
        # Descripción instantánea inicial
        initial_id = InstantaneousDescription(
            state=current_state,
            tape=TapeState(tape.copy(), head_position),
            mem_cache=mem_cache
        )
        ids_list.append(initial_id)
        
        step_count = 0
        
        while step_count < max_steps:
            # Verificar si estamos en estado final
            if current_state in self.final_states:
                return True, ids_list
            
            # Extender la cinta si es necesario
            while head_position >= len(tape):
                tape.append(None)
            
            # Leer símbolo actual
            current_symbol = tape[head_position] if head_position < len(tape) else None
            
            # Buscar transición
            transition = self._get_transition(current_state, mem_cache, current_symbol)
            
            if transition is None:
                # No hay transición válida, la MT se detiene
                return False, ids_list
            
            # Aplicar transición
            current_state = transition['next_state']
            mem_cache = transition.get('mem_cache')
            tape[head_position] = transition['tape_write']
            
            # Mover cabezal
            movement = transition['movement']
            if movement == 'R':
                head_position += 1
            elif movement == 'L':
                head_position = max(0, head_position - 1)
            # 'S' significa quedarse en el mismo lugar
            
            # Agregar nueva descripción instantánea
            new_id = InstantaneousDescription(
                state=current_state,
                tape=TapeState(tape.copy(), head_position),
                mem_cache=mem_cache
            )
            ids_list.append(new_id)
            
            step_count += 1
        
        # Se alcanzó el límite de pasos
        return False, ids_list

def load_config(filename: str) -> Dict[str, Any]:
    """Carga la configuración desde un archivo YAML"""
    with open(filename, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def print_simulation_results(input_string: str, accepted: bool, 
                            ids_list: List[InstantaneousDescription]):
    """Imprime los resultados de la simulación"""
    print(f"\n{'='*80}")
    print(f"SIMULACIÓN PARA LA CADENA: '{input_string}'")
    print(f"{'='*80}\n")
    
    print("DESCRIPCIONES INSTANTÁNEAS:")
    print("-" * 80)
    for i, id_desc in enumerate(ids_list):
        print(f"Paso {i}: {id_desc}")
    
    print("\n" + "-" * 80)
    if accepted:
        print("✓ RESULTADO: CADENA ACEPTADA")
    else:
        print("✗ RESULTADO: CADENA RECHAZADA")
    print("=" * 80 + "\n")

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso: python turing_simulator.py <archivo_config.yaml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        # Cargar configuración
        config = load_config(config_file)
        
        # Crear máquina de Turing
        tm = TuringMachine(config)
        
        print("\n" + "="*80)
        print("SIMULADOR DE MÁQUINAS DE TURING")
        print("="*80)
        print(f"\nEstados: {tm.states}")
        print(f"Estado inicial: q{tm.initial_state}")
        print(f"Estados finales: {['q' + s for s in tm.final_states]}")
        print(f"Alfabeto de entrada: {tm.alphabet}")
        print(f"Alfabeto de cinta: {[s if s else 'B' for s in tm.tape_alphabet]}")
        print(f"Número de transiciones: {len(tm.delta)}")
        
        # Simular cada cadena
        simulation_strings = config.get('simulation_strings', [])
        
        if not simulation_strings:
            print("\nNo hay cadenas para simular.")
            return
        
        print(f"\nCadenas a simular: {len(simulation_strings)}\n")
        
        for input_string in simulation_strings:
            accepted, ids_list = tm.simulate(input_string)
            print_simulation_results(input_string, accepted, ids_list)
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{config_file}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error al parsear el archivo YAML: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()