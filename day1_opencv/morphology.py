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

    kernel_small = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3),
    )

    kernel_large = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (7, 7),
    )

    opened_small = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel_small,
    )

    closed_small = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel_small,
    )

    opened_large = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel_large,
    )

    closed_large = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel_large,
    )

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    cv2.imwrite(str(output_dir / "mask_original.jpg"), mask)
    cv2.imwrite(str(output_dir / "mask_open_3x3.jpg"), opened_small)
    cv2.imwrite(str(output_dir / "mask_close_3x3.jpg"), closed_small)
    cv2.imwrite(str(output_dir / "mask_open_7x7.jpg"), opened_large)
    cv2.imwrite(str(output_dir / "mask_close_7x7.jpg"), closed_large)

    print("形态学处理完成，结果保存在 output/：")
    print("  mask_original.jpg")
    print("  mask_open_3x3.jpg")
    print("  mask_close_3x3.jpg")
    print("  mask_open_7x7.jpg")
    print("  mask_close_7x7.jpg")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
