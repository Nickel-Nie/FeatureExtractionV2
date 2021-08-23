import tkinter

from PacketLengthRange import PacketLengthRange


class PacketFilter:
    def __init__(self, lengthRange: PacketLengthRange, firstmPackets: int, firstnBytes: int):
        self.lengthRange = lengthRange
        self.firstmPackets = firstmPackets
        self.firstnBytes = firstnBytes

    def filter(self, packetDataList: list[bytes]) -> dict[int, bytes]:
        # 进行数据过滤，第一步获取满足长度范围的报文，第二步获取前N个字节，取完M个

        availablePacketsNumber = 0
        # availablePacketsDict = {}
        servicePayloadDict = {}

        for i in range(1, len(packetDataList) + 1):  # 为了获取报文编号
            # for packetData in packetDataList:
            if availablePacketsNumber >= self.firstmPackets:
                break

            packetLength = len(packetDataList[i - 1])
            if not self.lengthRange.isInRange(packetLength):
                # 当前报文长度不在范围内，继续处理下一个报文
                continue

            servicePayloadBytes = self._extractServicePayload(packetDataList[i-1]) # 获取业务负载字节流
            if len(servicePayloadBytes) < self.firstnBytes:
                # 业务负载字节流长度不足N，继续处理下一个报文
                continue

            availablePacketsNumber += 1
            # availablePacketsDict[i] = packetDataList[i-1]
            servicePayloadDict[i] = servicePayloadBytes[0:self.firstnBytes]  # 获取前n字节的业务负载数据

        return servicePayloadDict

    def _extractServicePayload(self, frameBytes: bytes):
        """
        处理报文字节流，获取业务负载字节流，即获取TCP以及UDP，并排除DNS(通过端口号53进行排除)
        返回
        :param frameBytes:
        :return:业务负载，以16进制字符流返回
        """
        # MAC_destination = frameBytes[0:6].hex()
        # MAC_source = frameBytes[6:12].hex()
        # MAC_type = frameBytes[12:14].hex()

        IP_dataOffset = 14
        _TCP = 6
        _UDP = 17

        IP_headerLength = (frameBytes[IP_dataOffset] & 0x0f) * 4
        IP_totalLength = int.from_bytes(frameBytes[IP_dataOffset + 2:IP_dataOffset + 4], "big", signed=False)  # 网络字节序
        IP_protocol = frameBytes[IP_dataOffset + 9]  # 传输层协议：6为TCP，17为UDP，其余均过滤

        # Transport Layer
        TL_dataOffset = IP_dataOffset + IP_headerLength
        TL_sourcePortBytes = frameBytes[TL_dataOffset: TL_dataOffset + 2]
        TL_sourcePort = int.from_bytes(TL_sourcePortBytes, "big", signed=False)
        TL_destinationPortBytes = frameBytes[TL_dataOffset + 2: TL_dataOffset + 4]
        TL_destinationPort = int.from_bytes(TL_destinationPortBytes, "big", signed=False)

        if IP_protocol == _TCP:
            # TCP头部长度
            TL_headerLength = ((frameBytes[TL_dataOffset + 12] & 0xf0) >> 4) * 4
            servicePayloadOffset = TL_dataOffset + TL_headerLength
        elif IP_protocol == _UDP:
            # UDP头部长度恒为8，故无需计算头部长度
            TL_headerLength = 8
            servicePayloadOffset = TL_dataOffset + 8
        else:
            return None

        if TL_sourcePort == 53 or TL_destinationPort == 53:
            return None

        payloadLength = IP_totalLength - IP_headerLength - TL_headerLength
        servicePayloadBytes = frameBytes[servicePayloadOffset: servicePayloadOffset + payloadLength]
        # print(f'payloadLength={payloadLength}, servicePayload=', end='')
        return servicePayloadBytes
