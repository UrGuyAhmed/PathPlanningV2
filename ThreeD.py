import tkinter as tk
def clean_up():
    """Clear the main window."""
    for widget in tk._default_root.winfo_children():
        widget.destroy()

def ShowMap3D(back_callback=None):
    clean_up()
    root = tk._default_root

    label = tk.Label(root, text="3D Map", bg="black", fg="white", font=("Bahnschrift", 24))
    label.pack(pady=50)
    text = tk.Text(root, bg="black", fg="white", font=("Bahnschrift", 14), width=50, height=20)
    text.pack(pady=60)
    # Back button uses the callback
    back_btn = tk.Button(
        root,
        text="Back",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 14),
        width=10,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=back_callback if back_callback else root.destroy
    )
    back_btn.place(relx=0.0, rely=1.0, anchor="sw", x=30, y=-30)