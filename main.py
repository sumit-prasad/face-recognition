import tkinter as tk
from user_registration import register_user_with_gui
from user_recognition import recognize_user
from database import create_database, reset_database

# Create a GUI for user interaction
root = tk.Tk()
root.title("Face Recognition System")

# Configure grid columns and rows
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create a frame for better organization
main_frame = tk.Frame(root, bg='lightblue')
main_frame.grid(row=1, column=1, padx=5, pady=5)

# Create a title label
welcome_label = tk.Label(main_frame, text="Welcome to Face Recognition System", font=("Helvetica", 16), bg='lightblue', padx=10, pady=20)
welcome_label.pack()

# Create a button style with increased spacing and rounded corners
button_style = {"font": ("Helvetica", 12), "padx": 10, "pady": 5, "borderwidth": 2, "relief": "ridge"}

# Create buttons with increased spacing, rounded corners, and icons
buttons_frame = tk.Frame(main_frame, bg='lightblue')
buttons_frame.pack(pady=20)

# Load icons
register_icon = tk.PhotoImage(file="assets/register.png")
recognize_icon = tk.PhotoImage(file="assets/recognize.png")
reset_icon = tk.PhotoImage(file="assets/reset.png")
exit_icon = tk.PhotoImage(file="assets/exit.png")

register_button = tk.Button(buttons_frame, text="Register a new user", image=register_icon, compound="left", command=register_user_with_gui, **button_style)
register_button.image = register_icon  # To prevent garbage collection of the image
register_button.pack(side='left', padx=10)

recognize_button = tk.Button(buttons_frame, text="Recognize users", image=recognize_icon, compound="left", command=recognize_user, **button_style)
recognize_button.image = recognize_icon
recognize_button.pack(side='left', padx=10)

reset_button = tk.Button(buttons_frame, text="Reset Database", image=reset_icon, compound="left", command=reset_database, **button_style)
reset_button.image = reset_icon
reset_button.pack(side='left', padx=10)

exit_button = tk.Button(buttons_frame, text="Exit", image=exit_icon, compound="left", command=root.destroy, **button_style)
exit_button.image = exit_icon
exit_button.pack(side='left', padx=10)

# Start the GUI application
if __name__ == "__main__":
    create_database()
    root.mainloop()
