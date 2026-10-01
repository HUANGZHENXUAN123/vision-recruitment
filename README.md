# RoboMaster 视觉招新考核

本项目用于完成 RoboMaster 视觉组招新考核，包含以下三个任务：

1. 蓝色装甲板灯条检测
2. 相机标定与 AprilTag 位姿估计
3. CV1 模拟串口通信

## 目录

- 环境与依赖
- 项目结构
- 任务一：蓝色灯条检测
- 任务二：AprilTag 位姿估计
- 任务三：CV1 串口通信
- 验证结果
- 提交材料
- 已知问题

## 环境与依赖

### 开发环境

| 项目 | 版本 |
| --- | --- |
| 操作系统 | Ubuntu 22.04.5 LTS |
| Python | 3.10.12 |
| pip | 25.2 |
| OpenCV | 5.0.0 |
| Git | 2.34.1 |

### Python 依赖

完整依赖版本记录在 `requirements.txt` 中，主要包括：

- numpy
- opencv-python
- pupil-apriltags
- pyserial
- PyYAML
- matplotlib

### Ubuntu 环境安装

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows 环境安装

任务三需要访问 Windows 摄像头和虚拟串口，因此使用 Windows Python 运行：

```powershell
python -m pip install -r requirements.txt
```

## 项目结构

```
vision-recruitment/
├── README.md
├── requirements.txt
├── .gitignore
├── opencv_basics/
│   ├── basic_image.py
│   ├── blue_mask.py
│   ├── morphology.py
│   ├── contours.py
│   ├── extract_frame.py
│   ├── experiment_notes.md
│   └── output/
├── task1_lightbar/
│   ├── detect_video.py
│   ├── README.md
│   └── representative_frames/
├── task2_apriltag/
│   ├── calibrate_camera.py
│   ├── detect_tag.py
│   ├── estimate_pose.py
│   ├── README.md
│   ├── calibration_info.txt
│   ├── tag_info.txt
│   ├── pose_experiment.md
│   └── output/              # 本地生成，未纳入 Git
└── task3_serial/
    ├── README.md
    ├── config.json
    ├── cv1_protocol.py
    ├── detect_apriltag_serial.py
    ├── test_log.md
    └── logs/
        └── serial_receive.log
```

目录职责：

- `opencv_basics/`：OpenCV 基础练习和中间处理结果。
- `task1_lightbar/`：视频蓝色装甲板灯条检测。
- `task2_apriltag/`：相机标定、AprilTag 检测和三维位姿估计。
- `task3_serial/`：CV1 协议组帧、串口发送和联调记录。

## 任务一：蓝色灯条检测

### 处理流程

```
视频读取
  ↓
BGR 转 HSV
  ↓
蓝色区域分割
  ↓
形态学开运算与闭运算
  ↓
轮廓提取
  ↓
面积和长宽比筛选
  ↓
旋转矩形框选
  ↓
显示帧号、灯条数量和处理耗时
  ↓
保存标注视频
```

### 使用的 OpenCV 方法

- `cv2.VideoCapture`
- `cv2.cvtColor`
- `cv2.split`
- `cv2.inRange`
- `cv2.threshold`
- `cv2.morphologyEx`
- `cv2.findContours`
- `cv2.contourArea`
- `cv2.minAreaRect`
- `cv2.boxPoints`
- `cv2.VideoWriter`

### 运行方式

```bash
python task1_lightbar/detect_video.py \
    task1_lightbar/input.mp4 \
    task1_lightbar/output/lightbar_result.mp4
```

### 运行参数

| 参数 | 含义 |
| --- | --- |
| 第一个路径 | 输入视频路径 |
| 第二个路径 | 输出视频路径 |
| HSV 下限 | (80, 120, 110) |
| HSV 上限 | (135, 255, 255) |
| B-R 差分阈值 | 40 |
| 形态学卷积核 | 1 × 1（对比实验后保留流程） |
| 最小轮廓面积 | 3 |
| 最大轮廓面积 | 100000 |
| 长宽比范围 | 1.5 ～ 20 |

### 输出内容

程序在输出视频中显示：

- 当前帧号。
- 当前帧检测到的灯条数量。
- 当前帧处理耗时。
- 每根候选灯条的旋转矩形。
- 候选区域面积。
- 候选区域长宽比。

输出视频由程序在本地生成：

```
task1_lightbar/output/lightbar_result.mp4
```

### OpenCV 基础练习

基础练习位于：

```
opencv_basics/
```

包括：

- 图像读取。
- BGR 通道分离。
- 灰度图转换。
- HSV 颜色分割。
- 形态学开运算和闭运算。
- 轮廓提取。
- 面积筛选。
- 长宽比筛选。
- 旋转矩形检测。

## 任务二：AprilTag 位姿估计

### 处理流程

```
相机读取
  ↓
棋盘格相机标定
  ↓
AprilTag 检测
  ↓
指定 ID 筛选
  ↓
solvePnP 位姿估计
  ↓
输出旋转矩阵、平移向量和直线距离
```

### 相机标定

运行标定程序：

```bash
python task2_apriltag/calibrate_camera.py
```

标定结果由程序在本地生成（当前被 `.gitignore` 排除）：

```
task2_apriltag/output/camera_params.npz
```

标定参数：

| 参数 | 数值 |
| --- | --- |
| 有效标定图片 | 17/18 |
| 棋盘格内角点 | 9 × 6 |
| 平均重投影误差 | 1.0518 px |
| 相机图像宽度 | 以 camera_params.npz 为准 |
| 相机图像高度 | 以 camera_params.npz 为准 |
| 方格边长 | 见 calibration_info.txt |

标定文件包含：

- `camera_matrix`
- `distortion`
- `image_width`
- `image_height`
- `pattern_width`
- `pattern_height`
- `square_size_mm`
- `reprojection_error`

### AprilTag 参数

- Tag 家族：`tag36h11`
- Tag 边长：0.163 m
- 目标 ID：通过运行时的 `--target-id` 参数指定。
- Tag 边长指黑色外框边长，不包括外部白色边缘。

### 位姿估计

```bash
python task2_apriltag/detect_tag.py
python task2_apriltag/estimate_pose.py
```

输出结果：

```
task2_apriltag/output/
```

### 相机坐标系

- X：图像向右
- Y：图像向下
- Z：镜头前方

位姿变换关系：

```
p_camera = R × p_tag + t
```

其中：

- `R`：Tag 坐标系到相机坐标系的旋转矩阵。
- `t`：Tag 中心在相机坐标系中的平移向量。
- `x`、`y`、`z`：平移向量的三个分量。
- `z`：Tag 在相机前方的深度，不等于直线距离。

直线距离计算：

```
distance = sqrt(x² + y² + z²)
```

已验证的位姿结果：

第一张图片：

```
t ≈ (-0.0147, -0.0510, 0.5604) m
distance ≈ 0.5630 m
```

第二张图片：

```
t ≈ (0.0469, -0.0316, 0.7054) m
distance ≈ 0.7076 m
```

## 任务三：CV1 串口通信

### 数据流

```
USB 摄像头
  ↓
AprilTag 检测
  ↓
solvePnP 位姿估计
  ↓
tvec / rvec
  ↓
CV1 报文组帧
  ↓
COM11
  ↓
COM12
  ↓
串口助手
```

### 运行环境

由于 WSL 当前无法直接访问 Windows 摄像头和 COM 端口，任务三使用 Windows Python 运行。

| 项目 | 配置 |
| --- | --- |
| 摄像头 | USB 摄像头 |
| 摄像头编号 | 1 |
| Python 发送端 | COM11 |
| 串口助手接收端 | COM12 |
| 波特率 | 115200 |
| 数据位 | 8 |
| 校验位 | 无 |
| 停止位 | 1 |
| 流控 | 无 |

### 配置文件

配置文件：

```
task3_serial/config.json
```

主要配置：

```json
{
  "pattern_size": [9, 6],
  "square_size_m": 0.025,
  "tag_size_m": 0.163,
  "expected_width": 1280,
  "expected_height": 720,
  "serial_port": "COM11",
  "serial_baudrate": 115200,
  "calibration_file": "../task2_apriltag/output/camera_params.npz"
}
```

任务三读取任务二生成的标定文件：

```
../task2_apriltag/output/camera_params.npz
```

### 运行方式

在 Windows PowerShell 中进入仓库根目录：

```powershell
Set-Location "C:\Users\32716\Desktop\vision-recruitment-win"
```

运行程序：

```powershell
python .\task3_serial\detect_apriltag_serial.py `
    --camera 1 `
    --target-id 0 `
    --port COM11
```

如果实际 Tag ID 不是 0，将 `--target-id 0` 替换为实际目标 ID。

### CV1 报文格式

```
$CV1,seq,t_ms,valid,id,x_mm,y_mm,z_mm,rx,ry,rz*HH\r\n
```

其中 `\r\n` 表示真实发送的两个字节：

```
0D 0A
```

### 报文示例

```
$CV1,42,12345,1,0,100.0,-50.0,800.0,0.000000,0.000000,0.000000*33\r\n
```

### 字段说明

| 字段 | 含义 |
| --- | --- |
| `$CV1` | 报文起始标识和协议版本 |
| seq | 32 位无符号递增序号，从 0 开始 |
| t_ms | 程序启动后的毫秒数 |
| valid | 位姿是否有效，1 有效，0 无效 |
| id | AprilTag ID，无效时为 -1 |
| x_mm | Tag 在相机坐标系中的 X 坐标，单位为毫米 |
| y_mm | Tag 在相机坐标系中的 Y 坐标，单位为毫米 |
| z_mm | Tag 在相机坐标系中的 Z 坐标，单位为毫米 |
| rx | Rodrigues 旋转向量 X 分量，单位为弧度 |
| ry | Rodrigues 旋转向量 Y 分量，单位为弧度 |
| rz | Rodrigues 旋转向量 Z 分量，单位为弧度 |
| HH | `$` 和 `*` 之间所有 ASCII 字节的 XOR 校验值 |

### 报文要求

- 坐标由米转换为毫米。
- 坐标保留 1 位小数。
- 旋转向量使用弧度。
- 旋转向量保留 6 位小数。
- 不将 Rodrigues 旋转向量转换为欧拉角。
- 校验值为两位大写十六进制。
- 报文结尾使用真实的 CRLF。
- 建议发送频率约为 10 Hz。
- 不要求额外的接收超时机制。
- 不要求多线程。
- 不要求额外编写接收校验脚本。

### 无效状态

以下情况发送无效报文：

- 未检测到 AprilTag。
- 检测到的 ID 与目标 ID 不匹配。
- 位姿估计失败。
- 摄像头读取到空帧。

无效报文状态：

```
valid=0
id=-1
x_mm=0.0
y_mm=0.0
z_mm=0.0
rx=0.000000
ry=0.000000
rz=0.000000
```

目标重新出现后，程序恢复发送有效位姿。

## 验证结果

### 任务一

- [x] 完成 Ubuntu、Python、Git 和 OpenCV 环境配置。
- [x] 完成图片读取。
- [x] 完成 BGR、灰度图和 HSV 学习。
- [x] 完成 HSV 蓝色分割。
- [x] 完成形态学开运算和闭运算。
- [x] 完成轮廓提取。
- [x] 完成面积和长宽比筛选。
- [x] 完成旋转矩形筛选。
- [x] 完成视频逐帧处理。
- [x] 完成输出标注视频。

### 任务二

- [x] 完成棋盘格相机标定。
- [x] 完成 18 张标定图片采集。
- [x] 有效标定图片数量为 17/18。
- [x] 平均重投影误差为 1.0518 px。
- [x] 完成 tag36h11 AprilTag 检测。
- [x] 完成指定 ID 检测。
- [x] 完成三维位姿估计。
- [x] 完成旋转矩阵和 Rodrigues 旋转向量输出。
- [x] 完成平移向量输出。
- [x] 完成直线距离计算。
- [x] 完成无 Tag 异常测试。
- [x] 完成不同距离和角度的位姿对比。

### 任务三

- [x] 完成 CV1 报文组帧。
- [x] 完成 XOR 校验。
- [x] 完成米到毫米的坐标转换。
- [x] 完成 Rodrigues 旋转向量输出。
- [x] 完成 115200/8N1 串口配置。
- [x] 完成虚拟串口连接。
- [x] 完成 Python 发送端与串口助手接收端联调。
- [x] 完成无效状态报文发送。
- [x] 完成有效状态报文发送。
- [x] 完成目标重新出现后的有效状态恢复。
- [x] 完成串口接收日志保存。

串口接收日志：

```
task3_serial/logs/serial_receive.log
```

## 提交材料

### 任务一

```
task1_lightbar/
├── detect_video.py
├── README.md
└── representative_frames/
```

输入视频与完整标注视频未纳入 Git，需在最终问卷或 README 中补充可访问的下载链接。

### 任务二

```
task2_apriltag/
├── calibrate_camera.py
├── detect_tag.py
├── estimate_pose.py
├── README.md
├── calibration_info.txt
├── tag_info.txt
└── pose_experiment.md
```

标定原图、`camera_params.npz` 和位姿演示图片当前未纳入 Git，需另附下载链接或在容量允许时提交。

### 任务三

```
task3_serial/
├── README.md
├── config.json
├── cv1_protocol.py
├── detect_apriltag_serial.py
├── test_log.md
└── logs/
    └── serial_receive.log
```

### Git 提交

查看工作区状态：

```bash
git status
```

查看最近提交：

```bash
git log --oneline -10
```

提交 README：

```bash
git add README.md
git commit -m "document vision recruitment project"
```
## 参考资料

- [OpenCV 官方文档](https://docs.opencv.org/)
- [OpenCV Camera Calibration](https://docs.opencv.org/4.5.2/dc/dbb/tutorial_py_calibration.html)
- [AprilTag 官方项目](https://github.com/AprilRobotics/apriltag)
- [pupil-apriltags](https://github.com/pupil-labs/apriltags)
- [pySerial 官方文档](https://pyserial.readthedocs.io/)
- [SerialPortAssistant](https://github.com/KangLin/SerialPortAssistant/releases)
- [COMTool](https://github.com/Neutree/COMTool)
- RoboMaster 视觉组招新考核手册（26.9）

## 已知问题

- WSL 当前无法直接访问 Windows 摄像头和 COM 端口。
- 任务三需要在 Windows Python 环境中运行。
- USB 摄像头编号为 1。
- Python 发送端使用 COM11。
- 串口助手接收端使用 COM12。
- 相机标定参数只适用于对应摄像头、分辨率和焦距。
- 更换摄像头、分辨率或焦距后需要重新标定。
- `input.mp4`、输出视频、测试图片和调试图片不建议提交到 Git。
- `.venv/`、`__pycache__/` 和 `*.pyc` 文件不属于提交材料。
