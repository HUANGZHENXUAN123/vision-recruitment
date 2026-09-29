from pathlib import Path

import cv2
import numpy as np


PATTERN_SIZE = (9, 6)
SQUARE_SIZE_MM = 22.0
IMAGE_DIR = Path("task2_apriltag/calibration_images")
OUTPUT_PATH = Path("task2_apriltag/output/camera_params.npz")


def main() -> int:
    image_paths = sorted(
        path
        for path in IMAGE_DIR.iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}
    )

    if not image_paths:
        print(f"没有找到标定图片: {IMAGE_DIR}")
        return 1

    object_points = []
    image_points = []
    image_size = None

    object_template = np.zeros(
        (PATTERN_SIZE[0] * PATTERN_SIZE[1], 3),
        dtype=np.float32,
    )

    object_template[:, :2] = np.mgrid[
        0:PATTERN_SIZE[0],
        0:PATTERN_SIZE[1],
    ].T.reshape(-1, 2)

    object_template *= SQUARE_SIZE_MM

    for image_path in image_paths:
        image = cv2.imread(str(image_path))

        if image is None:
            print(f"跳过无法读取的文件: {image_path}")
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        current_size = (gray.shape[1], gray.shape[0])

        if image_size is None:
            image_size = current_size
        elif current_size != image_size:
            print(f"跳过尺寸不一致的图片: {image_path}")
            continue

        found, corners = cv2.findChessboardCorners(
            gray,
            PATTERN_SIZE,
            cv2.CALIB_CB_ADAPTIVE_THRESH
            | cv2.CALIB_CB_NORMALIZE_IMAGE,
        )

        if not found:
            print(f"未检测到角点: {image_path}")
            continue

        refined_corners = cv2.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            (
                cv2.TERM_CRITERIA_EPS
                + cv2.TERM_CRITERIA_MAX_ITER,
                30,
                0.001,
            ),
        )

        object_points.append(object_template.copy())
        image_points.append(refined_corners)

        print(f"检测成功: {image_path}")

    valid_count = len(object_points)

    if valid_count < 5:
        print(f"有效标定图片太少: {valid_count} 张")
        return 1

    calibration_result = cv2.calibrateCamera(
        object_points,
        image_points,
        image_size,
        None,
        None,
    )

    (
        calibration_success,
        camera_matrix,
        distortion,
        rotation_vectors,
        translation_vectors,
    ) = calibration_result

    if not calibration_success:
        print("相机标定失败")
        return 1

    total_error = 0.0

    for index in range(valid_count):
        projected_points, _ = cv2.projectPoints(
            object_points[index],
            rotation_vectors[index],
            translation_vectors[index],
            camera_matrix,
            distortion,
        )

        detected = image_points[index].reshape(-1, 2)
        projected = projected_points.reshape(-1, 2)

        point_errors = np.linalg.norm(
            detected - projected,
            axis=1,
        )

        total_error += float(point_errors.mean())

    mean_error = total_error / valid_count

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    np.savez(
        OUTPUT_PATH,
        camera_matrix=camera_matrix,
        distortion=distortion,
        image_width=image_size[0],
        image_height=image_size[1],
        pattern_width=PATTERN_SIZE[0],
        pattern_height=PATTERN_SIZE[1],
        square_size_mm=SQUARE_SIZE_MM,
        reprojection_error=mean_error,
    )

    print()
    print(f"有效图片数量: {valid_count}/{len(image_paths)}")
    print("相机内参矩阵:")
    print(camera_matrix)
    print("畸变参数:")
    print(distortion.ravel())
    print(f"平均重投影误差: {mean_error:.4f} 像素")
    print(f"参数已保存: {OUTPUT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
