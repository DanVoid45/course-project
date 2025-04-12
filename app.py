from customtkinter import *
from PIL import Image
import functions

set_appearance_mode('dark')
set_default_color_theme('dark-blue')

def click_handler(request):
    cmd_result = functions.recognize_cmd(request)['cmd']
    message = CTkLabel(master = root, text = functions.execute_cmd(cmd_result), 
                       text_color="#FFFFFF",  fg_color="#2B2B2B",  font=("Arial", 14))
    
    message.place(relx = 0.4, rely = 0.7, anchor = 'center')

    return functions.speak(functions.execute_cmd(cmd_result))


    

root = CTk()
root.title('Айрис')
root.geometry('800x600')

entry = CTkEntry(master = root, placeholder_text= "Введите запрос", width = 300)
entry.place(relx = 0.5, rely = 0.8, anchor = 'center')

image = CTkImage(light_image=Image.open('plane.png'), size=(20, 20))
btn = CTkButton(master = root, image = image, width = 20, corner_radius = 32, text='', fg_color = '#CD0074', command = lambda: click_handler(entry.get()))
btn.place(relx = 0.75, rely = 0.8, anchor = 'center')



root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)
root.resizable(width=False, height=False)
root.mainloop()