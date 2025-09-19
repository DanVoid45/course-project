import tkinter as tk

def on_resize(event):
    """Функция, вызываемая при изменении размера окна."""
    new_width = event.width
    new_height = event.height
    print(f"Размер окна изменен: Ширина = {new_width}, Высота = {new_height}")
    # Здесь вы можете обновить элементы интерфейса или выполнить другие действия

# Создаем главное окно
root = tk.Tk()
root.title("Отслеживание размера окна")

# Привязываем функцию on_resize к событию <Configure>
root.bind('<Configure>', on_resize)

# Запускаем главный цикл обработки событий
root.mainloop()
