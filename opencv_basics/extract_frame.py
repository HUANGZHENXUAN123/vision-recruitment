import sys
from pathlib import Path

import cv2


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python extract_frame.py <视频路径> <帧号>")
        return 1

    video_path = Path(sys.argv[1])
    frame_number = int(sys.argv[2])

    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        print(f"无法打开视频: {video_path}")
        return 1

    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    success, frame = capture.read()
    capture.release()

    if not success:
        print(f"无法读取第 {frame_number} 帧")
        return 1

    output_path = Path("opencv_basics/debug_frame.jpg")
    cv2.imwrite(str(output_path), frame)

    print(f"已保存第 {frame_number} 帧:")
    print(output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
