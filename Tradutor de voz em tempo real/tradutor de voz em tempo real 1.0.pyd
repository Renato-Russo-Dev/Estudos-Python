import pyaudio
import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import time
import sys
from concurrent.futures import ThreadPoolExecutor

def wait_for_user():
    """
    Função para pausar e esperar o usuário pressionar Enter para continuar.
    """
    input("Pressione Enter para continuar com outra tradução...")

def main():
    # Inicializando o reconhecedor de fala, tradutor e engine de texto para fala
    recognizer = sr.Recognizer()
    translator = Translator()
    engine = pyttsx3.init()

    # Função para converter texto para fala
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # Função para traduzir texto
    def translate_text(text):
        return translator.translate(text, src='pt', dest='en').text

    # Função para reconhecer fala
    def recognize_speech(source):
        try:
            # Informar ao usuário sobre o tempo limite
            print("\nFale agora. Estou lhe escutando. Você tem quinze segundos para falar.")
            
            # Captura o áudio
            audio_data = recognizer.listen(source, timeout=15)  # Tempo limite ajustado para quinze segundos
            
            print("Voz escutada.")
            return audio_data
        except sr.WaitTimeoutError:
            print("Tempo de escuta expirado. Nenhuma voz detectada.")
            return None
        except Exception as e:
            print(f"Erro ao reconhecer fala: {e}", file=sys.stderr)
            return None

    # Inicializando o microfone
    mic = sr.Microphone()

    # Verificando as configurações do microfone
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

    except Exception as e:
        print(f"Erro ao inicializar o microfone: {e}", file=sys.stderr)
        return

    # Inicializando o ThreadPoolExecutor com até quatro threads
    executor = ThreadPoolExecutor(max_workers=4)

    try:
        while True:
            try:
                # Usando o Microphone como contexto
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)

                    # Usando o ThreadPoolExecutor para realizar o reconhecimento de fala em paralelo
                    future_audio = executor.submit(recognize_speech, source)
                    audio_data = future_audio.result()  # Bloqueia até o reconhecimento ser concluído

                    if audio_data:
                        # Usando o reconhecimento de fala
                        try:
                            text = recognizer.recognize_google(audio_data, language='pt-BR')
                            print(f"Texto detectado: {text}")

                            # Usando ThreadPoolExecutor para realizar a tradução em paralelo
                            future_translation = executor.submit(translate_text, text)
                            translated_text = future_translation.result()  # Bloqueia até a tradução ser concluída

                            print(f"Texto traduzido: {translated_text}")

                            # Convertendo o texto traduzido para fala
                            speak(translated_text)

                            # Pausar e esperar o usuário pressionar Enter para continuar
                            wait_for_user()

                        except sr.UnknownValueError:
                            print("Não consegui entender o áudio")
                        except sr.RequestError:
                            print("Não consegui conectar ao serviço de reconhecimento de fala")

            except Exception as e:
                print(f"Erro ao processar áudio: {e}", file=sys.stderr)

    except KeyboardInterrupt:
        print("Programa interrompido pelo usuário")

    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
