import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from ImageConverter2D import image_to_maze

def clean_up():
    for widget in tk._default_root.winfo_children():
        widget.destroy()

def ShowMap2D(map_holder=None, back_callback=None):
    clean_up()
    root = tk._default_root

    label = tk.Label(root, text="Map", bg="black", fg="white", font=("Bahnschrift", 24))
    label.pack(pady=(30, 10))  # Move map up a bit

    img_label = tk.Label(root, bg="black")
    img_label.pack(pady=(0, 10))  # Less bottom padding to move up

    # Find Path button (not packed yet)
    find_path_btn = tk.Button(
        root,
        text="Find Path",
        bg="#224488",
        fg="white",
        font=("Bahnschrift", 14),
        width=12,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Find Path clicked!")  # Replace with your pathfinding logic
    )

    # Frame for Start and End buttons
    se_btn_frame = tk.Frame(root, bg="black")

    start_btn = tk.Button(
        se_btn_frame,
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
        se_btn_frame,
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

    maze = None
    pil_img = None
    pil_img_orig = None  # <-- Add this line
    start_mode = tk.BooleanVar(value=False)
    end_mode = tk.BooleanVar(value=False)

    def upload_action():
        nonlocal maze, pil_img, pil_img_orig  # <-- Add pil_img_orig here
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
            pil_img_orig = pil_img.copy()  # Keep a clean copy for redrawing
            tk_img = ImageTk.PhotoImage(pil_img)
            img_label.config(image=tk_img)
            img_label.image = tk_img

            try:
                maze = image_to_maze(file_path)
                maze = maze.astype(object)
                # Show Find Path button and Start/End buttons after upload
                find_path_btn.pack(pady=(0, 10))
                se_btn_frame.pack(pady=(0, 20))
                start_btn.pack(side=tk.LEFT, padx=10)
                end_btn.pack(side=tk.LEFT, padx=10)
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

        # Remove previous S/E from maze
        if start_mode.get():
            # Remove old 'S'
            for r_idx in range(rows):
                for c_idx in range(cols):
                    if maze[r_idx, c_idx] == 'S':
                        maze[r_idx, c_idx] = 1  # or 0, depending on your maze logic

            maze[row, col] = 'S'
            # Redraw the image to clear old markers
            redraw_image_with_markers()
            # Draw new S
            draw = ImageDraw.Draw(pil_img)
            r_marker = 2
            x = int(col * w / cols)
            y = int(row * h / rows)
            draw.ellipse((x - r_marker, y - r_marker, x + r_marker, y + r_marker), fill="green")
            start_mode.set(False)

        elif end_mode.get():
            # Remove old 'E'
            for r_idx in range(rows):
                for c_idx in range(cols):
                    if maze[r_idx, c_idx] == 'E':
                        maze[r_idx, c_idx] = 1  # or 0, depending on your maze logic

            maze[row, col] = 'E'
            # Redraw the image to clear old markers
            redraw_image_with_markers()
            # Draw new E
            draw = ImageDraw.Draw(pil_img)
            r_marker = 2
            x = int(col * w / cols)
            y = int(row * h / rows)
            draw.ellipse((x - r_marker, y - r_marker, x + r_marker, y + r_marker), fill="red")
            end_mode.set(False)

        tk_img = ImageTk.PhotoImage(pil_img)
        img_label.config(image=tk_img)
        img_label.image = tk_img
        print(maze)

    def redraw_image_with_markers():
        nonlocal pil_img, pil_img_orig, maze  # <-- Add pil_img_orig here
        pil_img.paste(pil_img_orig)
        rows, cols = maze.shape
        w, h = img_label.winfo_width(), img_label.winfo_height()
        draw = ImageDraw.Draw(pil_img)
        r_marker = 2
        for r_idx in range(rows):
            for c_idx in range(cols):
                if maze[r_idx, c_idx] == 'S':
                    x = int(c_idx * w / cols)
                    y = int(r_idx * h / rows)
                    draw.ellipse((x - r_marker, y - r_marker, x + r_marker, y + r_marker), fill="green")
                elif maze[r_idx, c_idx] == 'E':
                    x = int(c_idx * w / cols)
                    y = int(r_idx * h / rows)
                    draw.ellipse((x - r_marker, y - r_marker, x + r_marker, y + r_marker), fill="red")

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