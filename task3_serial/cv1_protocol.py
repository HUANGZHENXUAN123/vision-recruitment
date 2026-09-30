"""CV1 ASCII 报文生成与串口发送工具。"""

from __future__ import annotations

import serial


def xor_checksum(payload: str) -> str:
    """计算 $ 之后、* 之前全部 ASCII 字节的 XOR 校验。"""
    checksum = 0
    for byte in payload.encode("ascii"):
        checksum ^= byte
    return f"{checksum:02X}"


def make_packet(
    seq: int,
    t_ms: int,
    valid: int,
    tag_id: int,
    x_mm: float,
    y_mm: float,
    z_mm: float,
    rx: float,
    ry: float,
    rz: float,
) -> bytes:
    """按照 CV1 格式生成以真实 CRLF 结尾的 ASCII 字节串。"""
    payload = (
        f"CV1,{seq},{t_ms},{valid},{tag_id},"
        f"{x_mm:.1f},{y_mm:.1f},{z_mm:.1f},"
        f"{rx:.6f},{ry:.6f},{rz:.6f}"
    )
    return f"${payload}*{xor_checksum(payload)}\r\n".encode("ascii")


def open_serial(port: str, baudrate: int = 115200) -> serial.Serial:
    """以 115200/8N1、无软硬件流控打开发送端。"""
    return serial.Serial(
        port=port,
        baudrate=baudrate,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
    )
