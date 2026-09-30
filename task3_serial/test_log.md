# 任务三联调记录

- 摄像头：USB 摄像头，编号 1
- 串口发送端：COM11
- 串口接收端：COM12
- 波特率：115200
- 数据格式：8N1
- Tag 家族：tag36h11
- Tag ID：0
- Tag 边长：0.163 m

## 测试结果

- [x] Tag 出现时 valid=1
- [x] Tag 消失时 valid=0
- [x] Tag 再次出现后恢复 valid=1
- [x] seq 持续递增
- [x] 坐标单位为 mm
- [x] 旋转向量单位为 rad
- [x] XOR 校验正确
- [x] CRLF 正确

