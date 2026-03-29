from __future__ import annotations
import os
from typing import Optional, Tuple
import cv2
import numpy as np
import config as cfg


def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def load_image(path: str) -> np.ndarray:
    if not path or not os.path.isfile(path):
        raise FileNotFoundError(f"Image not found: {path}")
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Failed to load image: {path}")
    return image


def save_image(path: str, image: np.ndarray) -> None:
    ensure_dir(os.path.dirname(path) or ".")
    ok = cv2.imwrite(path, image)
    if not ok:
        raise IOError(f"Failed to write image to: {path}")


def resize_to_max_width(image: np.ndarray, max_width: int) -> np.ndarray:
    h, w = image.shape[:2]
    if w <= max_width:
        return image
    scale = max_width / float(w)
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)


def stack_side_by_side(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """
    Stack two images horizontally with size alignment.
    Converts grayscale to BGR for consistent stacking.
    """
    def to_bgr(img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) if len(img.shape) == 2 else img

    l = to_bgr(left)
    r = to_bgr(right)
    h = max(l.shape[0], r.shape[0])
    def resize_h(img: np.ndarray, target_h: int) -> np.ndarray:
        scale = target_h / img.shape[0]
        new_w = int(img.shape[1] * scale)
        return cv2.resize(img, (new_w, target_h), interpolation=cv2.INTER_AREA)
    l = resize_h(l, h)
    r = resize_h(r, h)
    return np.hstack([l, r])


def draw_contour(image: np.ndarray, contour: Optional[np.ndarray]) -> np.ndarray:
    out = image.copy()
    if contour is not None and len(contour) > 0:
        cv2.drawContours(out, [contour], -1, (0, 255, 0), 2)
    return out