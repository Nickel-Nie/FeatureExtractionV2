from pathlib import Path

from PacketLengthRange import PacketLengthRange


class DirectoryHandler:
    def __init__(self, directory, packetLengthRange, firstnBytes):
        path = Path(directory)
        if not path.is_dir():  # 不是目录，直接失败
            raise Exception("请传入目录，而不是文件")

        self.absolutePath = path.resolve()
        self._makeDirectory(packetLengthRange, firstnBytes)

    def getAllDumpFile(self):
        pcapngFilenames = [str(pcapngFile) for pcapngFile in self.absolutePath.glob('*.pcapng')]
        pcapFilenames = [str(pcapFile) for pcapFile in self.absolutePath.glob('*.pcap')]
        return pcapngFilenames + pcapFilenames

    def _makeDirectory(self, packetLengthRange:PacketLengthRange, firstnBytes:int):
        directoryList = []
        self.jsonDirectory = packetLengthRange.rangeString + "-" + str(firstnBytes) + "-JSON"
        directoryList.append(self.jsonDirectory)
        self.md5Directory = packetLengthRange.rangeString + "-" + str(firstnBytes) + "-MD5"
        directoryList.append(self.md5Directory)
        self.featureDirectory = packetLengthRange.rangeString + "-" + str(firstnBytes) + "-FEATURE"
        directoryList.append(self.featureDirectory)

        for directory in directoryList:
            directoryPath = self.absolutePath.joinpath(directory)
            if directoryPath.exists():
                print(f"{directory}目录已存在")
            else:
                directoryPath.mkdir()

