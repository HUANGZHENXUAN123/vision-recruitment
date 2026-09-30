import sys
from pathlib import Path

import cv2


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "用法: python polygon_approximation.py "
            "<原图路径> <掩膜路径>"
        )
        return 1

    image_path = Path(sys.argv[1])
    mask_path = Path(sys.argv[2])

    image = cv2.imread(str(image_path))
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"无法读取原图: {image_path}")
        return 1

    if mask is None:
        print(f"无法读取掩膜: {mask_path}")
        return 1

    if image.shape[:2] != mask.shape[:2]:
        print("原图和掩膜尺寸不一致")
        return 1

    contour_result = image.copy()
    polygon_result = image.copy()
    combined_result = image.copy()

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    valid_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 100 or area > 100000:
            continue

        perimeter = cv2.arcLength(contour, True)

        polygon = cv2.approxPolyDP(
            contour,
            0.02 * perimeter,
            True,
        )

        rectangle = cv2.minAreaRect(contour)
        width, height = rectangle[1]

        short_side = min(width, height)
        long_side = max(width, height)

        if short_side <= 0:
            continue

        aspect_ratio = long_side / short_side

        if aspect_ratio < 1.5 or aspect_ratio > 20:
            continue

        box = cv2.boxPoints(rectangle).astype("int32")

        cv2.drawContours(
            contour_result,
            [contour],
            -1,
            (255, 0, 0),
            2,
        )

        cv2.drawContours(
            polygon_result,
            [polygon],
            -1,
            (0, 0, 255),
            3,
        )

        cv2.drawContours(
            combined_result,
            [contour],
            -1,
            (255, 0, 0),
            2,
        )

        cv2.drawContours(
            combined_result,
            [polygon],
            -1,
            (0, 0, 255),
            3,
        )

        cv2.drawContours(
            combined_result,
            [box],
            -1,
            (0, 255, 0),
            2,
        )

        valid_count += 1

    output_dir = Path("task1_lightbar/representative_frames")
    output_dir.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(
        str(output_dir / "raw_contours.jpg"),
        contour_result,
    )
    cv2.imwrite(
        str(output_dir / "polygon_approximation.jpg"),
        polygon_result,
    )
    cv2.imwrite(
        str(output_dir / "contour_polygon_rectangle.jpg"),
        combined_result,
    )

    print(f"原始轮廓数量: {len(contours)}")
    print(f"通过筛选的候选数量: {valid_count}")
    print("蓝色线: 原始轮廓")
    print("红色线: approxPolyDP 多边形近似")
    print("绿色线: minAreaRect 旋转矩形")
    print(f"结果目录: {output_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

