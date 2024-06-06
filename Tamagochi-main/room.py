import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import time

class MascotaVirtual:
    def __init__(self, master):
        self.master = master
        self.master.title("Mascota Virtual")
        self.master.geometry("800x600")  # Definir la resolución de la ventana

        # Cargar la imagen de la habitación
        self.room_image = Image.open("room.png")
        self.room_photo = ImageTk.PhotoImage(self.room_image)
        self.room_label = tk.Label(master, image=self.room_photo)
        self.room_label.pack()

        # Barra de alimentación
        self.alimentacion = 100  # Puntos de alimentación iniciales
        self.alimentacion_label = tk.Label(master, text="Alimentación: {}".format(self.alimentacion))
        self.alimentacion_label.pack()

        # Botón para alimentar
        self.feed_button = tk.Button(master, text="Alimentar", command=self.alimentar)
        self.feed_button.pack()

        # Botón para bañar
        self.bathe_button = tk.Button(master, text="Bañar", command=self.baño)
        self.bathe_button.pack()

        # Iniciar el contador para la disminución de la alimentación
        self.master.after(5000, self.disminuir_alimentacion)

    def alimentar(self):
        self.alimentacion += 10
        if self.alimentacion > 100:
            self.alimentacion = 100
        self.actualizar_barra_alimentacion()

    def baño(self):
        messagebox.showinfo("Baño", "¡Tu mascota está limpia y feliz!")
        self.alimentacion -= 20
        self.actualizar_barra_alimentacion()

    def disminuir_alimentacion(self):
        self.alimentacion -= 1
        self.actualizar_barra_alimentacion()
        if self.alimentacion <= 0:
            messagebox.showinfo("¡Tu mascota se murió!")
            self.master.destroy()
            return
        self.master.after(5000, self.disminuir_alimentacion)

    def actualizar_barra_alimentacion(self):
        self.alimentacion_label.config(text="Alimentación: {}".format(self.alimentacion))


def main():
    root = tk.Tk()
    app = MascotaVirtual(root)
    root.mainloop()

if __name__ == "__main__":
    main()
