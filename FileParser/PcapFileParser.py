from pathlib import Path

from FileParser.FileParser import FileParser


class PcapFileParser(FileParser):

    PCAP_HEADER_LENGTH = 24
    PACKET_HEADER_LENGTH = 16

    def __init__(self, file: Path):
        super().__init__(file)
        self.filePtr = self.file.open('rb')
        # self.endian = self._getEndian()  # 获得字节序，供后续解析使用

    def parse(self) -> list[str]:
        packetDataList = []

        # # 跳过文件头
        # self.filePtr.seek(self.PCAP_HEADER_LENGTH, 1)
        # 处理文件头
        pcapHeaderBytes = self.filePtr.read(self.PCAP_HEADER_LENGTH)
        self._processPcapHeader(pcapHeaderBytes)

        while True:
            # 16Bytes Packet Header
            packetHeaderBytes = self.filePtr.read(self.PACKET_HEADER_LENGTH)
            if len(packetHeaderBytes) < self.PACKET_HEADER_LENGTH:
                break

            captureLength = int.from_bytes(packetHeaderBytes[8:12], self.endian, signed=False)
            packetDataBytes = self.filePtr.read(captureLength)
            packetDataList.append(packetDataBytes.hex())

        return packetDataList

    def _processPcapHeader(self, pcapHeaderBytes:bytes):
        magicBytes = pcapHeaderBytes[0:4]
        if magicBytes == b"\xd4\xc3\xb2\xa1":
            self.endian = "little"
        else:
            self.endian = "big"

    # def _getEndian(self) -> str:
    #     magicBytes = self.filePtr.read(4)
    #     self.filePtr.seek(0, 0)  # 回到文件开头
    #
    #     if magicBytes == b"\xd4\xc3\xb2\xa1":
    #         return "small"
    #     else:
    #         return "big"
