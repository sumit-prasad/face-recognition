import tkinter as tk
from user_registration import register_user_with_gui
from user_recognition import recognize_user
from database import reset_database

# Create a GUI for user interaction
root = tk.Tk()
root.title("Face Recognition System")

# Configure grid columns and rows
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create labels and buttons
welcome_label = tk.Label(root, text="Welcome to Face Recognition System", font=("Helvetica", 16), bg='lightblue', pady=10, padx=10)
welcome_label.grid(row=1, column=1, pady=20)

# Create buttons with the same size
button_size = (8, 3)  # Adjust the size as needed
register_button = tk.Button(root, text="Register a new user", command=register_user_with_gui, padx=10, pady=5)
register_button.grid(row=2, column=1, pady=10, sticky="nsew")
register_button.config(width=button_size[0], height=button_size[1])

recognize_button = tk.Button(root, text="Recognize users", command=recognize_user, padx=10, pady=5)
recognize_button.grid(row=3, column=1, pady=10, sticky="nsew")
recognize_button.config(width=button_size[0], height=button_size[1])

reset_button = tk.Button(root, text="Reset Database", command=reset_database, padx=10, pady=5)
reset_button.grid(row=4, column=1, pady=10, sticky="nsew")
reset_button.config(width=button_size[0], height=button_size[1])

exit_button = tk.Button(root, text="Exit", command=root.destroy, padx=10, pady=5)
exit_button.grid(row=5, column=1, pady=10, sticky="nsew")
exit_button.config(width=button_size[0], height=button_size[1])

# Start the GUI application
if __name__ == "__main__":
    root.mainloop()
