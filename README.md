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
