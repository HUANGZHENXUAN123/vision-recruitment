# Task3 学习进度与主任务整合说明

## 1. Task3 已完成内容

- 理解 CV1 报文结构：`$CV1,seq,t_ms,valid,id,x_mm,y_mm,z_mm,rx,ry,rz*HH\r\n`。
- 掌握 XOR 校验范围：只计算 `$` 后、`*` 前的 ASCII 字节，结果为两位大写十六进制。
- 掌握数据格式：坐标保留 1 位小数，旋转向量保留 6 位小数。
- 明确 CRLF 必须是实际字节 `0D 0A`。
- 建立 Windows 虚拟串口对，完成 115200/8N1、无流控配置。
- Python 已能持续发送固定和模拟 CV1 报文，串口助手配对端已成功接收。
- 已实现序号递增、运行毫秒时间、有效/无效状态和串口异常处理。

## 2. 文件用途

- `cv1_protocol.py`：Task3 的协议层，只负责校验、组帧和打开串口，可被其他主程序导入。
- `detect_apriltag.py`：原 Task2 独立检测程序，保留用于单独排查相机和位姿问题。
- `detect_apriltag_serial.py`：整合后的主程序，连接“相机检测结果”和“CV1 串口输出”。
- `config.json`：相机、Tag 尺寸和串口配置。
- 桌面的 `serial_cv1_test.py`：Task3 独立模拟发送程序，保留用于排查串口链路。
- 桌面的 `stage3_sender.txt`：一次运行输出记录，不是程序源码。

## 3. 整合后的数据流

`相机 → AprilTag 检测 → solvePnP → tvec/rvec → CV1 组帧 → COM11 → 配对端 → 串口助手/下位机`

- `tvec` 的单位由米乘 1000 转换为毫米，填入 `x_mm/y_mm/z_mm`。
- `rvec` 本身就是 Rodrigues 旋转向量，直接填入 `rx/ry/rz`。
- 检测到目标 ID：`valid=1`，发送真实 ID、坐标和旋转向量。
- 未检测到目标 ID或解算失败：`valid=0,id=-1`，坐标和旋转全部置零。
- `seq` 每帧加 1，`t_ms` 是程序启动后的单调毫秒数。

## 4. 运行前检查

1. `config.json` 中的 `tag_size_m` 必须是 Tag 黑色外框的真实边长。
2. 必须存在有效的 `calibration_data.npz`，相机分辨率应与标定时一致。
3. `serial_port` 填 Python 发送端；串口助手打开虚拟串口对的另一端。
4. 两个程序不能打开同一个 COM 端口。

## 5. 运行方式

在本目录打开 PowerShell：

```powershell
python detect_apriltag_serial.py --camera 0 --target-id 0
```

临时指定其他串口时：

```powershell
python detect_apriltag_serial.py --camera 0 --target-id 0 --port COM11
```

按 `q` 正常退出。

## 6. 分层排错顺序

1. 先运行 `detect_apriltag.py`，确认相机、标定和位姿正常。
2. 再运行桌面 `serial_cv1_test.py`，确认虚拟串口链路正常。
3. 两项都正常后，运行 `detect_apriltag_serial.py`。

这样可以快速判断故障来自视觉部分还是串口部分。
