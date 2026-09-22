import sys
from pathlib import Path

import cv2


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python basic_image.py <图片路径>")
        return 1

    image_path = Path(sys.argv[1])
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"无法读取图片: {image_path}")
        return 1

    blue, green, red = cv2.split(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    cv2.imwrite(str(output_dir / "original.jpg"), image)
    cv2.imwrite(str(output_dir / "blue_channel.jpg"), blue)
    cv2.imwrite(str(output_dir / "green_channel.jpg"), green)
    cv2.imwrite(str(output_dir / "red_channel.jpg"), red)
    cv2.imwrite(str(output_dir / "gray.jpg"), gray)
    cv2.imwrite(str(output_dir / "hsv.jpg"), hsv)

    print(f"图片尺寸: 宽={image.shape[1]}, 高={image.shape[0]}")
    print(f"通道数量: {image.shape[2]}")
    print(f"OpenCV 版本: {cv2.__version__}")
    print("已保存 6 个结果到 output/")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
