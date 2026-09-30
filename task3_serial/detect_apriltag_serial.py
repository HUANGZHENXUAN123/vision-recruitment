"""主任务：实时检测 AprilTag，并把目标位姿作为 CV1 报文发送。"""

import argparse
import json
import time
from pathlib import Path

import cv2
import numpy as np
import serial

from cv1_protocol import make_packet, open_serial


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--target-id", type=int, default=0)
    parser.add_argument("--port", default=None, help="发送端口，例如 COM11；默认读取 config.json")
    args = parser.parse_args()

    root = Path(__file__).parent
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = root / config_path
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    port = args.port or cfg.get("serial_port", "COM11")
    baudrate = int(cfg.get("serial_baudrate", 115200))

    calibration_file = Path(
        cfg.get(
            "calibration_file",
            "../task2_apriltag/output/camera_params.npz",
        )
    )

    if not calibration_file.is_absolute():
        calibration_file = root / calibration_file

    if not calibration_file.exists():
        print(f"标定文件不存在: {calibration_file}")
        return 1

    calibration = np.load(calibration_file)
    camera_matrix = calibration["camera_matrix"]
    dist_coeffs = calibration["distortion"]
    calibration_size = (
        int(calibration["image_width"]),
        int(calibration["image_height"]),
    )
    dictionary = cv2.aruco.getPredefinedDictionary(
        cv2.aruco.DICT_APRILTAG_36h11
    )
    detector = cv2.aruco.ArucoDetector(dictionary, cv2.aruco.DetectorParameters())
    tag_size = float(cfg["tag_size_m"])
    object_points = np.array(
        [
            [-tag_size / 2, tag_size / 2, 0],
            [tag_size / 2, tag_size / 2, 0],
            [tag_size / 2, -tag_size / 2, 0],
            [-tag_size / 2, -tag_size / 2, 0],
        ],
        np.float32,
    )

    camera = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW)
    if not camera.isOpened():
        raise RuntimeError(f"无法打开摄像头 {args.camera}")

    seq = 0
    start_time = time.monotonic()

    try:
        with open_serial(port, baudrate) as sender:
            print(f"检测目标 ID={args.target_id}；通过 {port} 发送 CV1；按 q 退出")

            while True:
                ok, frame = camera.read()
                if not ok:
                    print("无法读取摄像头")
                    break

                if (frame.shape[1], frame.shape[0]) != calibration_size:
                    cv2.putText(
                        frame,
                        f"WARNING resolution {frame.shape[1]}x{frame.shape[0]} != calibration {calibration_size}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 0, 255),
                        2,
                    )

                valid = 0
                tag_id = -1
                x_mm = y_mm = z_mm = 0.0
                rx = ry = rz = 0.0

                corners, ids, _ = detector.detectMarkers(frame)
                if ids is not None:
                    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                    for corner, detected_id in zip(corners, ids.flatten()):
                        points = corner.reshape(4, 2).astype(np.float32)
                        center = tuple(points.mean(axis=0).astype(int))
                        cv2.putText(
                            frame,
                            f"ID {detected_id}",
                            center,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0),
                            2,
                        )
                        pose_ok, rvec, tvec = cv2.solvePnP(
                            object_points,
                            points,
                            camera_matrix,
                            dist_coeffs,
                            flags=cv2.SOLVEPNP_IPPE_SQUARE,
                        )
                        if pose_ok:
                            cv2.drawFrameAxes(
                                frame, camera_matrix, dist_coeffs, rvec, tvec, tag_size * 0.6, 2
                            )
                        if pose_ok and int(detected_id) == args.target_id:
                            translation = tvec.flatten()
                            rotation = rvec.flatten()
                            valid = 1
                            tag_id = int(detected_id)
                            x_mm, y_mm, z_mm = translation * 1000.0
                            rx, ry, rz = rotation

                t_ms = int((time.monotonic() - start_time) * 1000)
                packet = make_packet(
                    seq, t_ms, valid, tag_id,
                    x_mm, y_mm, z_mm, rx, ry, rz,
                )
                sender.write(packet)
                print(packet.decode("ascii").rstrip())
                seq = (seq + 1) & 0xFFFFFFFF

                cv2.imshow("AprilTag + CV1 serial", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except serial.SerialException as exc:
        print(f"串口错误：{exc}")
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
