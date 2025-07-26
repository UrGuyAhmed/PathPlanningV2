import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from ImageConverter2D import image_to_maze

def clean_up():
    """Clear the main window."""
    for widget in tk._default_root.winfo_children():
        widget.destroy()

def ShowMap2D(map_holder=None, back_callback=None):
    clean_up()
    root = tk._default_root

    label = tk.Label(root, text="Map", bg="black", fg="white", font=("Bahnschrift", 24))
    label.pack(pady=50)

    img_label = tk.Label(root, bg="black")
    img_label.pack(pady=20)

    maze = None
    pil_img = None  # Store the PIL image for drawing
    start_mode = tk.BooleanVar(value=False)
    end_mode = tk.BooleanVar(value=False)

    # Create Start and End buttons but do not pack them yet
    start_btn = tk.Button(
        root,
        text="Start",
        bg="#228822",
        fg="white",
        font=("Bahnschrift", 14),
        width=10,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: start_mode.set(True)
    )
    end_btn = tk.Button(
        root,
        text="End",
        bg="#882222",
        fg="white",
        font=("Bahnschrift", 14),
        width=10,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: end_mode.set(True)
    )

    def upload_action():
        nonlocal maze, pil_img
        file_path = filedialog.askopenfilename(
            title="Select your map",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            if map_holder:
                map_holder.load_map(file_path)
            pil_img = Image.open(file_path).convert("RGB")
            display_width, display_height = 500, 500
            pil_img = pil_img.resize((display_width, display_height), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(pil_img)
            img_label.config(image=tk_img)
            img_label.image = tk_img

            # Convert the image to a maze/grid using your function
            try:
                maze = image_to_maze(file_path)
                maze = maze.astype(object)
                # Show Start and End buttons after successful upload
                start_btn.place(relx=0.7, rely=1.0, anchor="se", x=-30, y=-30)
                end_btn.place(relx=0.55, rely=1.0, anchor="se", x=-30, y=-30)
            except Exception as e:
                print("Error converting image:", e)

    def on_image_click(event):
        nonlocal maze, pil_img
        if maze is None or pil_img is None:
            return
        w, h = img_label.winfo_width(), img_label.winfo_height()
        rows, cols = maze.shape
        col = int(event.x / w * cols)
        row = int(event.y / h * rows)
        draw = ImageDraw.Draw(pil_img)
        r = 2  # radius of marker

        if start_mode.get():
            maze[row, col] = 'S'
            # Draw a green circle for Start
            x = int(col * w / cols)
            y = int(row * h / rows)
            draw.ellipse((x - r, y - r, x + r, y + r), fill="green")
            start_mode.set(False)
        elif end_mode.get():
            maze[row, col] = 'E'
            # Draw a red circle for End
            x = int(col * w / cols)
            y = int(row * h / rows)
            draw.ellipse((x - r, y - r, x + r, y + r), fill="red")
            end_mode.set(False)

        # Update the displayed image
        tk_img = ImageTk.PhotoImage(pil_img)
        img_label.config(image=tk_img)
        img_label.image = tk_img
        print(maze)

    img_label.bind("<Button-1>", on_image_click)

    upload_map = tk.Button(
        root,
        text="Upload Map",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 14),
        width=10,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=upload_action
    )
    upload_map.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-30)

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