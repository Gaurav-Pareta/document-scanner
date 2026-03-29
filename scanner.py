from __future__ import annotations

from typing import Generator, List, Optional, Tuple

import cv2
import numpy as np

import config as cfg


class DocumentScanner:
    """
    Document detection, perspective transform, and enhancement.
    Uses multiple edge maps, morphology, convex hull / min-area-rectangle fallbacks,
    and optional multi-scale detection for robustness.
    """

    def __init__(self) -> None:
        pass

    def preprocess(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Convert to grayscale and blur; return (gray, blurred)."""
        if image is None or image.size == 0:
            raise ValueError("Invalid image provided to preprocess()")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, cfg.GAUSSIAN_BLUR_KERNEL, cfg.GAUSSIAN_BLUR_SIGMA)
        return gray, blurred

    def detect_edges(self, blurred: np.ndarray) -> np.ndarray:
        """Compute Canny edges from a blurred grayscale image (fixed thresholds)."""
        return cv2.Canny(blurred, cfg.CANNY_THRESHOLD_1, cfg.CANNY_THRESHOLD_2)

    def _safe_find_contours(self, image: np.ndarray, mode: int, method: int) -> List[np.ndarray]:
        result = cv2.findContours(image, mode, method)
        if len(result) == 3:
            return result[1]
        return result[0]

    def _postprocess_edges(self, edges: np.ndarray) -> np.ndarray:
        k = max(3, int(cfg.EDGE_CLOSE_KERNEL_SIZE))
        if k % 2 == 0:
            k += 1
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        it = int(cfg.EDGE_DILATE_ITERATIONS)
        if it > 0:
            closed = cv2.dilate(closed, kernel, iterations=it)
        return closed

    def _canny_auto(self, blurred: np.ndarray) -> Tuple[int, int]:
        med = float(np.median(blurred))
        lo = int(max(0.0, med * cfg.CANNY_AUTO_LOW_RATIO))
        hi = int(min(255.0, med * cfg.CANNY_AUTO_HIGH_RATIO))
        if hi <= lo:
            hi = min(255, lo + 1)
        return lo, hi

    def _iter_edge_maps(self, gray: np.ndarray) -> Generator[np.ndarray, None, None]:
        blurred = cv2.GaussianBlur(gray, cfg.GAUSSIAN_BLUR_KERNEL, cfg.GAUSSIAN_BLUR_SIGMA)
        lo, hi = self._canny_auto(blurred)

        yield self._postprocess_edges(
            cv2.Canny(blurred, cfg.CANNY_THRESHOLD_1, cfg.CANNY_THRESHOLD_2)
        )
        yield self._postprocess_edges(cv2.Canny(blurred, lo, hi))

        bil = cv2.bilateralFilter(
            gray,
            cfg.BILATERAL_D,
            cfg.BILATERAL_SIGMA_COLOR,
            cfg.BILATERAL_SIGMA_SPACE,
        )
        yield self._postprocess_edges(cv2.Canny(bil, lo, hi))

        adaptive = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )
        yield self._postprocess_edges(cv2.Canny(adaptive, 50, 150))

    def _resize_for_detection(self, image: np.ndarray, scale: float) -> Tuple[np.ndarray, float, float]:
        h, w = image.shape[:2]
        ms = cfg.DETECTION_MAX_SIDE
        if ms <= 0 or scale <= 0:
            return image.copy(), 1.0, 1.0
        target = max(320, int(ms * scale))
        long = max(h, w)
        if long <= target:
            return image.copy(), 1.0, 1.0
        s = target / float(long)
        nw, nh = int(round(w * s)), int(round(h * s))
        small = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_AREA)
        sx = w / float(nw)
        sy = h / float(nh)
        return small, sx, sy

    def _scale_quad_to_full(self, pts: np.ndarray, sx: float, sy: float) -> np.ndarray:
        out = pts.astype(np.float32).copy()
        out[:, 0] *= sx
        out[:, 1] *= sy
        return out

    def _quad_area_ratio(self, pts: np.ndarray, image_area: float) -> float:
        c = pts.reshape(-1, 1, 2).astype(np.float32)
        return abs(cv2.contourArea(c)) / max(image_area, 1.0)

    def _quad_passes_geometry(self, pts: np.ndarray, image_area: float, min_dim_px: float) -> bool:
        if pts.shape != (4, 2):
            return False
        t = self._quad_area_ratio(pts, image_area)
        if t < cfg.MIN_DOCUMENT_AREA_RATIO or t > cfg.MAX_DOCUMENT_AREA_RATIO:
            return False
        rect = self.order_points(pts.astype(np.float32))
        tl, tr, br, bl = rect
        w = float(max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl)))
        h = float(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))
        if min(w, h) < min_dim_px:
            return False
        ar = max(w, h) / max(min(w, h), 1e-6)
        if ar > cfg.MAX_QUAD_ASPECT_RATIO:
            return False
        return True

    def _quad_from_contour(
        self, contour: np.ndarray, image_area: float, min_dim_px: float
    ) -> Optional[np.ndarray]:
        peri = cv2.arcLength(contour, True)
        if peri < 1e-6:
            return None

        for eps in cfg.CONTOUR_APPROX_EPSILON_FACTORS:
            approx = cv2.approxPolyDP(contour, float(eps) * peri, True)
            if len(approx) == 4:
                p = approx.reshape(4, 2).astype(np.float32)
                if self._quad_passes_geometry(p, image_area, min_dim_px):
                    return p

        if len(contour) >= 4:
            hull = cv2.convexHull(contour)
            if hull is not None and len(hull) >= 4:
                hperi = cv2.arcLength(hull, True)
                for eps in cfg.CONTOUR_APPROX_EPSILON_FACTORS:
                    approx = cv2.approxPolyDP(hull, float(eps) * hperi, True)
                    if len(approx) == 4:
                        p = approx.reshape(4, 2).astype(np.float32)
                        if self._quad_passes_geometry(p, image_area, min_dim_px):
                            return p

        rect = cv2.minAreaRect(contour)
        (rw, rh) = rect[1]
        if rw < 1 or rh < 1:
            return None
        side_long = max(rw, rh)
        side_short = min(rw, rh)
        ar = side_long / max(side_short, 1e-6)
        if ar > cfg.MAX_QUAD_ASPECT_RATIO:
            return None

        box = cv2.boxPoints(rect).astype(np.float32)
        if self._quad_passes_geometry(box, image_area, min_dim_px):
            return box
        return None

    def _quad_score(self, pts: np.ndarray, image_area: float) -> float:
        return self._quad_area_ratio(pts, image_area)

    def _detect_quad_once(self, image: np.ndarray, edges: np.ndarray) -> Optional[np.ndarray]:
        h, w = image.shape[:2]
        image_area = float(h * w)
        min_area = cfg.MIN_DOCUMENT_AREA_RATIO * image_area
        min_dim_px = max(8.0, 0.01 * min(h, w))

        best: Optional[np.ndarray] = None
        best_score = -1.0

        for retr in (cv2.RETR_LIST, cv2.RETR_EXTERNAL):
            contours = self._safe_find_contours(edges.copy(), retr, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                continue
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for contour in contours[:35]:
                a = cv2.contourArea(contour)
                if a < min_area:
                    break
                quad = self._quad_from_contour(contour, image_area, min_dim_px)
                if quad is None:
                    continue
                score = self._quad_score(quad, image_area)
                if score > best_score:
                    best_score = score
                    best = quad

        return best

    def detect_document_quad(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Full multi-strategy detection. Returns 4x2 float32 corners in image coordinates, or None.
        """
        if image is None or image.size == 0:
            return None
        h, w = image.shape[:2]
        for scale in cfg.DETECTION_SCALES:
            small, sx, sy = self._resize_for_detection(image, float(scale))
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            for edges in self._iter_edge_maps(gray):
                quad = self._detect_quad_once(small, edges)
                if quad is not None:
                    return self._scale_quad_to_full(quad, sx, sy)
        return None

    def find_document_contour(self, image: np.ndarray, edges: np.ndarray) -> Optional[np.ndarray]:
        """
        Find a document quadrilateral using a single precomputed edge map (post-processed).
        """
        if image.shape[:2] != edges.shape[:2]:
            raise ValueError("image and edges must have the same height and width")
        pp = self._postprocess_edges(edges)
        return self._detect_quad_once(image, pp)

    def order_points(self, pts: np.ndarray) -> np.ndarray:
        if pts.shape != (4, 2):
            raise ValueError("order_points expects (4,2) array")
        rect = np.zeros((4, 2), dtype=np.float32)
        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def four_point_transform(self, image: np.ndarray, pts: np.ndarray) -> np.ndarray:
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect

        width_a = np.linalg.norm(br - bl)
        width_b = np.linalg.norm(tr - tl)
        max_w = int(max(width_a, width_b))

        height_a = np.linalg.norm(tr - br)
        height_b = np.linalg.norm(tl - bl)
        max_h = int(max(height_a, height_b))

        max_w = max(max_w, 1)
        max_h = max(max_h, 1)

        dst = np.array(
            [[0, 0], [max_w, 0], [max_w, max_h], [0, max_h]],
            dtype=np.float32,
        )

        m = cv2.getPerspectiveTransform(rect, dst)
        return cv2.warpPerspective(
            image,
            m,
            (max_w, max_h),
            flags=cv2.INTER_LINEAR,
            borderMode=cfg.WARP_BORDER_MODE,
            borderValue=cfg.WARP_BORDER_VALUE,
        )

    def enhance(self, image: np.ndarray, mode: str) -> np.ndarray:
        mode = (mode or "adaptive").lower()
        if mode == "adaptive":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            block_size = cfg.ADAPTIVE_THRESH_BLOCK_SIZE
            if block_size % 2 == 0:
                block_size += 1
            return cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                block_size,
                cfg.ADAPTIVE_THRESH_C,
            )
        if mode == "grayscale":
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if mode == "sharpen":
            kernel = np.array(cfg.SHARPEN_KERNEL, dtype=np.float32)
            return cv2.filter2D(image, -1, kernel)
        raise ValueError(f"Unknown enhancement mode: {mode}")

    def scan(self, image: np.ndarray, enhancement_mode: str = "adaptive") -> Tuple[np.ndarray, Optional[np.ndarray]]:
        contour_pts = self.detect_document_quad(image)
        if contour_pts is None:
            raise ValueError(
                "No document detected. Try a clearer photo, better lighting, or ensure the document edges are visible."
            )
        warped = self.four_point_transform(image, contour_pts)
        if warped.size == 0:
            raise ValueError("Perspective transform produced an empty image.")
        enhanced = self.enhance(warped, enhancement_mode)
        return enhanced, contour_pts.reshape(-1, 1, 2).astype(np.int32)
