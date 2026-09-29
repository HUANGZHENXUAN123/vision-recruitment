import sys
from pathlib import Path

import cv2
import numpy as np
from pupil_apriltags import Detector


TARGET_ID = 0
TAG_SIZE_M = 0.163


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python estimate_pose.py <图片路径>")
        return 1

    image_path = Path(sys.argv[1])
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"无法读取图片: {image_path}")
        return 1

    params_path = Path("task2_apriltag/output/camera_params.npz")

    if not params_path.exists():
        print(f"找不到相机参数文件: {params_path}")
        return 1

    params = np.load(params_path)

    camera_matrix = params["camera_matrix"].astype(np.float64)
    distortion = params["distortion"].astype(np.float64)

    calibration_width = int(params["image_width"])
    calibration_height = int(params["image_height"])

    image_height, image_width = image.shape[:2]

    if image_width != calibration_width or image_height != calibration_height:
        print(
            f"图片尺寸 {image_width}x{image_height} "
            f"与标定尺寸 {calibration_width}x{calibration_height} 不一致"
        )
        return 1

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detector = Detector(
        families="tag36h11",
        nthreads=2,
        quad_decimate=1.0,
        quad_sigma=0.0,
        refine_edges=True,
        decode_sharpening=0.25,
        debug=False,
    )

    detections = detector.detect(
        gray,
        estimate_tag_pose=True,
        camera_params=(
            float(camera_matrix[0, 0]),
            float(camera_matrix[1, 1]),
            float(camera_matrix[0, 2]),
            float(camera_matrix[1, 2]),
        ),
        tag_size=TAG_SIZE_M,
    )

    result = image.copy()
    target_detection = None

    for detection in detections:
        corners = detection.corners.astype(np.int32)
        center = detection.center.astype(np.int32)

        color = (0, 255, 0) if detection.tag_id == TARGET_ID else (0, 0, 255)

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
            f"ID={detection.tag_id}",
            tuple(center + np.array([10, -10])),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2,
        )

        if detection.tag_id == TARGET_ID:
            target_detection = detection

    if target_detection is None:
        print(f"没有检测到目标 ID={TARGET_ID}")
        output_path = Path("task2_apriltag/output/pose_result.jpg")
        cv2.imwrite(str(output_path), result)
        print(f"结果已保存: {output_path}")
        return 1

    pose_t = np.asarray(target_detection.pose_t, dtype=np.float64).reshape(3)
    pose_R = np.asarray(target_detection.pose_R, dtype=np.float64).reshape(3, 3)

    rotation_vector, _ = cv2.Rodrigues(pose_R)

    x_m, y_m, z_m = pose_t
    distance_m = float(np.linalg.norm(pose_t))

    cv2.drawFrameAxes(
        result,
        camera_matrix,
        distortion,
        rotation_vector,
        pose_t,
        TAG_SIZE_M * 0.5,
        3,
    )

    info_lines = [
        f"x={x_m:.3f} m y={y_m:.3f} m z={z_m:.3f} m",
        f"distance={distance_m:.3f} m",
        f"rvec=({rotation_vector[0, 0]:.3f}, "
        f"{rotation_vector[1, 0]:.3f}, "
        f"{rotation_vector[2, 0]:.3f})",
    ]

    for index, line in enumerate(info_lines):
        cv2.putText(
            result,
            line,
            (30, 40 + index * 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2,
        )

    output_path = Path("task2_apriltag/output/pose_result.jpg")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), result)

    print(f"ID: {TARGET_ID}")
    print(f"平移向量 t (m): {pose_t}")
    print(f"旋转矩阵 R:\n{pose_R}")
    print(f"旋转向量 rvec (rad): {rotation_vector.ravel()}")
    print(f"直线距离 (m): {distance_m:.6f}")
    print(f"结果已保存: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
