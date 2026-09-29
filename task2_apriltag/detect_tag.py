import sys
from pathlib import Path

import cv2
from pupil_apriltags import Detector


TARGET_ID = 0


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python detect_tag.py <图片路径>")
        return 1

    image_path = Path(sys.argv[1])
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"无法读取图片: {image_path}")
        return 1

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detector = Detector(
        families="tag36h11",
        nthreads=2,
        quad_decimate=1.0,
        quad_sigma=0.8,
        refine_edges=True,
        decode_sharpening=0.25,
        debug=False,
    )

    detections = detector.detect(
        gray,
        estimate_tag_pose=False,
        camera_params=None,
        tag_size=None,
    )

    result = image.copy()
    target_found = False

    for detection in detections:
        corners = detection.corners.astype("int32")
        center = detection.center.astype("int32")
        tag_id = detection.tag_id

        color = (0, 255, 0) if tag_id == TARGET_ID else (0, 0, 255)

        cv2.polylines(
            result,
            [corners.reshape((-1, 1, 2))],
            True,
            color,
            3,
        )

        cv2.circle(
            result,
            tuple(center),
            6,
            color,
            -1,
        )

        cv2.putText(
            result,
            f"ID={tag_id}",
            tuple(center + [10, -10]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2,
        )

        print(
            f"检测到 ID={tag_id}, "
            f"中心=({detection.center[0]:.1f}, "
            f"{detection.center[1]:.1f})"
        )

        if tag_id == TARGET_ID:
            target_found = True

    if not detections:
        print("没有检测到 AprilTag")
    elif not target_found:
        print(f"检测到了 Tag，但没有找到目标 ID={TARGET_ID}")

    output_dir = Path("task2_apriltag/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "tag_detection.jpg"
    cv2.imwrite(str(output_path), result)

    print(f"结果已保存: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
