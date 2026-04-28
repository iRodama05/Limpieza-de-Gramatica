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
