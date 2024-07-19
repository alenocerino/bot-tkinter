from tkinter import *  
import openai
import os
from dotenv import load_dotenv, find_dotenv


# Configura tu clave de API de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define una función para obtener la completación del modelo GPT-3.5
def get_completion(prompt, model="gpt-3.5-turbo"):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.5
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Define una función para borrar el texto de marcador de posición cuando el usuario hace clic en el campo de entrada
def clear_placeholder(event):
    if usuario.get() == "Escribe aqui...":
        usuario.delete(0, END)

# Define una función que se ejecutará cuando se presione el botón de búsqueda
def click():
    prompt = '''
    Eres un asistente virtual que vas a responder las respuestas del usuario de manera corta y precisa.
    ''' + usuario.get()
    
    response = get_completion(prompt)
    
    respuesta.config(state=NORMAL)  # Habilita el widget de texto para edición
    respuesta.delete(1.0, END)      # Borra cualquier contenido anterior
    respuesta.insert(END, response + "\n\n¡Espero que te sirva de ayuda! Gracias por usar mi servicio.")  # Inserta la nueva respuesta
    respuesta.config(state=DISABLED)  # Configura el widget de texto para solo lectura

# Crea una ventana principal de Tkinter
root = Tk()
root.title("Chatbot")  # Añade un título a la ventana

# Crea un widget de etiqueta para mostrar un mensaje de bienvenida
texto = Label(root, text='TU CHAT-BOT', font=("Helvetica", 14, "bold"))
texto.grid(row=0, column=0, padx=10, pady=10)

# Crea un widget de entrada para que el usuario ingrese texto
usuario = Entry(root, width=60, font=("Helvetica", 12))
usuario.insert(0, 'Escribe aqui...') 
usuario.grid(row=1, column=0, padx=10, pady=10)
usuario.bind("<Button-1>", clear_placeholder)

# Crea un botón para iniciar la búsqueda
boton = Button(root, text='ENVIAR MENSAJE', bg="#90EE90", padx=50, pady=10, command=click)
boton.grid(row=2, column=0, padx=10, pady=10)

# Crea un widget de texto para mostrar la respuesta del modelo
respuesta = Text(root, height=20, width=60, font=("Helvetica", 12), wrap=WORD)
respuesta.grid(row=3, column=0, padx=10, pady=10)
respuesta.config(state=DISABLED)  # Configura el widget para solo lectura inicialmente

# Función que se ejecuta al iniciar la aplicación para mostrar el mensaje del prompt en el cuadro de respuesta
def iniciar_aplicacion():
    prompt_inicial = '''"¡Hola! Soy tu chatbot favorito, tu asistente digital. Estoy aquí para responder cualquier pregunta.
    '''
    
    respuesta_inicial = get_completion(prompt_inicial)
    
    respuesta.config(state=NORMAL)  # Habilita el widget de texto para edición
    respuesta.delete(1.0, END)      # Borra cualquier contenido anterior
    respuesta.insert(END, respuesta_inicial)  # Inserta la respuesta inicial
    respuesta.config(state=DISABLED)  # Configura el widget de texto para solo lectura

# Llamar a la función iniciar_aplicacion() al iniciar la aplicación
iniciar_aplicacion()

# Inicia el bucle principal de Tkinter 
root.mainloop()
