from customtkinter import *
from PIL import Image
import functions
# сделать массивы, чтобы отделить сообщения пользователя от сообщений помощника
set_appearance_mode('dark')
set_default_color_theme('dark-blue')

messages_user = []
messages_assistant = []

def click_handler_voice():
    functions.listen(messages_user)

def click_handler_text(request):
    entry.delete(0, END)

    # --- Сообщение пользователя ---
    user_frame = CTkFrame(master=root, fg_color="#2B2B2B", corner_radius=10)
    user_label = CTkLabel(master=user_frame, text=request,
                          text_color="#FFFFFF", font=("Arial", 14), wraplength=300)
    user_label.pack(padx=10, pady=5)
    user_frame.place(relx=0.3, rely=0.7 - len(messages_user + messages_assistant)*0.08, anchor='center')
    messages_user.append(user_frame)

    # --- Ответ помощника ---
    cmd_result = functions.recognize_cmd(request)['cmd']
    response_text = functions.execute_cmd(cmd_result)

    assistant_frame = CTkFrame(master=root, fg_color="#2B2B2B", corner_radius=10)
    assistant_label = CTkLabel(master=assistant_frame, text=response_text,
                               text_color="#FFFFFF", font=("Arial", 14), wraplength=300)
    assistant_label.pack(padx=10, pady=5)
    assistant_frame.place(relx=0.75, rely=0.7 - len(messages_user + messages_assistant)*0.08, anchor='center')
    messages_assistant.append(assistant_frame)

    # --- Ограничение количества сообщений ---
    max_messages = 5
    while len(messages_user) > max_messages:
        old = messages_user.pop(0)
        old.destroy()

    while len(messages_assistant) > max_messages:
        old = messages_assistant.pop(0)
        old.destroy()

    total_pairs = len(messages_user)
    for i in range(total_pairs):
        y_base = 0.65 - (total_pairs - 1 - i) * 0.15
        messages_user[i].place(relx=0.75, rely=y_base, anchor='center')
        messages_assistant[i].place(relx=0.3, rely=y_base + 0.08, anchor='center')

    return functions.speak(response_text)



    

root = CTk()
root.title('Айрис')
root.geometry('800x600')

entry = CTkEntry(master = root, placeholder_text= "Введите запрос", width = 500)
entry.place(relx = 0.5, rely = 0.8, anchor = 'center')

image_plane = CTkImage(light_image=Image.open('pictures/plane.png'), size=(20, 20))
btn_text = CTkButton(master = root, image = image_plane, width = 20, corner_radius = 32, text='', fg_color = '#CD0074', command = lambda: click_handler_text(entry.get()))
btn_text.place(relx = 0.9, rely = 0.8, anchor = 'center')
btn_text.bind('<Enter>', lambda e: btn_text.configure(fg_color='#CD0074'))
root.bind('<Return>', lambda event: btn_text.invoke())

#Кнопка для прослушивания
image_microfone = CTkImage(light_image=Image.open('pictures/microfone.png'), size=(20, 20))
btn_voice = CTkButton(master = root, image = image_microfone, width = 20, corner_radius = 32, text='', fg_color = '#CD0074', command = click_handler_voice)
btn_voice.place(relx=0.1, rely=0.8, anchor='center')


root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)
root.resizable(width=False, height=False)
root.mainloop()