from pathlib import Path

from PacketLengthRange import PacketLengthRange


class DirectoryHandler:
    def __init__(self, directory, packetLengthRange, firstmPackets, firstnBytes):
        path = Path(directory)
        if not path.is_dir():  # 不是目录，直接失败
            raise Exception("请传入目录，而不是文件")

        self.absolutePath = path.resolve()
        self._makeDirectory(packetLengthRange, firstmPackets, firstnBytes)

    def getAllDumpFile(self):
        pcapngFilenames = [pcapngFile.name for pcapngFile in self.absolutePath.glob('*.pcapng')]
        pcapFilenames = [pcapFile.name for pcapFile in self.absolutePath.glob('*.pcap')]
        return pcapngFilenames + pcapFilenames

    def _makeDirectory(self, packetLengthRange:PacketLengthRange, firstmPacket:int, firstnBytes:int):
        prefixName = packetLengthRange.rangeString + "-" + str(firstmPacket) + "-" + str(firstnBytes)
        directoryList = []

        jsonDirectory = prefixName + "-JSON"
        self.jsonDirectory = str(self.absolutePath.joinpath(jsonDirectory))
        directoryList.append(jsonDirectory)

        md5Directory = prefixName + "-MD5"
        self.md5Directory = str(self.absolutePath.joinpath(md5Directory))
        directoryList.append(md5Directory)

        featureDirectory = prefixName + "-FEATURE"
        self.featureDirectory = str(self.absolutePath.joinpath(featureDirectory))
        directoryList.append(featureDirectory)

        for directory in directoryList:
            directoryPath = self.absolutePath.joinpath(directory)
            if directoryPath.exists():
                print(f"{directory}目录已存在")
            else:
                directoryPath.mkdir()

