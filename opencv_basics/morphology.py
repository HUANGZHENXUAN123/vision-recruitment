import sys
from pathlib import Path

import cv2


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python morphology.py <掩膜图片路径>")
        return 1

    mask_path = Path(sys.argv[1])
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

    if mask is None:
        print(f"无法读取掩膜图片: {mask_path}")
        return 1

    kernel_1x1 = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (1, 1),
    )

    kernel_3x3 = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3),
    )

    kernel_7x7 = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (7, 7),
    )

    opened_1x1 = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel_1x1,
    )

    closed_1x1 = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel_1x1,
    )

    opened_3x3 = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel_3x3,
    )

    closed_3x3 = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel_3x3,
    )

    opened_7x7 = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel_7x7,
    )

    closed_7x7 = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel_7x7,
    )

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    cv2.imwrite(str(output_dir / "mask_original.jpg"), mask)
    cv2.imwrite(str(output_dir / "mask_open_1x1.jpg"), opened_1x1)
    cv2.imwrite(str(output_dir / "mask_close_1x1.jpg"), closed_1x1)
    cv2.imwrite(str(output_dir / "mask_open_3x3.jpg"), opened_3x3)
    cv2.imwrite(str(output_dir / "mask_close_3x3.jpg"), closed_3x3)
    cv2.imwrite(str(output_dir / "mask_open_7x7.jpg"), opened_7x7)
    cv2.imwrite(str(output_dir / "mask_close_7x7.jpg"), closed_7x7)

    print("形态学处理完成，结果保存在 output/：")
    print("  mask_original.jpg")
    print("  mask_open_1x1.jpg")
    print("  mask_close_1x1.jpg")
    print("  mask_open_3x3.jpg")
    print("  mask_close_3x3.jpg")
    print("  mask_open_7x7.jpg")
    print("  mask_close_7x7.jpg")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
