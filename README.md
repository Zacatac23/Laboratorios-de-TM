# Laboratorio 7 - Simplificación de Gramáticas Libres de Contexto

**Universidad del Valle de Guatemala**  
**Facultad de Ingeniería**  
**Ingeniería en Ciencia de la Computación y Tecnologías de la Información**

## Descripción

Este laboratorio implementa algoritmos para la simplificación de gramáticas libres de contexto (CFGs), específicamente la eliminación de producciones-ε (épsilon).

## Estructura del Repositorio

```
.
├── cfg_processor.py
├── Documento
│   └── lab7.pdf
├── grammar1.txt
├── grammar2.txt

```

## Ejercicio 1 (50%)

Transformación manual de dos CFGs a través de los siguientes pasos:
1. Eliminación de producciones-ε
2. Eliminación de producciones unitarias
3. Eliminación de símbolos inútiles
4. Conversión a Forma Normal de Chomsky (CNF)

**Archivo**: `Documento/lab7.pdf`

## Ejercicio 2 (50%)

Implementación en Python de un programa que elimina producciones-ε de gramáticas libres de contexto.

### Características del Programa

- **Validación de entrada**: Utiliza expresiones regulares para validar el formato de las producciones
- **Carga de archivos**: Procesa archivos de texto con gramáticas
- **Algoritmo de eliminación**: Implementa el algoritmo completo para eliminar producciones-ε
- **Salida detallada**: Muestra el proceso paso a paso

### Archivos del Programa

- `cfg_processor.py`: Programa principal
- `grammar1.txt`: Primera gramática de prueba
- `grammar2.txt`: Segunda gramática de prueba

### Instalación y Ejecución

1. Clonar el repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd laboratorio7
```

2. Navegar al directorio del ejercicio 2
```bash
cd ejercicio2
```

3. Ejecutar el programa
```bash
python cfg_processor.py
```

### Gramáticas de Prueba

**Gramática 1:**
```
S -> 0S0 | 1S1 | ε
A -> ε
B -> S | A
C -> S | ε
```

**Gramática 2:**
```
S -> aAa | bBb | ε
A -> C | a
B -> C | b
C -> CDE | ε
D -> A | B | ab
```

## Funcionalidades Implementadas

### Validación con Regex
- Verifica formato correcto: `[No-terminal] -> [producciones]`
- Valida que no-terminales sean letras mayúsculas
- Verifica que terminales sean letras minúsculas o dígitos
- Permite múltiples producciones separadas por `|`

### Algoritmo de Eliminación de ε-producciones

1. **Identificación de símbolos anulables**:
   - Encuentra símbolos que derivan directamente ε
   - Encuentra símbolos que derivan indirectamente ε

2. **Generación de nuevas producciones**:
   - Para cada producción con símbolos anulables
   - Genera todas las combinaciones posibles (2^n casos)
   - Elimina duplicados

3. **Limpieza**:
   - Remueve todas las producciones-ε
   - Elimina símbolos que solo tenían producciones-ε



**Link del video**: https://www.youtube.com/watch?v=ECAItk06u-4



## Autor

Jonathan Zacarias , Hugo Barillas  
231104 , 
Universidad del Valle de Guatemala
