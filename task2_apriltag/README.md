# 任务二：相机标定与 AprilTag 位姿估计

## 参数

- AprilTag 家族：`tag36h11`
- 目标 ID：`0`
- Tag 黑色外框边长：`0.163 m`
- 棋盘格内角点：`9×6`
- 方格边长：`22.0 mm`
- 有效标定图片：`17/18`
- 平均重投影误差：`1.0518 px`

## 运行

从仓库根目录执行：

```bash
python task2_apriltag/calibrate_camera.py
python task2_apriltag/detect_tag.py <测试图片>
python task2_apriltag/estimate_pose.py <测试图片>
```

标定程序生成 `task2_apriltag/output/camera_params.npz`。位姿程序读取其中的内参、畸变参数及标定分辨率，输出指定 Tag 的中心、角点、坐标轴、旋转矩阵 `R`、平移向量 `t` 和直线距离。

## 坐标与单位

- 相机坐标系：X 向右、Y 向下、Z 向镜头前方。
- 变换关系：`p_camera = R × p_tag + t`。
- 程序内部平移单位为米；任务三发送时转换为毫米。
- 直线距离为 `sqrt(x²+y²+z²)`，不等同于 Z 深度。

## 验收材料

- `calibration_info.txt`：标定配置和结果。
- `tag_info.txt`：Tag 家族、ID 和实测边长。
- `pose_experiment.md`：不同距离/角度以及无 Tag 情况的测试记录。
- 标定原图、参数文件和位姿演示图片由 `.gitignore` 排除；最终提交时应另附下载链接，或按提交平台容量限制加入仓库。
