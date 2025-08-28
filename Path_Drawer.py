from PIL import ImageDraw, ImageTk

def draw_path_on_image(pil_img_orig, img_label, path, rows, cols,
                       color=(0,120,255), line_width=1, node_radius=1):
    """
    Draw full path onto a copy of pil_img_orig and update img_label.
    - color default is blue, line_width and node_radius default to 1 (very thin)
    - Returns the new PIL image with path drawn.
    """
    if pil_img_orig is None or img_label is None or not path:
        return pil_img_orig

    img = pil_img_orig.copy().convert("RGB")
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # compute pixel centers for each grid cell in path
    points = []
    for r, c in path:
        x = int((c + 0.5) * w / cols)
        y = int((r + 0.5) * h / rows)
        points.append((x, y))

    # ensure minimum 1 pixel stroke
    draw_width = max(1, int(round(line_width)))

    if len(points) >= 2:
        draw.line(points, fill=color, width=draw_width)

    # tiny nodes matching stroke width (optional)
    if node_radius > 0:
        for x, y in points:
            r = max(1, int(node_radius))
            draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

    tk_img = ImageTk.PhotoImage(img)
    img_label.config(image=tk_img)
    img_label.image = tk_img

    return None

def animate_path_on_image(pil_img_orig, img_label, path, rows, cols,
                          color=(0,120,255), line_width=1, node_radius=1,
                          delay=10, on_complete=None):
    """
    Animate drawing the path incrementally on img_label.
    - delay: milliseconds between frames (smaller = faster)
    - on_complete: optional callable() invoked when animation finishes
    Note: function uses img_label.after for scheduling and does not block.
    """
    if pil_img_orig is None or img_label is None or not path:
        if on_complete:
            on_complete()
        return

    w, h = pil_img_orig.size
    points = []
    for r, c in path:
        x = int((c + 0.5) * w / cols)
        y = int((r + 0.5) * h / rows)
        points.append((x, y))

    draw_width = max(1, int(line_width))

    def step(i):
        # redraw background and draw up to i points/segments
        img = pil_img_orig.copy().convert("RGB")
        draw = ImageDraw.Draw(img)
        if i >= 2:
            draw.line(points[:i], fill=color, width=draw_width)
        for px, py in points[:i]:
            if node_radius > 0:
                r = node_radius
                draw.ellipse((px - r, py - r, px + r, py + r), fill=color)
        tk_img = ImageTk.PhotoImage(img)
        img_label.config(image=tk_img)
        img_label.image = tk_img
        if i < len(points):
            img_label.after(delay, lambda: step(i + 1))
        else:
            if on_complete:
                on_complete()

    # start animation with the first point
    step(3)
    return None