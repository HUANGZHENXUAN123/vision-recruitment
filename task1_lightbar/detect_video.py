import sys
import time
from pathlib import Path

import cv2


def detect_lightbars(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 初始蓝色范围，后续需要根据考核视频调参
    lower_blue = (80, 120, 110)
    upper_blue = (135, 255, 255)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3),
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel,
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    detections = []

    for contour in contours:
        area = cv2.contourArea(contour)

        # 过滤过小噪声和过大区域
        if area < 50 or area > 100000:
            continue

        rectangle = cv2.minAreaRect(contour)
        center, size, angle = rectangle
        width, height = size

        short_side = min(width, height)
        long_side = max(width, height)

        if short_side <= 0:
            continue

        aspect_ratio = long_side / short_side

        # 灯条通常是细长区域
        if aspect_ratio < 1.5 or aspect_ratio > 20:
            continue

        box = cv2.boxPoints(rectangle).astype("int32")

        detections.append(
            {
                "box": box,
                "center": center,
                "area": area,
                "ratio": aspect_ratio,
            }
        )

    return detections


def main():
    if len(sys.argv) != 3:
        print("用法: python detect_video.py <输入视频> <输出视频>")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"输入视频不存在: {input_path}")
        return 1

    capture = cv2.VideoCapture(str(input_path))

    if not capture.isOpened():
        print(f"无法打开输入视频: {input_path}")
        return 1

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30.0

    output_path.parent.mkdir(parents=True, exist_ok=True)

    codec = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        str(output_path),
        codec,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        print(f"无法创建输出视频: {output_path}")
        capture.release()
        return 1

    frame_number = 0

    try:
        while True:
            start_time = time.perf_counter()

            success, frame = capture.read()

            if not success:
                break

            detections = detect_lightbars(frame)

            for detection in detections:
                box = detection["box"]
                center = detection["center"]
                area = detection["area"]
                ratio = detection["ratio"]

                cv2.drawContours(
                    frame,
                    [box],
                    0,
                    (0, 255, 0),
                    3,
                )

                cv2.putText(
                    frame,
                    f"area={area:.0f} ratio={ratio:.1f}",
                    (int(center[0]), int(center[1])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            cv2.putText(
                frame,
                f"frame={frame_number}",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"lightbars={len(detections)}",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"time={elapsed_ms:.2f} ms",
                (30, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                2,
            )

            writer.write(frame)
            frame_number += 1

    finally:
        capture.release()
        writer.release()

    print(f"处理完成，总帧数: {frame_number}")
    print(f"结果视频: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
