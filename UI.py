import tkinter as tk
from Start import add_start_buttons
from MapHolder import MapHolder  


root = tk.Tk()
map_holder = MapHolder()  
def ShowMainPage():
    """Return to the main page."""
    for widget in root.winfo_children():
        widget.destroy()
    MainPage()

def MainPage():
    """Initialize the main page UI."""
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    root.title("Path Planning")
    root.geometry("800x800")
    title_label = tk.Label(root, text="Path Planning", bg="black", fg="white", font=("Bahnschrift", 36))
    title_label.pack(pady=50)
    description_label = tk.Label(root, text="Visualize path planning algorithms on a map.", bg="black", fg="white", font=("Bahnschrift", 16))
    description_label.pack(pady=20)
    # Import ShowMap2D and ShowMap3D here to avoid circular import
    from twoD import ShowMap2D
    from ThreeD import ShowMap3D
    add_start_buttons(
        root,
        on_2d=lambda: ShowMap2D(map_holder=map_holder, back_callback=ShowMainPage),  
        on_3d=lambda: ShowMap3D(back_callback=ShowMainPage)
    )
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

    # Example usage: load a map when needed
    # map_holder.load_map("path/to/map.png")

if __name__ == "__main__":
    MainPage()
    root.mainloop()