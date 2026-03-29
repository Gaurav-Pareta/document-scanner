"""
Configuration constants for the Document Scanner and Enhancer.
"""

# Preprocessing
GAUSSIAN_BLUR_KERNEL = (5, 5)
GAUSSIAN_BLUR_SIGMA = 0
# Bilateral filter (edge-preserving); good for textured backgrounds
BILATERAL_D = 7
BILATERAL_SIGMA_COLOR = 75
BILATERAL_SIGMA_SPACE = 75

# Canny edge detection (used when not in auto mode)
CANNY_THRESHOLD_1 = 75
CANNY_THRESHOLD_2 = 200
# Median-based auto Canny: lower = max(0, median * LOW), upper = min(255, median * HIGH)
CANNY_AUTO_LOW_RATIO = 0.66
CANNY_AUTO_HIGH_RATIO = 1.33

# Morphology on edge maps: closes gaps so findContours sees closed quads
EDGE_CLOSE_KERNEL_SIZE = 5
EDGE_DILATE_ITERATIONS = 1

# Contour detection
CONTOUR_APPROX_EPSILON_FACTORS = (0.02, 0.035, 0.05, 0.065)
MIN_DOCUMENT_AREA_RATIO = 0.06  # lower helps cluttered desk photos
MAX_DOCUMENT_AREA_RATIO = 0.99  # ignore quads that cover almost the entire frame (no real crop)
# long_side / short_side of ordered quad; reject extreme slivers
MAX_QUAD_ASPECT_RATIO = 8.0

# Run detection on resized image for stability; points are mapped back to full resolution
DETECTION_MAX_SIDE = 900
DETECTION_SCALES = (1.0, 0.72)  # try full resize target, then slightly smaller

# Perspective transform
WARP_BORDER_MODE = 1  # cv2.BORDER_CONSTANT
WARP_BORDER_VALUE = (0, 0, 0)

# Enhancement
ADAPTIVE_THRESH_BLOCK_SIZE = 25  # must be odd and > 1 (code will enforce oddness)
ADAPTIVE_THRESH_C = 15
SHARPEN_KERNEL = [
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1],
]

# Display & I/O
WINDOW_NAME = "Document Scanner"
STACKED_WINDOW_NAME = "Original vs Scanned"
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_IMAGES_DIR = "images"
DEFAULT_OUTPUT_NAME = "scan.png"

# Webcam
DEFAULT_CAMERA_INDEX = 0
WEBCAM_FRAME_MAX_WIDTH = 900