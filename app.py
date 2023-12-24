import customtkinter
import tkinter
from jarvis import Jarvis

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Javis Assistant")
label.pack(pady=12, padx=10)

label = customtkinter.CTkLabel(master=root,
                               text="",
                               width=120,
                               height=25,
                               corner_radius=8)
label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

assistant = Jarvis(root, label)
assistant.speak('Hello, I am Jarvis. Please tell me how may I help you.')

if __name__ == "__main__":
    while True:
        root.update()
        assistant.takeCommand()