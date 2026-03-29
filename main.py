import argparse
import os
from datetime import datetime
import cv2
import numpy as np
import config as cfg
from scanner import DocumentScanner
import utils as U


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Document Scanner and Enhancer")
    src = parser.add_mutually_exclusive_group(required=False)
    src.add_argument("-i", "--image", type=str, help="Path to input image")
    src.add_argument("-w", "--webcam", action="store_true", help="Use webcam input")
    parser.add_argument(
        "-m", "--mode", type=str, default="adaptive",
        choices=["adaptive", "grayscale", "sharpen"],
        help="Enhancement mode (default: adaptive)",
    )
    parser.add_argument(
        "-o", "--output", type=str,
        default=os.path.join(cfg.DEFAULT_OUTPUT_DIR, cfg.DEFAULT_OUTPUT_NAME),
        help="Output image path",
    )
    parser.add_argument("--visualize", action="store_true", help="Show comparison window")
    parser.add_argument("--camera", type=int, default=cfg.DEFAULT_CAMERA_INDEX, help="Webcam index (default: 0)")
    return parser.parse_args()


def process_single_image(image_path: str, mode: str, output_path: str, visualize: bool) -> int:
    try:
        image = U.load_image(image_path)
    except Exception as e:
        print(f"[Error] {e}")
        return 1

    scanner = DocumentScanner()
    try:
        enhanced, contour = scanner.scan(image, enhancement_mode=mode)
    except Exception as e:
        print(f"[Error] {e}")
        return 2



    try:
        U.save_image(output_path, enhanced)
        print(f"[OK] Saved scan to: {output_path}")
    except Exception as e:
        print(f"[Error] {e}")
        return 3


    if visualize:
        preview = U.draw_contour(image, contour)
        stacked = U.stack_side_by_side(preview, enhanced)
        stacked = U.resize_to_max_width(stacked, 1200)
        cv2.imshow(cfg.STACKED_WINDOW_NAME, stacked)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return 0



def process_webcam(mode: str, output_dir: str, camera_index: int) -> int:
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("[Error] Unable to access webcam.")
        return 1


    print("Webcam mode: press 's' to scan/save, 'q' to quit.")
    scanner = DocumentScanner()
    U.ensure_dir(output_dir)


    while True:
        ok, frame = cap.read()
        if not ok:
            print("[Error] Failed to read frame from webcam.")
            break


        frame_disp = U.resize_to_max_width(frame, cfg.WEBCAM_FRAME_MAX_WIDTH)
        preview = frame_disp.copy()


        # Preview uses same multi-strategy detector as scan 
        
        try:
            contour_pts = scanner.detect_document_quad(frame_disp)
            if contour_pts is not None:
                preview = U.draw_contour(preview, contour_pts.reshape(-1, 1, 2).astype(np.int32))
        except Exception:
            pass

        cv2.imshow(cfg.WINDOW_NAME, preview)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            try:
                enhanced, contour = scanner.scan(frame, enhancement_mode=mode)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scan_{timestamp}.png"
                save_path = os.path.join(output_dir, filename)
                U.save_image(save_path, enhanced)
                print(f"[OK] Saved scan to: {save_path}")

                
                
                preview_full = U.draw_contour(frame, contour)
                stacked = U.stack_side_by_side(preview_full, enhanced)
                stacked = U.resize_to_max_width(stacked, 1200)
                cv2.imshow(cfg.STACKED_WINDOW_NAME, stacked)
                cv2.waitKey(0)  # Wait for user to see the result
                cv2.destroyWindow(cfg.STACKED_WINDOW_NAME)
            except Exception as e:
                print(f"[Error] {e}")

    cap.release()
    cv2.destroyAllWindows()
    return 0



def main() -> int:
    args = parse_args()
    if not args.image and not args.webcam:
        print("No input specified. Use --image PATH or --webcam. For help: python main.py -h")
        return 1

    if args.image:
        return process_single_image(args.image, args.mode, args.output, args.visualize)
    else:
        out_dir = os.path.dirname(args.output) or "."
        return process_webcam(args.mode, out_dir, args.camera)



if __name__ == "__main__":
    raise SystemExit(main())