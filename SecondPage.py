import tkinter as tk

selected_mode = None  # Global variable to store the mode

def ShowSecondPage(back_callback=None, continue_callback=None):
    global selected_mode
    root = tk._default_root
    for widget in root.winfo_children():
        widget.destroy()
    label = tk.Label(root, text="This is the Second Page", bg="black", fg="white", font=("Bahnschrift", 24))
    label.pack(pady=50)

    def set_interactive():
        global selected_mode
        selected_mode = 'I'
        if continue_callback:
            continue_callback()

    def set_normal():
        global selected_mode
        selected_mode = 'N'
        if continue_callback:
            continue_callback()

    interactive_btn = tk.Button(
        root,
        text="Interactive",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 14),
        width=10,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=set_interactive
    )
    interactive_btn.pack(pady=10)

    normal_btn = tk.Button(
        root,
        text="Normal",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 14),
        width=10,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=set_normal
    )
    normal_btn.pack(pady=10)

    print(selected_mode)  # Will be 'I' or 'N' after user selection