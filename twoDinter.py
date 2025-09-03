import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from ImageConverter2D import image_to_maze
from Path_Drawer import animate_path_on_image



def clean_up():
    for widget in tk._default_root.winfo_children():
        widget.destroy()

def ShowMap2D(map_holder=None, back_callback=None):
    clean_up()
    root = tk._default_root

    # create a horizontal container: left = map, right = controls
    main_frame = tk.Frame(root, bg="black")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Left: map area
    map_frame = tk.Frame(main_frame, bg="black")
    map_frame.pack(side=tk.LEFT, expand=True)

    label = tk.Label(map_frame, text="Interactive Map", bg="black", fg="white", font=("Bahnschrift", 24))
    label.pack(pady=(10, 5))

    img_label = tk.Label(map_frame, bg="black")
    img_label.pack(pady=(0, 10))

    # Find Path button (will be shown after upload)
    find_path_btn = tk.Button(
        map_frame,
        text="Find Path",
        bg="#224488",
        fg="white",
        font=("Bahnschrift", 14),
        width=12,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: run_algorithm() # replace with pathfinding call
    )

    # Frame for Start and End buttons (under the Find Path button)
    se_btn_frame = tk.Frame(map_frame, bg="black")

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

    # Right: algorithm controls (placed to the right of the map)
    right_frame = tk.Frame(main_frame, bg="black")
    right_frame.pack(side=tk.LEFT, anchor="n", padx=(20,0))

    # Algorithm label + option menu + selected label will be packed into right_frame
    # create placeholders (will be created in show_algo_and_sim)
    algo_menu = None
    selected_algo_label = None

    maze = None
    pil_img = None
    pil_img_orig = None  # <-- Add this line
    start_mode = tk.BooleanVar(value=False)
    end_mode = tk.BooleanVar(value=False)

    # Variables to track selection
    start_chosen = [False]
    end_chosen = [False]
    algo_var = tk.StringVar(value="")
    Algorithm_Selected = [None]   # <-- store selection here
    # sim_btn removed on purpose (UI uses Find Path button instead)
    algo_menu = None

    def run_algorithm():
        nonlocal maze
        alg = Algorithm_Selected[0]
        print(f"Algorithm selected (running): {alg}")
        if maze is None:
            print("No maze loaded.")
            return
        # find start/end
        start = end = None
        rows, cols = maze.shape
        for i in range(rows):
            for j in range(cols):
                if maze[i, j] == 'S':
                    start = (i, j)
                if maze[i, j] == 'E':
                    end = (i, j)
        if not start or not end:
            print("Start or End missing.")
            return
        if alg == "Dijkstra":
            from Dijkstra_2_D import dijkstra
            path = dijkstra(start, end, maze)
        elif alg == "A*":
            try:
                from Astar_2_D import astar
                path = astar(start, end, maze)
            except Exception:
                print("A* algorithm not implemented.")
                path = None
        else:
            print("Selected algorithm not supported.")
            path = None

        if path:
            from Path_Drawer import animate_path_on_image
            # use a thinner line and smaller node radius
            pil_img = animate_path_on_image(pil_img_orig, img_label, path, rows, cols, color=(0,200,0), line_width=1, node_radius=3, delay=30)
            # store pil_img back to outer scope if you rely on it later:
            # (add `nonlocal pil_img` at top of run_algorithm)
        else:
            print("No path found.")

    def show_algo_and_sim():
        nonlocal algo_menu
        if start_chosen[0] and end_chosen[0]:
            if not algo_menu:
                algo_label = tk.Label(
                    right_frame,
                    text="Choose Algorithm:",
                    bg="black",
                    fg="white",
                    font=("Bahnschrift", 16)
                )
                algo_label.pack(pady=(10, 5))
                algo_menu = tk.OptionMenu(right_frame, algo_var, "Dijkstra", "A*", "BFS")
                algo_menu.config(
                    font=("Bahnschrift", 14),
                    bg="#222222",
                    fg="white",
                    activebackground="#444444",
                    activeforeground="white",
                    width=12,
                    highlightthickness=0,
                    borderwidth=0
                )
                algo_menu["menu"].config(
                    font=("Bahnschrift", 12),
                    bg="#222222",
                    fg="white",
                    activebackground="#444444",
                    activeforeground="white"
                )
                algo_menu.pack(pady=(0, 10))
                # display label for selected algorithm
                selected_algo_label = tk.Label(right_frame, text="Selected Algorithm: ", bg="black", fg="#00ffcc", font=("Bahnschrift", 14))
                selected_algo_label.pack(pady=(0, 5))

            def on_algo_change(*args):
                Algorithm_Selected[0] = algo_var.get()
                print(f"Algorithm selected: {Algorithm_Selected[0]}")
                # Update GUI label only (no sim_btn to enable)
                if algo_var.get():
                    selected_algo_label.config(text=f"Selected Algorithm: {algo_var.get()}")
                else:
                    selected_algo_label.config(text="Selected Algorithm: ")

            # attach trace once
            algo_var.trace_add("write", on_algo_change)

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
            redraw_image_with_markers()
            draw = ImageDraw.Draw(pil_img)
            r_marker = 2
            x = int(col * w / cols)
            y = int(row * h / rows)
            draw.ellipse((x - r_marker, y - r_marker, x + r_marker, y + r_marker), fill="green")
            start_mode.set(False)
            print(f"Start point set at: ({row}, {col})")  # <-- Print start coordinates
            start_chosen[0] = True
        elif end_mode.get():
            # Remove old 'E'
            for r_idx in range(rows):
                for c_idx in range(cols):
                    if maze[r_idx, c_idx] == 'E':
                        maze[r_idx, c_idx] = 1  # or 0, depending on your maze logic

            maze[row, col] = 'E'
            redraw_image_with_markers()
            draw = ImageDraw.Draw(pil_img)
            r_marker = 2
            x = int(col * w / cols)
            y = int(row * h / rows)
            draw.ellipse((x - r_marker, y - r_marker, x + r_marker, y + r_marker), fill="red")
            end_mode.set(False)
            print(f"End point set at: ({row}, {col})")  # <-- Print end coordinates
            end_chosen[0] = True
        show_algo_and_sim()

        tk_img = ImageTk.PhotoImage(pil_img)
        img_label.config(image=tk_img)
        img_label.image = tk_img
        # print(maze)  # Optional: print the whole maze

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