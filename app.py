import queue
import tkinter as tk
from customtkinter import *
from PIL import Image

import functions  

voice_queue = queue.Queue()

set_appearance_mode('dark')
set_default_color_theme('dark-blue')

voice_running = False
listener = None
current_text = ""
messages_history_user, messages_history_assist = [], []

def callback_ui_threadsafe(text, is_voice=False):
    voice_queue.put((text, is_voice))

def process_queue():
    try:
        while True:
            global current_text
            text, is_voice = voice_queue.get_nowait()
            current_text = text
            click_handler_text(text, is_voice)
    except queue.Empty:
        pass
    root.after(100, process_queue)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=10, fill='', outline=''):

    points = [
        (x1+radius, y1), (x2-radius, y1),  # Верхняя линия
        (x2, y1+radius), (x2, y2-radius),  # Правая линия
        (x2-radius, y2), (x1+radius, y2),  # Нижняя линия
        (x1, y2-radius), (x1, y1+radius)   # Левая линия
    ]

    # Верхняя линия
    canvas.create_line(points[0], points[1], fill=outline)
    # Правая линия
    canvas.create_line(points[2], points[3], fill=outline)
    # Нижняя линия
    canvas.create_line(points[4], points[5], fill=outline)
    # Левая линия
    canvas.create_line(points[6], points[7], fill=outline)

    # Четыре дуги
    canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, fill=fill, outline=outline, style='pieslice')
    canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, fill=fill, outline=outline, style='pieslice')
    canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, fill=fill, outline=outline, style='pieslice')
    canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, fill=fill, outline=outline, style='pieslice')

    # В центре прямоугольник без углов (заливка)
    canvas.create_rectangle(x1+radius, y1, x2-radius, y2, fill=fill, outline='')
    canvas.create_rectangle(x1, y1+radius, x2, y2-radius, fill=fill, outline='')


def click_handler_voice_start():
    global listener
    listener = functions.listen(callback_ui=callback_ui_threadsafe)

def click_handler_voice_stop():
    global listener
    if listener:
        try:
            listener.stop()
        except Exception:
            pass
        listener = None

def toggle_voice():
    global voice_running
    if not voice_running:
        click_handler_voice_start()
        voice_running = True
        btn_voice.configure(fg_color="#21D6C4")
    else:
        click_handler_voice_stop()
        voice_running = False
        btn_voice.configure(fg_color="#CD0074")

#определяем высоту текста
def calculate_text_height(canvas, text, font, width):
    temp_id = canvas.create_text(0, 0, text=text, font=font, anchor='nw', width=width)
    canvas.update_idletasks()
    bbox = canvas.bbox(temp_id)
    canvas.delete(temp_id)
    if bbox:
        return bbox[3] - bbox[1]
    return 40  # fallback по умолчанию


message_y = 10  # глобальная переменная, высота для следующего сообщения

bottom_y = 500  # изначально нижняя граница сообщений (высота)

#Функция вызывается при изменении размера окна
def on_windows_resize(event):
        global current_text
        new_width = root.winfo_width() * 1.1875
        messages_canvas.delete("all")
        click_handler_text(current_text, is_voice=False, canvas_width = new_width)



def click_handler_text(request, is_voice=False, canvas_width = 950):
    global bottom_y
    if not request or request.strip() == "" or request in ["Голос не распознан!", "Ошибка соединения!"]:
        return
    if not is_voice:
        entry.delete(0, END)

    padding = 10
    msg_width = 280

    user_bg = "#2B3A42"        # Темный серо-синий
    assistant_bg = "#3A4B53"   # Серо-синий немного светлее
    text_color = "#FFFFFF"

    font = ("Arial", 14)

    messages_history_user.append(request)
    # --- Пользователь ---
    user_text_height = calculate_text_height(messages_canvas, request, font, msg_width - 20)
    x1 = canvas_width - msg_width - padding
    y1 = bottom_y
    x2 = canvas_width - padding
    y2 = y1 + user_text_height + 20

    create_rounded_rectangle(messages_canvas, x1, y1, x2, y2, radius=15, fill=user_bg, outline="")
    messages_canvas.create_text(x2 - 10, y1 + 10, text=request, fill=text_color,
                                font=font, anchor='ne', width=msg_width - 20)

    bottom_y += user_text_height + 20 + padding

    # --- Ассистент ---
    response_text = functions.callback_for_text_input(request, callback_ui=click_handler_text)

    messages_history_assist.append(response_text)
    assistant_text_height = calculate_text_height(messages_canvas, response_text, font, msg_width - 20)
    x1 = padding
    y1 = bottom_y
    x2 = padding + msg_width
    y2 = y1 + assistant_text_height + 20

    create_rounded_rectangle(messages_canvas, x1, y1, x2, y2, radius=15, fill=assistant_bg, outline="")
    messages_canvas.create_text(x1 + 10, y1 + 10, text=response_text, fill=text_color,
                                font=font, anchor='nw', width=msg_width - 20)

    bottom_y += assistant_text_height + 20 + padding
    messages_canvas.configure(scrollregion=(0, 0, canvas_width, bottom_y))
    messages_canvas.yview_moveto(1.0)

    return messages_canvas.after(100, lambda: functions.speak(response_text))


if __name__ == "__main__":
    root = CTk()
    root.title("Айрис")
    root.geometry("800x600")

    # Контейнер для сообщений
    messages_container = CTkFrame(root, fg_color="#1C1C1C")
    messages_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Canvas и Scrollbar
    messages_canvas = tk.Canvas(messages_container, bg="#1C1C1C", highlightthickness=0)
    scrollbar = CTkScrollbar(messages_container, orientation="vertical", command=messages_canvas.yview)
    messages_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    messages_canvas.pack(side="left", fill="both", expand=True)

    # Нижняя панель
    bottom_panel = CTkFrame(root, height=60)
    bottom_panel.pack(fill="x", padx=10, pady=10)

    image_plane = CTkImage(light_image=Image.open('pictures/plane.png'), size=(20, 20))
    image_microfone = CTkImage(light_image=Image.open('pictures/microfone.png'), size=(20, 20))


    # Элементы управления через pack
    btn_voice = CTkButton(
        bottom_panel, 
        image=image_microfone, 
        width=20, 
        corner_radius=32, 
        text='',
        fg_color='#CD0074', 
        command=toggle_voice
    )
    btn_voice.pack(side="left", padx=5)

    entry = CTkEntry(bottom_panel, placeholder_text="Введите запрос...")
    entry.pack(side="left", fill="x", expand=True, padx=5)

    btn_text = CTkButton(
        bottom_panel, 
        image=image_plane, 
        width=20, 
        corner_radius=32, 
        text='', 
        fg_color='#CD0074',
        command=lambda: click_handler_text(entry.get())
    )
    btn_text.pack(side="right", padx=5)
    


    #root.resizable(False, False)
    root.bind('<Return>', lambda e: btn_text.invoke())
    root.after(100, process_queue)
    root.bind('<Configure>', on_windows_resize) # следим за конфигурацией размеров окна

    root.mainloop()