#Archivo para declarar constantes de la aplicacion

TITULO_INTERFAZ = "Othello"
TITULO = "OTHELLO"

#Dimensiones
VENTANA_LARGO = 700
VENTANA_ANCHO = 1100
ORIGEN_MARGO = {'x':30,'y':30}
ORIGEN_TABLERO = {'x':117,'y':117}
FIN_MARCO = {'x':667,'y':667}
FIN_TABLERO = {'x':583,'y':583}
DIM_TABLERO = FIN_TABLERO['x']-ORIGEN_TABLERO['x']
CELDAS = 8
DIM_CELDA = DIM_TABLERO / CELDAS
DIM_FICHA = DIM_CELDA
LOCALIZACION_CENTRO_DERECHA =  FIN_MARCO['x'] + ((VENTANA_ANCHO - FIN_MARCO['x']) //2 )
DIM_TAPA_TEXTO = {'x':200,'y':45}
DIM_BOTON_GUARDADO = 45

#Turno 
TURNO = "TURNO:"
DIM_FICHA_TURNO = DIM_FICHA/1.5

#Movimientos
INICIO_TEXTO_MOVIMIENTOS = {"x": LOCALIZACION_CENTRO_DERECHA, "y":ORIGEN_MARGO['y'] + 50}
DISTANCIA_TEXTO_MOVIMIENTOS = 25
DIM_FICHA_MOVIMIENTO = DIM_FICHA_TURNO/1.5
OFFSET_UNO_MOVIMIENTO = -80
OFFSET_DOS_MOVIMIENTO = 50
OFFSET_TRES_MOVIMIENTO = 180
MAXIMO_MOVIMIENTOS_TEXTO = 20
SEPARACION_FICHA_TEXTO = 100

#Fuentes
FUENTE = "../Fuentes/KarmaSuture.ttf"
FUENTE_TITULO = "../Fuentes/KarmaSuture.ttf"
ESPACIADO_TITULO = 2
ESPACIADO_TURNO = 1
ESPACIADO_GANADOR = 1
ESPACIADO_BOTONES = 1
ESPACIADO_MOVIMIENTOS = 1

#Imagenes
IMG_TABLERO = "../Assets/Board-othello.png"
IMG_FICHA_BLANCA = "../Assets/Pieza-blanca.png"
IMG_FICHA_NEGRA = "../Assets/Pieza-negra.png"
IMG_FICHA_BLANCA_SEMITRANSPARENTE = "../Assets/Pieza-blanca-semitransparente.png"
IMG_FICHA_NEGRA_SEMITRANSPARENTE = "../Assets/Pieza-negra-semitransparente.png"
IMG_FONDO_MENU_PRINCIPAL = "../Assets/Fondo-Menu-Tablero.png"
IMG_FONDO_JUEGO = "../Assets/Fondo-Menu.png"
IMG_BOTON = "../Assets/Boton.png"
IMG_BOTON_ENCIMA = "../Assets/Boton-Encima.png"
IMG_TAPA_TEXTO = "../Assets/Tapar-Texto.png"
IMG_CELDA_OSCURA = "../Assets/Celda-Oscura.png"
IMG_CELDA_CLARA = "../Assets/Celda-Clara.png"
IMG_GUARDAR_PARTIDA = "../Assets/Guardar-Partida.png"

#Fichas
FICHA_BLANCA = 'blanca'
FICHA_NEGRA = 'negra'

#Botones
ANCHURA_BOTON = 250
ALTURA_BOTON = 100
ANCHURA_BOTON_GUARDADO = 250
ALTURA_BOTON_GUARDADO = 70
TEXTO_BOTON_IA = "1 VS IA"
TEXTO_BOTON_JUGADORES = "1 VS 1"
TEXTO_BOTON_GUARDADO = "GUARDAR RESULTADO"

#Colores RGB
BLANCO_RGB = (255,255,255)
NEGRO_RGB = (0,0,0)
MARRON_RGB = (104,68,53)
VERDE_RGB = (45,86,50)

#Jugadores
BLANCO = 2
NEGRO = 1
P1 = 1
P2 = 2

#Tablero 
VACIO = 0
CASILLAS_TABLERO = 64
VALOR_COLUMNAS = {"0":"A","1":"B","2":"C","3":"D","4":"E","5":"F","6":"G","7":"H"}
VALOR_FILAS = {"0":"1","1":"2","2":"3","3":"4","4":"5","5":"6","6":"7","7":"8"}
A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6 
H = 7

#Ganador
BLANCAS = "GANAN BLANCAS"
NEGRAS = "GANAN NEGRAS"
EMPATE = "EMPATE"
JUGADOR1_GANA = 1
JUGADOR2_GANA = 2
EMPATE_ENTRE_JUGADORES = 0

#Celdas
CELDAS_OSCURAS = [(0,A),(0,C),(0,E),(0,G),(1,B),(1,D),(1,F),(1,H),(2,A),(2,C),(2,E),(2,G),(3,B),(3,D),(3,F),(3,H),
                  (4,A),(4,C),(4,E),(4,G),(5,B),(5,D),(5,F),(5,H),(6,A),(6,C),(6,E),(6,G),(7,B),(7,D),(7,F),(7,H)]

ESQUINAS = [(0,A),(7,A),(0,H),(7,H)]
ESQUINAS_CODIGO = {'00': (0,A), '70': (7,A), '07': (0,H), '77': (7,H)}

ADYACENTES_ESQUINAS = {'00': [(0,B),(1,A)], '70': [(6,A),(7,B)], '07': [(0,G),(1,H)], '77': [(7,G),(6,H)]}

#Inteligencia Artificial
PARTIDAS = 30
EVALUADOR_RANDOM = 0
EVALUADOR_FICHAS = 1
EVALUADOR_MOVILIDAD = 2
EVALUADOR_ESQUINAS = 3
EVALUADOR_COMBINADO = 4
EVALUADOR_PESOS = 5

PESOS_TABLERO = [
    [ 100, -75,  50,  50,  50,  50, -75,  100],
    [-75, -100, -25, -25, -25, -25, -100, -75],
    [ 50, -25,  25,  0,  0,  25, -25,  50],
    [ 50, -25,  0,  25,  25,  0, -25,  50],
    [ 50, -25,  0,  25,  25,  0, -25,  50],
    [ 50, -25,  25,  0,  0,  25, -25,  50],
    [-75, -100, -25, -25, -25, -25, -100, -75],
    [ 100, -75, 50,  50,  50,  50, -75,  100]
]

MAXIMA_PROFUNDIDAD_MINIMAX = 6

#Valores evaluador random
MIN_PUNTUACION = -100
MAX_PUNTUACION = 100
EMPATE = 0


