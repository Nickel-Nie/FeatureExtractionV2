from pathlib import Path

from FileParser.FileParser import FileParser


class PcapFileParser(FileParser):
    def __init__(self, file: Path):
        super().__init__(file)
        self.filePtr = self.file.open('r')
        self.endian = self._getEndian()  # 获得字节序，供后续解析使用

    def parse(self):
        pass

    def _getEndian(self) -> str:
        magic = self.filePtr.read(4)
        self.filePtr.seek(0, 0)  # 回到文件开头

        if magic == b"\xd4\xc3\xb2\xa1":
            return "small"
        else:
            return "big"
