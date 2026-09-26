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

    lower_blue = (80, 120, 110)
    upper_blue = (135, 255, 255)

    hsv_mask = cv2.inRange(
        hsv,
        lower_blue,
        upper_blue,
    )

    blue_channel, green_channel, red_channel = cv2.split(image)

    blue_difference = cv2.subtract(
        blue_channel,
        red_channel,
    )

    difference_mask = cv2.threshold(
        blue_difference,
        40,
        255,
        cv2.THRESH_BINARY,
    )[1]

    blue_mask = cv2.bitwise_and(
        hsv_mask,
        difference_mask,
    )

    blue_result = cv2.bitwise_and(
        image,
        image,
        mask=blue_mask,
    )

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    cv2.imwrite(
        str(output_dir / "hsv_mask.jpg"),
        hsv_mask,
    )

    cv2.imwrite(
        str(output_dir / "difference_mask.jpg"),
        difference_mask,
    )

    cv2.imwrite(
        str(output_dir / "blue_mask.jpg"),
        blue_mask,
    )

    cv2.imwrite(
        str(output_dir / "blue_result.jpg"),
        blue_result,
    )

    white_pixels = cv2.countNonZero(blue_mask)
    total_pixels = blue_mask.shape[0] * blue_mask.shape[1]
    percentage = white_pixels / total_pixels * 100

    print(f"HSV 下限: {lower_blue}")
    print(f"HSV 上限: {upper_blue}")
    print("B-R 差分阈值: 40")
    print(f"可能的蓝色区域占比: {percentage:.2f}%")
    print("已生成:")
    print("  output/hsv_mask.jpg")
    print("  output/difference_mask.jpg")
    print("  output/blue_mask.jpg")
    print("  output/blue_result.jpg")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
