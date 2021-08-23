from pathlib import Path

from FileParser.FileParser import FileParser


class PcapngFileParser(FileParser):
    ALIGNED_BYTES = 4  # 四字节对齐

    def __init__(self, file: Path):
        super().__init__(file)
        self.filePtr = self.file.open('rb')

    def parse(self) -> list[str]:
        packetDataList = []

        # 以节头块开头，获取字节序
        self._processSectionHeaderBlock()

        # 循环遍历每一个Block
        while True:

            blockTypeBytes = self.filePtr.read(self.ALIGNED_BYTES)
            if len(blockTypeBytes) < self.ALIGNED_BYTES:
                break  # 读取结束
            blockTotalLengthBytes = self.filePtr.read(self.ALIGNED_BYTES)
            blockType = int.from_bytes(blockTypeBytes, self.endian, signed=False)
            blockTotalLength = int.from_bytes(blockTotalLengthBytes, self.endian, signed=False)

            blockDataBytes = self.filePtr.read(blockTotalLength - 3*self.ALIGNED_BYTES)
            blockTotalLength2Bytes = self.filePtr.read(self.ALIGNED_BYTES)  # 重复的字段
            # 构建block数据
            blockBytes = blockTypeBytes + blockTotalLengthBytes + blockDataBytes + blockTotalLength2Bytes

            packetDataBytes = b""
            if blockType == 0x01:
                self._processInterfaceDescriptionBlock(blockBytes)
            elif blockType == 0x06:
                packetDataBytes = self._processEnhancedPacketBlock(blockBytes)
            elif blockType == 0x03:
                packetDataBytes = self._processSimplePacketBlock(blockBytes)
            elif blockType == 0x02:
                packetDataBytes = self._processPacketBlock(blockBytes)
            else:
                print("未知Block类型")

            if len(packetDataBytes) != 0:
                packetDataList.append(packetDataBytes.hex())

        return packetDataList

    def _processSectionHeaderBlock(self):
        # 处理节头块，需要获取字节序，相较于其他Block而言需要进行特殊处理
        blockTypeBytes = self.filePtr.read(self.ALIGNED_BYTES)
        blockTotalLengthBytes = self.filePtr.read(self.ALIGNED_BYTES)
        magicBytes = self.filePtr.read(self.ALIGNED_BYTES)

        if magicBytes == b"\x4d\x3c\x2b\x1a":
            self.endian = "little"
        elif magicBytes == b"\x1a\x2b\x3c\x4d":
            self.endian = "big"
        else:
            print("未知字节序")

        blockTotalLength = int.from_bytes(blockTotalLengthBytes, self.endian, signed=False)
        # 跳过节头块剩余部分
        self.filePtr.seek(blockTotalLength - 3 * self.ALIGNED_BYTES, 1)

    def _processInterfaceDescriptionBlock(self, bytesOfIDB:bytes):
        # 无需进行处理，没有需要获取的数据
        pass

    def _processEnhancedPacketBlock(self, bytesOfEPB:bytes)->bytes:
        # 需要获取packet数据
        captureLengthBytes = bytesOfEPB[20:24]
        captureLength = int.from_bytes(captureLengthBytes, self.endian, signed=False)

        packetDataBytes = bytesOfEPB[28: 28+captureLength]
        return packetDataBytes

    def _processSimplePacketBlock(self, bytesOfSPB:bytes)->bytes:
        packetLengthBytes = bytesOfSPB[8:12]
        packetLength = int.from_bytes(packetLengthBytes, self.endian, signed=False)

        packetDataBytes = bytesOfSPB[12:12+packetLength]
        return packetDataBytes

    def _processPacketBlock(self, bytesOfPB:bytes):
        # 分组块，该块已经过时
        captureLengthBytes = bytesOfPB[20:24]
        captureLength = int.from_bytes(captureLengthBytes, self.endian, signed=False)

        packetDataBytes = bytesOfPB[28: 28 + captureLength]
        return packetDataBytes
        pass

