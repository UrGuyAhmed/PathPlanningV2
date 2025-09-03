import tkinter as tk
from MapHolder import MapHolder
import SecondPage  # import module so we can read SecondPage.selected_mode at runtime

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
        # open the main mode selection page first (don't show SecondPage here)
        command=lambda: MainPage()
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
    root.update_idletasks()
    mode_label = tk.Label(root, text="Choose your MODE", bg="black", fg="white", font=("Bahnschrift", 36))
    mode_label.pack(pady=50)

    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(pady=20)

    # lazy import: 3D viewer
    from ThreeD import ShowMap3D

    # callback that will be invoked after user chooses Normal/Interactive in SecondPage
    def launch_2d_from_mode():
        # read the current selection from the SecondPage module
        mode = getattr(SecondPage, "selected_mode", None)

        try:
            if mode == 'N':
                from twoDNormal import ShowMap2D as _ShowMap2D
            else:
                from twoDinter import ShowMap2D as _ShowMap2D
        except Exception as e:
            print("Error importing 2D module for mode=", mode, ":", e)
            return

        _ShowMap2D(map_holder=map_holder, back_callback=MainPage)

    # When user clicks 2D: first show the SecondPage to choose N/I, then continue to launch the correct 2D view
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
        command=lambda: SecondPage.ShowSecondPage(back_callback=MainPage, continue_callback=launch_2d_from_mode)
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
        # return to the first page
        command=lambda: ShowFirstPage()
    )
    back_btn.pack(side="bottom", pady=20)

if __name__ == "__main__":
    ShowFirstPage()
    root.mainloop()