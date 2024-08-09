import pyaudio
import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import time
import sys
from concurrent.futures import ThreadPoolExecutor

def wait_for_user():
    input("Pressione Enter para continuar com outra tradução...")

def main():
    recognizer = sr.Recognizer()
    translator = Translator()
    engine = pyttsx3.init()

    def speak(text):
        engine.say(text)
        engine.runAndWait()
        
    def translate_text(text):
        return translator.translate(text, src='pt', dest='en').text

    def recognize_speech(source):
        try:
            print("\nFale agora. Estou lhe escutando. Você tem quinze segundos para falar.")
            audio_data = recognizer.listen(source, timeout=15)
            print("Voz escutada.")
            return audio_data
        except sr.WaitTimeoutError:
            print("Tempo de escuta expirado. Nenhuma voz detectada.")
            return None
        except Exception as e:
            print(f"Erro ao reconhecer fala: {e}", file=sys.stderr)
            return None

    mic = sr.Microphone()
	
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

    except Exception as e:
        print(f"Erro ao inicializar o microfone: {e}", file=sys.stderr)
        return

    executor = ThreadPoolExecutor(max_workers=4)

    try:
        while True:
            try:
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)
                    future_audio = executor.submit(recognize_speech, source)
                    audio_data = future_audio.result()

                    if audio_data:
                        try:
                            text = recognizer.recognize_google(audio_data, language='pt-BR')
                            print(f"Texto detectado: {text}")
                            future_translation = executor.submit(translate_text, text)
                            translated_text = future_translation.result()
                            print(f"Texto traduzido: {translated_text}")
                            speak(translated_text)
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
