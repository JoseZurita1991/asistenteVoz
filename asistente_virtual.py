import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import pyautogui
import time

# OPCIONES DE VOZ / IDIOMA
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
id3 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id4 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'


# ESCUCHAR MICRÓFONO Y DEVOLVER AUDIO COMO TEXTO
def trasformar_audio_en_texto():

    # Almacenar recognizer en una variable
    r = sr.Recognizer()

    # Configurar micrófono
    with sr.Microphone() as origen:

        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar al usuario de que puede hablar
        print("Ya puedes hablar")

        # Guardar el audio del usuario como una variable
        audio = r.listen(origen)

        try:
            # Buscar en Google
            pedido = r.recognize_google(audio, language="es-ES")

            # Mensaje del reconocimiento
            print("Has dicho: " + pedido)

            # Devolver la petición
            return pedido

        # En caso de que no se comprenda el audio
        except sr.UnknownValueError:

            # Mensaje de que no comprendio el audio
            print("Ups, no te he entendido")

            # Devolver error
            return "Sigo esperando"

        # En caso de no resolver la petición
        except sr.RequestError:

            # Mensaje de que no se comprendio el audio
            print("Ups, no hay servicio")

            # Devolver error
            return "Sigo esperando"

        # Error inesperado
        except:

            # Mensaje de que no se comprendio el audio
            print("Ups, algo salió mal")

            # Devolver error
            return "Sigo esperando"


# Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # Activar el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id4)

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar el dia de la semana
def pedir_dia():

    # Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario con nombres de dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # Decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# Informar que hora es
def pedir_hora():

    # Crear una variable con los datos de la hora
    hora = datetime.datetime.now()
    hora = f'Son las {hora.hour} horas y {hora.minute} minutos'
    print(hora)

    # Decir la hora
    hablar(hora)


# Funcion para el saludo inicial
def saludo_inicial():

    # Crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    # Decir el saludo
    hablar(f'{momento}, soy Pylar, tu asistente personal. Por favor, dime en qué te puedo ayudar')

# Función para captura de pantalla
def capturar_pantalla():
    # Obtener la marca de tiempo actual
    marca_tiempo = time.strftime("%d%m%Y_%H%M%S")
    # Capturar la pantalla y guardarla como una imagen con marca de tiempo en el nombre
    nombre_archivo = f'Screenshot_{marca_tiempo}.png'
    imagen = pyautogui.screenshot()
    imagen.save(nombre_archivo)
    hablar('Captura de pantalla realizada')

# Funcion central del asistente
def pedir_cosas():

    # Activar saludo inicial
    saludo_inicial()

    # Variable de corte
    continuar = True

    # Loop central
    while continuar:

        # Activar el micro y guardar el pedido en un string
        pedido = trasformar_audio_en_texto().lower()

        if 'abre youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
        elif 'abre el navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
        elif 'qué día es hoy' in pedido:
            pedir_dia()
        elif 'qué hora es' in pedido:
            pedir_hora()
        elif 'busca en wikipedia' in pedido:
            hablar(f'Perfecto, voy a buscarlo...')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Según Wikipedia:')
            hablar(resultado)
        elif 'busca en internet' in pedido:
            hablar('Okey, ahora mismo lo busco...')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
        elif 'reproduce' in pedido:
            hablar('Buena idea, voy a reproducirlo')
            pywhatkit.playonyt(pedido)
        elif 'captura' in pedido:
            capturar_pantalla()
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'AAPL', 'amazon': 'AMZN', 'google': 'GOOGL'}
            try:
                accion_buscada = cartera.get(accion.lower())
                if accion_buscada:
                    accion_buscada = yf.Ticker(accion_buscada)
                    precio_actual = accion_buscada.info['regularMarketPrice']
                    hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                else:
                    hablar("Perdón pero no la he encontrado")
            except Exception as e:
                hablar("Hubo un error al obtener el precio de las acciones")
                print(e)
        elif 'adiós' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            continuar = False
        else:
            hablar("Lo siento, pero no te entendí. ¿Hay algo más en lo que pueda ayudarte?")

# Llamar a la función principal
pedir_cosas()