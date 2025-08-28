import tkinter as tk
from MapHolder import MapHolder  
from SecondPage import ShowSecondPage, selected_mode

root = tk.Tk()
map_holder = MapHolder()  

# make the window fullscreen / maximized on startup (Windows: zoomed)
try:
    root.state("zoomed")
except Exception:
    try:
        root.attributes("-fullscreen", True)
    except Exception:
        pass

def ShowMainPage():
    """Return to the main page."""
    for widget in root.winfo_children():
        widget.destroy()
    MainPage()

def ShowFirstPage():
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    root.title("Path Planning")
    # window is already maximized; do not force a fixed geometry
    root.update_idletasks()
    title_label = tk.Label(root, text="Path Planning", bg="black", fg="white", font=("Bahnschrift", 36))
    title_label.pack(pady=50)
    start_button = tk.Button(
        root,
        text="Start",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 24),
        width=10,
        height=2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ShowSecondPage(back_callback=ShowFirstPage, continue_callback=MainPage)
    )
    start_button.pack(pady=30)
    credit_label = tk.Label(root, text="Created by Ahmed Yacine Ahriche", bg="black", fg="white", font=("Bahnschrift", 10))
    credit_label.pack(side="bottom", pady=5)
    close_button = tk.Button(
        root,
        text="Close",
        command=root.destroy,
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 12),
        width=10,
        height=2,
        borderwidth=0,
        highlightthickness=0
    )
    close_button.pack(side="bottom", pady=10)

def MainPage():
    """Show the mode selection label and 2D/3D buttons."""
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    root.title("Path Planning")
    # keep the maximized state — avoid resetting geometry
    root.update_idletasks()
    mode_label = tk.Label(root, text="Choose your MODE", bg="black", fg="white", font=("Bahnschrift", 36))
    mode_label.pack(pady=50)

    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(pady=20)

    from twoDNormal import ShowMap2D
    from ThreeD import ShowMap3D

    btn_2d = tk.Button(
        button_frame,
        text="2D",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 24),
        width=10,
        height=2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ShowMap2D(map_holder=map_holder, back_callback=MainPage)
    )
    btn_2d.pack(side=tk.LEFT, padx=20)

    btn_3d = tk.Button(
        button_frame,
        text="3D",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 24),
        width=10,
        height=2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ShowMap3D(back_callback=MainPage)
    )
    btn_3d.pack(side=tk.LEFT, padx=20)

    # Add Back button to return to the second page
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
        command=lambda: ShowSecondPage(back_callback=ShowFirstPage, continue_callback=MainPage)
    )
    back_btn.pack(side="bottom", pady=20)

if __name__ == "__main__":
    ShowFirstPage()
    root.mainloop()