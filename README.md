# Generación y Limpieza de Gramática

## El Esperanto y su contexto
El esperanto es el idioma planificado (o lengua construida) más hablado en el mundo. Fue creado por el oftalmólogo polaco L. L. Zamenhof en 1887 con la publicación de su libro Unua Libro. La idea de Zamenhof era el crear un idioma auxiliar internacional que fuera neutral, fácil de aprender y que sirviera como una lengua universal que sirviera como apoyo en la comunicación entre personas de distintas culturas y lenguas. En otras palabras, buscaba que el esperanto fuera el nuevo idioma universal, replazando así el inglés.

### Características lingüísticas:
A diferencia de otros idiomas que evolucionan de manera desordenada y están llenos de irregularidades y excepciones, el esperanto fue diseñado de forma lógica y estructurada. Pertenece a la tipología de lenguas aglutinantes, lo que significa que las palabras se forman uniendo raíces invariables con una serie de afijos (prefijos y sufijos) regulares.

Sus reglas gramaticales son finitas y absolutas. El Fundamento de Esperanto, documento que establece las bases inmutables del idioma, define únicamente 16 reglas gramaticales fundamentales sin ninguna excepción. Por ejemplo, todos los sustantivos terminan sistemáticamente en la letra -o, todos los adjetivos en -a, y los verbos en infinitivo en -i.

### ¿Por qué Esperanto?
Más allá de que el idioma está diseñado específicamente para ser sencillo, y por ende, fácil de analizar, el esperanto presenta un caso de estudio ideal para la generación de Gramáticas Libres de Contexto. Su carencia de excepciones morfológicas y su estructura sintáctica predecible permiten una traducción casi directa a reglas de producción matemáticas.

## Construcción del Analizador Léxico

Antes de que la gramática analice la estructura de una oración, es importante tener un motor que identifique qué es cada palabra, siendo la mejor solución el utilizar expresiones regulares (Regex) pues el esperanto es perfecto para esto por sus terminaciones absolutas. Podemos definir patrones Regex para clasificar nuestros "tokens" automáticamente, por ejemplo:

- **Sustantivos (N):** Palabras que terminan en "o" (ej. `\b[a-z]+o\b`).

- **Adjetivos (Adj):** Palabras que terminan en "a" (ej. `\b[a-z]+a\b`).

- **Verbos (V):** Podemos capturar el presente, pasado y futuro con terminaciones como "as", "is", "os" (ej. `\b[a-z]+(as|is|os)\b`).

- **Artículos y Preposiciones:** Palabras fijas como "la", "en", "al".

### Diccionario Léxico y Expresiones Regulares

Para garantizar que el analizador léxico esté completo y sea robusto, lo mejor será establecer un conjunto de vocabulario clasificado por su categoría gramatical. Las siguientes expresiones regulares (Regex) serán el motor central para la "tokenización" de las cadenas de entrada, sofreciendo una solución de software directamente implementable.

1. **Sustantivos (N):**
En esperanto, todos los sustantivos terminan en `-o`. Para permitir el análisis de objetos directos (acusativo), se permite la terminación opcional `-on`, y para plurales `-oj` u `-ojn`.

    - **Regex:** `\b[a-z]+o[jn]?\b`

    - **Vocabulario soportado:** viro (hombre), hundo (perro), domo (casa), pomo (manzana), knabo (niño), kato (gato), birdo (pájaro), libro (libro), teleskopo (telescopio), parko (parque).
  
2. **Adjetivos (Adj):**
Terminan estrictamente en `-a` (o `-an` / `-aj` / `-ajn` por concordancia).

    - **Regex:** `\b[a-z]+a[jn]?\b`

    - **Vocabulario soportado:** granda (grande), bela (hermoso), blua (azul), rapida (rápido), bona (bueno), malgranda (pequeño).
  
3. **Verbos (V):**
Se capturarán los tiempos fundamentales: presente (`-as`), pasado (`-is`), futuro (`-os`) e infinitivo (`-i`).

    - **Regex:** `\b[a-z]+(as|is|os|i)\b`

    - **Vocabulario soportado:** vidas (ve), manĝas (come), havas (tiene), kuras (corre), legas (lee), flugas (vuela).

4. **Artículos Definidos (Art) y Preposiciones (Prep):**
Palabras invariables con función estrictamente estructural. El esperanto no tiene artículo indefinido.

    - **Regex (Art):** `\bla\b` (la / el / los / las).

    - **Regex (Prep):** `\b(en|kun|per|sub|sur)\b` (en, con, por medio de, debajo, sobre).

## Casos de estudio

Para validar la solidez del analizador sintáctico y documentar las pruebas requeridas con Autómatas de Pila o parsers LL1, se ha diseñado un corpus de 20 oraciones estructuradas. Este corpus incluye intencionalmente cadenas diseñadas para detonar ambigüedad y poner a prueba el manejo de la recursividad.

### Cadenas Aceptadas (Sintaxis Válida)

Estas oraciones están gramaticalmente correctas bajo el estándar SVO (Sujeto-Verbo-Objeto) y deberán generar un árbol de sintaxis exitoso.

1. `La viro vidas la hundon.` (Sintaxis básica SVO).

2. `La hundo kuras.`

3. `La granda bela blua birdo flugas.` (Caso especial: Diseñada para detonar recursividad izquierda mediante adjetivos múltiples).

4. `La knabo manĝas la bonan pomon.` (Uso de adjetivos en el objeto directo).

5. `La viro vidas la hundon per la teleskopo.` (Caso especial: Diseñada para detonar ambigüedad estructural. ¿Quién tiene el telesocopio, el hombre o el perro?).

6. `La kato kuras en la domo.` (Uso de frase preposicional).

7. `La granda viro legas la libron.`

8. `La blua birdo havas la pomon.`

9. `La knabo legas la libron en la granda domo.`

10. `La bela kato vidas la bluan birdon.`

11. `La knabo manĝas la pomon kun la hundo.` (Caso especial: Ambigüedad de adjunción preposicional).

12. `La malgranda hundo kuras sub la domo.`

### Cadenas Rechazadas (Sintaxis Inválida)

Estas oraciones contienen errores estructurales graves y el parser deberá rechazarlas, demostrando la robustez de las reglas libres de contexto implementadas.

1. `Vidas la viro hundon la.` (Orden completamente fracturado).

2. `La bela granda.` (Falta el sustantivo del sujeto).

3. `Manĝas en la domo.` (Ausencia de sujeto explícito).

4. `La viro la libro legas.` (Violación del orden SVO).

5. `Per domo la kuras kato.` (Preposición y artículos mal ubicados).

6. `La la hundo kuras.` (Duplicidad de tokens de artículo).

7. `Viro bela la vidas.` (Artículo pospuesto).

8. `Knabo manĝas la blua.` (Adjetivo sin sustantivo en el objeto directo).

<p align="center">
$S → NP VP$

<p align="center">
$NP → Art N$

<p align="center">
$NP → Art AdjList N$

<p align="center">
$NP → NP PP$

<p align="center">
$AdjList → AdjList Adj$

<p align="center">
$AdjList → Adj$

<p align="center">
$VP → V$

<p align="center">
$VP → V NP$

<p align="center">
$VP → VP PP$

<p align="center">
$PP → Prep NP$
</p>

### Análisis de los Problemas Inyectados en la Gramática Base

Esta gramática base presenta dos problemas fundamentales en la teoría de lenguajes formales que impiden que un analizador sintáctico (parser) descendente, como un LL(1), funcione correctamente:

#### 1. Recursividad Izquierda:
Una gramática es recursiva por la izquierda si existe una derivación $A →+ A\alpha$. Por ejemplo, si en un diccionaro buscaramos la palabra "universo" y la definición dice "Universo: El universo que contiene estrellas", como la definición contiene la propia palabra que se está buscando, nunca se termina de comprender qué significa. Igual en las reglas pasa algo similar en $AdjList → AdjList Adj$ donde básicamente decimos "Una lista de adjetivos es una lista de adjetivos a la que le agregas otro adjetivo".

Los programas que analizan texto (los "parsers descendentes") son máquinas que leen estrictamente de izquierda a derecha. Si el programa intenta entender qué es un $AdjList$, lee la regla y dice:

1. "Busco un $AdjList$".
2. "Para encontrarlo, la regla dice que primero debo buscar un $AdjList$".
3. "Busco un $AdjList$".
4. "La regla dice que para encontrarlo, primero debo buscar un $AdjList$".

El programa entra en un bucle infinito de buscar la definición de qué es un $AdjList$.

#### 2. Ambigüedad Estructural:
Una gramática es ambigua si puede generar más de un árbol de derivación (o árbol de sintaxis) válido para una misma cadena de entrada. En este modelo, la ambigüedad se introdujo mediante la frase preposicional ($PP$), la cual puede derivarse tanto desde un $NP$ como desde un $VP$.

**Demostración Visual:**

Para ilustrar la ambigüedad, utilizamos la oración de prueba número 5 de nuestro corpus:
"La viro vidas la hundon per la teleskopo" (El hombre ve al perro con el telescopio).

La gramática base permite dos interpretaciones válidas, generando dos árboles distintos:

- **Árbol A: Adjunción al Verbo (VP):**
  El hombre utiliza el telescopio como instrumento para ver al perro. La frase preposicional modifica al verbo.
  
                S
              /   \
            NP      VP
           / |     /  \
        Art  N   VP    PP
       (La)(viro) / \   /  \
                 V  NP Prep NP
            (vidas) /| (per) / \
                 Art N    Art   N
                (la)(hundon)(la)(teleskopo)
  
- **Árbol B: Adjunción al Sustantivo (NP):**
  Interpretación semántica: El hombre ve a un perro que tiene/posee un telescopio. La frase preposicional modifica al objeto directo.

                S
              /   \
            NP      VP
           / |     /  \
        Art  N    V    NP
       (La)(viro)(vidas)/ \
                      NP    PP
                     / |   /  \
                   Art N Prep NP
                 (la)(hundon)(per) / \
                                Art   N
                               (la)(teleskopo)

Al existir dos árboles de derivación por la izquierda para la misma cadena de entrada, queda formalmente demostrado que la gramática base es ambigua.

## Limpieza de la Gramática

### 1. Eliminación de la Ambigüedad

Para resolver el problema de que una oración genere dos árboles distintos, es necesario eliminar las reglas redundantes. En la gramática base, el problema es que la frase preposicional ($PP$) puede derivarse tanto del sustantivo ($NP$) como del verbo ($VP$).

### 2. Eliminación de Recursividad a la Izquierda

El problema principal de la recursividad izquierda es que obliga al analizador sintáctico a evaluar una regla de forma infinita antes de poder leer la primera palabra de la oración. Para solucionarlo, es posible aplicar un proceso de transformación matemática que convierte esta recursividad de "izquierda" a "derecha".

En lugar de definir una lista buscando primero la lista entera y luego su último elemento, la redefinimos buscando primero un elemento inicial, seguido de un nuevo símbolo auxiliar que se encargará de buscar si existen elementos adicionales siendo este el sufijo "prima.

**A) Transformación de la Lista de Adjetivos ($AdjList$)**

- **Regla original (sucia):** $AdjList \rightarrow AdjList \ Adj \mid Adj$
- **Regla transformada (limpia):** Extraemos el elemento inicial (el primer adjetivo) y le agregamos el símbolo auxiliar ($AdjList'$).
- $AdjList \rightarrow Adj \ AdjList'$
- $AdjList' \rightarrow Adj \ AdjList' \mid \epsilon$

**B) Transformación de la Frase Verbal ($VP$)**

- **Regla original (sucia):** $VP \rightarrow VP \ PP \mid V \mid V \ NP$
- **Regla transformada (limpia):** Extraemos las bases que inician la frase (un verbo solo, o un verbo con objeto) y les agregamos el símbolo auxiliar ($VP'$).
- $VP \rightarrow V \ VP' \mid V \ NP \ VP'$
- $VP' \rightarrow PP \ VP' \mid \epsilon$

## Implementación: NLTK y Análisis Computacional

Para la validación computacional de la gramática, se utilizó la biblioteca nltk (Natural Language Toolkit) de Python. Esta herramienta permite instanciar la Gramática Libre de Contexto limpia ($G_{limpia}$) y ejecutar un parser automático sobre el corpus de pruebas.

### Configuración de la Gramática en NLTK

La traducción de nuestras reglas matemáticas a código requiere definir explícitamente los terminales (el vocabulario validado previamente por nuestras expresiones regulares). NLTK utiliza un formato de cadena estricto para cargar las producciones.

```py

import nltk

# Definición de la Gramática Limpia en formato NLTK
grammar_string = """
  S -> NP VP
  NP -> Art N | Art AdjList N
  AdjList -> Adj AdjListPrima
  AdjListPrima -> Adj AdjListPrima | 
  VP -> V VPPrima | V NP VPPrima
  VPPrima -> PP VPPrima | 
  PP -> Prep NP

  Art -> 'la'
  N -> 'viro' | 'hundon' | 'hundo' | 'birdo' | 'knabo' | 'pomon' | 'teleskopo' | 'kato' | 'domo' | 'viro' | 'libron'
  Adj -> 'granda' | 'bela' | 'blua' | 'bonan' | 'malgranda' | 'bluan'
  V -> 'vidas' | 'kuras' | 'flugas' | 'manĝas' | 'legas' | 'havas'
  Prep -> 'per' | 'en' | 'kun' | 'sub'
"""

# Instanciación de la gramática
esperanto_cfg = nltk.CFG.fromstring(grammar_string)

# Instanciación del parser descendente
parser = nltk.ChartParser(esperanto_cfg)

```

Para procesar una oración, el analizador léxico (Regex) primero tokeniza la cadena de entrada en una lista de palabras (ej. [`'la', 'viro', 'vidas', 'la', 'hundon']`), la cual es evaluada por el `parser.parse()`. Las cadenas del corpus marcadas como aceptadas generan uno o más árboles, mientras que las rechazadas levantan una excepción al no encontrar una derivación válida, cumpliendo así con las pruebas documentadas.

### Documentación Formal: Análisis con Parser LL(1)

Para fundamentar teóricamente el éxito de las pruebas en la implementación de software, demostramos el comportamiento del analizador mediante la lógica de un parser LL(1).

Al haber eliminado la recursividad izquierda y factorizado la ambigüedad, se garantiza que por cada combinación de un símbolo no terminal (estado actual) y un símbolo terminal (token de entrada o lookahead), exista a lo sumo una única regla de producción aplicable.

### Tabla de Parseo LL(1) (Extracto Demostrativo)

La siguiente tabla ilustra cómo el analizador toma decisiones deterministas sin necesidad de retroceso (backtracking), evaluando la variable tope de la pila contra el token de entrada actual.

| No Terminal / Token | la (Art) | granda (Adj) | vidas (V) | per (Prep) | $ (Fin de cadena) |
|:--------------------|:---------|:-------------|:----------|:-----------|:------------------|
| S | $S \rightarrow NP \ VP$| - | - | - | - |
| NP | $NP \rightarrow Art \ N$ o $Art \ AdjList \ N$ | - | - | - | - |
| AdjList | - | $AdjList \rightarrow Adj \ AdjList'$ | - | - | - |
| AdjList' | - | $AdjList' \rightarrow Adj \ AdjList'$ | $AdjList' \rightarrow \epsilon$ | - | - |
| VP | - | - | $VP \rightarrow V \ VP'$ o $V \ NP \ VP'$ | - | - |
| VP' | - | - | - | $VP' \rightarrow PP \ VP'$ | $VP' \rightarrow PP \ VP'$ | $VP' \rightarrow \epsilon$ |

## Análisis Teórico y Complejidad

### Jerarquía de Chomsky: Antes y Después de la Limpieza

La jerarquía de Chomsky clasifica los lenguajes formales en cuatro niveles (Tipos 0 al 3) según las restricciones impuestas a sus reglas de producción.

#### Antes de la limpieza ($G_{sucia}$):
La gramática base con ambigüedad y recursividad izquierda pertenece al Tipo 2: Lenguajes Libres de Contexto (CFL). Las producciones tienen la forma estricta $A \rightarrow \gamma$, donde $A$ es un único símbolo no terminal y $\gamma$ es una cadena de terminales y/o no terminales. Su evaluación requiere la memoria de un Autómata de Pila (PDA).

#### Después de la limpieza ($G_{limpia}$):
Tras eliminar la ambigüedad y la recursividad izquierda, el nivel de la gramática en la jerarquía de Chomsky no cambia; sigue siendo de Tipo 2.

Sin embargo, aunque pertenece a la misma categoría principal, la gramática limpia ahora forma parte de un subconjunto estricto y mucho más restrictivo dentro del Tipo 2: las Gramáticas LL(1) (o Lenguajes Libres de Contexto Deterministas). Las transformaciones matemáticas no alteraron el poder expresivo del lenguaje (sigue pudiendo modelar el esperanto), pero sí optimizaron su estructura topológica para garantizar el determinismo computacional.

#### Implicaciones de la Complejidad Temporal

El impacto real de la transformación gramatical se refleja directamente en el tiempo de ejecución de los algoritmos de parseo.

Si intentamos analizar la gramática original con programas básicos, el sistema entrará en un ciclo infinito debido a la recursividad. Para obligar a la computadora a procesar esta gramática "sucia" y resolver sus ambigüedades, tendríamos que usar algoritmos mucho más pesados (como CYK o Earley). El gran inconveniente es que estos métodos son lentos; su tiempo de ejecución crece de forma cúbica, lo que se representa formalmente como $O(n^3)$, dependiendo de cuántas palabras tenga la oración. En la práctica, esto exige demasiado esfuerzo a la computadora y se vuelve ineficiente al analizar textos largos.

En cambio, al corregir las reglas matemáticas, nos aseguramos de poder usar un analizador eficiente (LL1) que lee la oración de izquierda a derecha en una sola pasada, sin tener que adivinar ni volver sobre sus propios pasos. Gracias a esto, el programa tarda exactamente lo mismo en procesar cada palabra de manera individual. El tiempo total de ejecución se vuelve directamente proporcional a la longitud de la oración, logrando una complejidad lineal de $O(n)$. Básicamente, la limpieza de la gramática nos permitió pasar de un sistema lento y costoso a uno sumamente rápido, ideal para implementarse en aplicaciones de software reales.
