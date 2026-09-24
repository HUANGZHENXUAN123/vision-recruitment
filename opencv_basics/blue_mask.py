import sys
from pathlib import Path

import cv2


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python blue_mask.py <图片路径>")
        return 1

    image_path = Path(sys.argv[1])
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"无法读取图片: {image_path}")
        return 1

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_blue = (90, 80, 60)
    upper_blue = (135, 255, 255)

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_result = cv2.bitwise_and(image, image, mask=blue_mask)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    cv2.imwrite(str(output_dir / "blue_mask.jpg"), blue_mask)
    cv2.imwrite(str(output_dir / "blue_result.jpg"), blue_result)

    white_pixels = cv2.countNonZero(blue_mask)
    total_pixels = blue_mask.shape[0] * blue_mask.shape[1]
    percentage = white_pixels / total_pixels * 100

    print(f"HSV 下限: {lower_blue}")
    print(f"HSV 上限: {upper_blue}")
    print(f"可能的蓝色区域占比: {percentage:.2f}%")
    print("已生成:")
    print("  output/blue_mask.jpg")
    print("  output/blue_result.jpg")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
