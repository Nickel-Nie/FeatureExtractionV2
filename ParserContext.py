from FileParser.FileParser import FileParser
from FileParser.PcapFileParser import PcapFileParser
from FileParser.PcapngFileParser import PcapngFileParser

from pathlib import Path

class ParserContext:
    fileParser:FileParser = None

    def __init__(self, filename:str, filepath:str):
        # 不能够仅仅通过文件名后缀来判断是pcap类型还是pcapng类型，可能被改了后缀名
        # 需要通过文件数据进行判断
        self.file = Path(filepath).joinpath(filename)

        filePtr = self.file.open('r')
        fileTypeBytes = filePtr.read(4)

        if fileTypeBytes == b"\xd4\xc3\xb2\xa1" or fileTypeBytes == b"\xa1\xb2\xc3\xd4":
            # pcap
            self.fileParser = PcapFileParser(self.file)
        elif fileTypeBytes == b"\x0a\x0d\x0d\x0a":
            # pcapng
            self.fileParser = PcapngFileParser(self.file)
        else:
            raise Exception("未知文件类型")

        filePtr.close()

    def parse(self):
        self.fileParser.parse()
