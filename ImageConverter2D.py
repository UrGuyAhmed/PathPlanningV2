import cv2
import numpy as np

def image_to_maze(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not load image at {path}")
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    maze = np.where(binary == 255, 1, 0)
    return maze