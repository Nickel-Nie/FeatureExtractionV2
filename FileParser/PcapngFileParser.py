from pathlib import Path

from FileParser.FileParser import FileParser


class PcapngFileParser(FileParser):
    def __init__(self, file: Path):
        super().__init__(file)

    def parse(self):
        pass