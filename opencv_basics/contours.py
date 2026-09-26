import sys
from pathlib import Path

import cv2


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python contours.py <掩膜图片路径> <对应原图路径>")
        return 1

    mask_path = Path(sys.argv[1])
    original_path = Path(sys.argv[2])
    mask = cv2.imread(
        str(mask_path),
        cv2.IMREAD_GRAYSCALE,
    )

    if mask is None:
        print(f"无法读取掩膜图片: {mask_path}")
        return 1

    original = cv2.imread(str(original_path))

    if original is None:

        print(f"无法读取原图: {original_path}")
        return 1

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    result = original.copy()
    candidate_count = 0

    min_area = 10
    min_aspect_ratio = 1.0
    max_aspect_ratio = 15.0
    min_fill_ratio = 0.15
    max_area = 5000  
    for contour in contours:
        area = cv2.contourArea(contour)

        if area < min_area or area >max_area:
            continue

        rectangle = cv2.minAreaRect(contour)
        center, size, angle = rectangle
        width, height = size

        short_side = min(width, height)
        long_side = max(width, height)

        if short_side <= 0:
            continue

        aspect_ratio = long_side / short_side

        if (
            aspect_ratio < min_aspect_ratio
            or aspect_ratio > max_aspect_ratio
        ):
            continue

        rectangle_area = width * height

        if rectangle_area <= 0:
            continue

        fill_ratio = area / rectangle_area

        if fill_ratio < min_fill_ratio:
            continue

        box = cv2.boxPoints(rectangle).astype("int32")

        cv2.drawContours(
            result,
            [box],
            0,
            (0, 255, 0),
            3,
        )

        center_x = int(center[0])
        center_y = int(center[1])

        label = (
            f"id={candidate_count} "
        )

        cv2.putText(
            result,
            label,
            (center_x, center_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        print(
            f"候选 {candidate_count}: "
            f"中心=({center[0]:.1f}, {center[1]:.1f}), "
            f"面积={area:.1f}, "
            f"宽={width:.1f}, "
            f"高={height:.1f}, "
            f"角度={angle:.1f}, "
            f"长宽比={aspect_ratio:.2f}, "
            f"填充率={fill_ratio:.2f}"
        )

        candidate_count += 1

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "contours_result.jpg"
    saved = cv2.imwrite(str(output_path), result)

    if not saved:
        print(f"保存结果失败: {output_path}")
        return 1

    print(f"原始轮廓数量: {len(contours)}")
    print(f"筛选后候选数量: {candidate_count}")
    print(f"结果已保存: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
