from pathlib import Path

class FileParser:
    def __init__(self, file:Path):
        self.file = file

    def parse(self) -> list[str]:
        # 将字节转换为16进制字符串
        pass