from customtkinter import *
from PIL import Image
import functions

set_appearance_mode('dark')
set_default_color_theme('dark-blue')

messages = []

def click_handler(request):
    entry.delete(0, END)

    #Запрос пользователя
    message_frame_user = CTkFrame(master=root, fg_color="#2B2B2B", corner_radius=10)
    message_user = CTkLabel(master=message_frame_user, text = request, 
                       text_color="#FFFFFF", font=("Arial", 14), wraplength=100)
    message_user.pack(padx = 30, pady = 5)
    messages.insert(0, message_frame_user)

    #Распознование команды
    cmd_result = functions.recognize_cmd(request)['cmd']
    response_text = functions.execute_cmd(cmd_result)
    print(response_text)
    #Вывод помощника
    message_frame = CTkFrame(master=root, fg_color="#2B2B2B", corner_radius=10)
    message = CTkLabel(master=message_frame, text=response_text, 
                       text_color="#FFFFFF", font=("Arial", 14), wraplength=300)
    message.pack(padx = 10, pady = 5)
    messages.insert(0, message_frame)
    
    # Ограничиваем максимальное количество видимых сообщений (например, 5)
    if len(messages) > 5:
        old_frame = messages.pop(0)  # Удаляем самое старое сообщение
        old_frame.destroy()
    
    # Размещаем все сообщения, начиная с текущей позиции
    for i, frame in enumerate(messages):
        if i % 2 == 0:
            frame.place(relx=0.3, rely= 0.7 - 2 * i * 0.08, anchor='center')
        else:
            frame.place(relx=0.75, rely= 0.7 - 2 * i * 0.08, anchor='center')
    
    return functions.speak(response_text)


    

root = CTk()
root.title('Айрис')
root.geometry('800x600')

entry = CTkEntry(master = root, placeholder_text= "Введите запрос", width = 500)
entry.place(relx = 0.5, rely = 0.8, anchor = 'center')

image = CTkImage(light_image=Image.open('plane.png'), size=(20, 20))
btn = CTkButton(master = root, image = image, width = 20, corner_radius = 32, text='', fg_color = '#CD0074', command = lambda: click_handler(entry.get()))
btn.place(relx = 0.9, rely = 0.8, anchor = 'center')
btn.bind('<Enter>', lambda e: btn.configure(fg_color='#CD0074'))
root.bind('<Return>', lambda event: btn.invoke())



root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)
root.resizable(width=False, height=False)
root.mainloop()