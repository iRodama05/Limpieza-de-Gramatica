import nltk
# Es posible que haga falta usar pip install nltk en una terminal

# 1. Definición de la Gramática Limpia
grammar_string = """
  S -> NP VP
  NP -> Art N | Art AdjList N
  AdjList -> Adj AdjListPrima
  AdjListPrima -> Adj AdjListPrima | 
  VP -> V VPPrima | V NP VPPrima
  VPPrima -> PP VPPrima | 
  PP -> Prep NP

  Art -> 'la'
  N -> 'viro' | 'hundon' | 'hundo' | 'birdo' | 'knabo' | 'pomon' | 'teleskopo' | 'kato' | 'domo' | 'libron'
  Adj -> 'granda' | 'bela' | 'blua' | 'bonan' | 'malgranda' | 'bluan'
  V -> 'vidas' | 'kuras' | 'flugas' | 'manĝas' | 'legas' | 'havas'
  Prep -> 'per' | 'en' | 'kun' | 'sub'
"""

# 2. Cargar la gramática en NLTK
esperanto_cfg = nltk.CFG.fromstring(grammar_string)

# 3. Crear el parser
parser = nltk.ChartParser(esperanto_cfg)

# 4. Función de prueba para procesar oraciones
def probar_oracion(oracion):
    print(f"\nAnalizando: '{oracion}'")
    # Tokenización simple
    tokens = oracion.lower().split()
    
    try:
        # parser.parse devuelve un generador con los árboles válidos
        arboles = list(parser.parse(tokens))
        
        if len(arboles) > 0:
            print("La oración es sintácticamente correcta.")
            for arbol in arboles:
                print(arbol) # Imprime el árbol en la consola
                arbol.draw()
        else:
            print("No se pudo construir un árbol (Sintaxis inválida).")
            
    except ValueError as e:
        # NLTK lanza ValueError si una palabra no existe en el diccionario (terminales)
        print(f"(Error Léxico): {e}")

# ==========================================
# Zona de Pruebas
# ==========================================

print("--- PRUEBAS DE CADENAS ACEPTADAS ---")
probar_oracion("la viro vidas la hundon")
probar_oracion("la granda bela blua birdo flugas")
probar_oracion("la viro vidas la hundon per la teleskopo")

print("\n--- PRUEBAS DE CADENAS RECHAZADAS ---")
probar_oracion("vidas la viro hundon la")
probar_oracion("la bela granda")
