# Laboratorio 7 - Simplificación de Gramáticas Libres de Contexto

**Universidad del Valle de Guatemala**  
**Facultad de Ingeniería**  
**Ingeniería en Ciencia de la Computación y Tecnologías de la Información**

## Descripción

Este laboratorio implementa algoritmos para la simplificación de gramáticas libres de contexto (CFGs), específicamente la eliminación de producciones-ε (épsilon).

## Estructura del Repositorio

```
├── README.md
├── ejercicio1/
│   └── ejercicio1_solucion.pdf
├── ejercicio2/
│   ├── cfg_processor.py
│   ├── grammar1.txt
│   ├── grammar2.txt
│   └── requirements.txt
└── docs/
    └── demo_video.md
```

## Ejercicio 1 (50%)

Transformación manual de dos CFGs a través de los siguientes pasos:
1. Eliminación de producciones-ε
2. Eliminación de producciones unitarias
3. Eliminación de símbolos inútiles
4. Conversión a Forma Normal de Chomsky (CNF)

**Archivo**: `ejercicio1/ejercicio1_solucion.pdf`

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

## Demostración en Video

El video de demostración (máximo 10 minutos) muestra:

### Contenido del Video:
1. **Introducción** (30 seg):
   - Presentación del laboratorio
   - Explicación de las gramáticas a procesar

2. **Ejecución normal** (3-4 min):
   - Carga de `grammar1.txt`
   - Proceso paso a paso de eliminación de ε-producciones
   - Resultado final de Grammar 1

3. **Continuación con Grammar 2** (3-4 min):
   - Carga de `grammar2.txt`
   - Proceso completo de eliminación
   - Análisis del resultado

4. **Demostración de validación** (2-3 min):
   - Introducción de errores en archivos
   - Muestra de cómo el programa detecta errores
   - Ejemplos de diferentes tipos de errores

5. **Conclusiones** (30 seg):
   - Resumen de resultados
   - Verificación de que el algoritmo funciona correctamente

### Script para la Demostración:

```bash
# 1. Mostrar los archivos de gramática
echo "=== Contenido de grammar1.txt ==="
cat grammar1.txt
echo ""
echo "=== Contenido de grammar2.txt ==="
cat grammar2.txt
echo ""

# 2. Ejecutar el programa principal
python cfg_processor.py

# 3. Mostrar ejemplo de archivo con errores (opcional)
echo "=== Ejemplo de archivo con errores ==="
echo "s -> 0S0 | 1S1 | ε  # Error: minúscula
A => ε                   # Error: flecha incorrecta
B -> S | A
invalid line             # Error: formato inválido" > grammar_error.txt
cat grammar_error.txt
```

**Link del video**: [Agregar link de YouTube aquí]

### Puntos Clave a Mencionar en el Video:
- Explicar qué son las producciones-ε y por qué se eliminan
- Mostrar cómo el algoritmo identifica símbolos anulables
- Explicar la generación de combinaciones (2^n casos)
- Demostrar la robustez de la validación con regex

## Ejemplo de Salida

```
=== PROCESANDO GRAMMAR1.TXT ===

=== Cargando gramática desde grammar1.txt ===
Línea 1: S -> 0S0 | 1S1 | ε
Línea 2: A -> ε
Línea 3: B -> S | A
Línea 4: C -> S | ε
✅ Gramática cargada exitosamente

=== Gramática Original ===
A -> ε
B -> S | A
C -> S | ε
S -> 0S0 | 1S1 | ε

============================================================
ALGORITMO PARA ELIMINAR PRODUCCIONES-ε
============================================================

=== Paso 1: Encontrando símbolos anulables ===

Iteración 1:
  A es anulable (producción directa: A -> ε)
  C es anulable (producción directa: C -> ε)
  S es anulable (producción directa: S -> ε)

Iteración 2:
  B es anulable (todos los símbolos en 'A' son anulables)

Iteración 3:
  No se encontraron nuevos símbolos anulables

Símbolos anulables encontrados: ['A', 'B', 'C', 'S']

=== Paso 2: Generando nuevas producciones ===
...
```

## Tecnologías Utilizadas

- **Python 3.8+**
- **Expresiones regulares** (módulo `re`)
- **Itertools** para generación de combinaciones

## Autor

[Tu nombre]  
[Tu carnet]  
Universidad del Valle de Guatemala

## Notas

- El programa maneja automáticamente la validación de entrada
- Se incluye demostración de manejo de errores
- La salida es detallada para mostrar cada paso del algoritmo
- Compatible con diferentes formatos de espaciado en archivos de entrada