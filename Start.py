import tkinter as tk

root = tk.Tk()  # Make sure you have a root window

button_frame = tk.Frame(root)
button_frame.pack(pady=30)

start_button_2d = tk.Button(button_frame, text="2D", bg="gray", fg="white", font=("Bahnschrift", 24), width=10, height=2)
start_button_2d.pack(side=tk.LEFT, padx=10)

start_button_3d = tk.Button(button_frame, text="3D", bg="gray", fg="white", font=("Bahnschrift", 24), width=10, height=2)
start_button_3d.pack(side=tk.LEFT, padx=10)

root.mainloop()