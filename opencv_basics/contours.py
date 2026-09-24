import sys
from pathlib import Path

import cv2


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python contours.py <掩膜图片路径>")
        return 1

    mask_path = Path(sys.argv[1])
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

    if mask is None:
        print(f"无法读取掩膜图片: {mask_path}")
        return 1

    original = cv2.imread("test.jpg")

    if original is None:
        print("无法读取原图: test.jpg")
        return 1

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    result = original.copy()
    candidate_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 100:
            continue

        rectangle = cv2.minAreaRect(contour)
        center, size, angle = rectangle
        width, height = size

        short_side = min(width, height)
        long_side = max(width, height)

        if short_side <= 0:
            continue

        aspect_ratio = long_side / short_side

        if aspect_ratio < 1.5 or aspect_ratio > 20:
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

        cv2.putText(
            result,
            f"id={candidate_count} area={area:.0f} ratio={aspect_ratio:.1f}",
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
            f"宽={width:.1f}, 高={height:.1f}, "
            f"角度={angle:.1f}, "
            f"长宽比={aspect_ratio:.2f}"
        )

        candidate_count += 1

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "contours_result.jpg"
    cv2.imwrite(str(output_path), result)

    print(f"原始轮廓数量: {len(contours)}")
    print(f"筛选后候选数量: {candidate_count}")
    print(f"结果已保存: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
