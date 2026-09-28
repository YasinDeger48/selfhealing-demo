"""Crops the video frames and the report screenshot to the parts the slides show (readable at 1080 px).

    python crops.py      -> ../images/crops/*.png      (needs Pillow: pip install pillow)
"""
import os

from PIL import Image

IMAGES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")

# source picture -> (crop box left, top, right, bottom, target)
CROPS = [
    ("step2-healed-login.png", (420, 300, 1270, 790), "cover.png"),        # healed username field + panel
    ("step1-candidates-scored.png", (420, 180, 1270, 790), "candidates.png"),
    ("step2-healed-login.png", (420, 180, 1270, 790), "healed-login.png"),
    ("step3-healed-search.png", (80, 95, 1270, 790), "healed-search.png"),
    ("report-expanded-top.png", (240, 40, 2560, 1800), "report.png"),       # 2x screenshot of the report
]


def main():
    os.makedirs(os.path.join(IMAGES, "crops"), exist_ok=True)
    for src, box, dst in CROPS:
        Image.open(os.path.join(IMAGES, src)).crop(box).save(os.path.join(IMAGES, "crops", dst))
        print("crop", dst)


if __name__ == "__main__":
    main()
