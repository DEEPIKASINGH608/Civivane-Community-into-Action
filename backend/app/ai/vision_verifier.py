import cv2
import numpy as np
from typing import Dict, Any

class VisionEvidenceVerifier:
    @staticmethod
    def compute_phash(image_bytes: bytes) -> str:
        """Compute a perceptual hash (pHash) of the image to detect duplicate fraud."""
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return ""

        # Resize to 32x32 and compute DCT
        img_resized = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)
        dct = cv2.dct(np.float32(img_resized))
        dct_low = dct[:8, :8]

        # Compute median and binary hash string
        median = np.median(dct_low)
        hash_bits = (dct_low > median).flatten()
        return "".join(['1' if b else '0' for b in hash_bits])

    @staticmethod
    def verify_image_quality(image_bytes: bytes) -> Dict[str, Any]:
        """Check image blurriness using Laplacian variance and compute pHash."""
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return {"is_valid": False, "reason": "Invalid image format or unreadable file."}

        # Blur detection via Laplacian variance
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        is_blurry = laplacian_var < 100.0  # Threshold for acceptable sharpness
        phash_val = VisionEvidenceVerifier.compute_phash(image_bytes)

        status = "VERIFIED" if not is_blurry else "NEEDS_REVIEW"
        reason = "Image quality approved." if not is_blurry else f"Image too blurry (Laplacian variance: {laplacian_var:.2f}). Escalated to human review."

        return {
            "is_valid": not is_blurry,
            "status": status,
            "sharpness_score": round(laplacian_var, 2),
            "phash": phash_val,
            "reason": reason
        }