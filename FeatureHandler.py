import json
from DirectoryHandler import DirectoryHandler
from pathlib import Path

class FeatureHandler:
    def __init__(self, jsonDirectory, md5Directory, featureDirectory, featureNumbers):
        self.jsonDirectory = Path(jsonDirectory)
        self.md5Directory = Path(md5Directory)
        self.featureDirectory = Path(featureDirectory)
        self.featureNumbers = featureNumbers

    def handle(self):
        jsonList = self._getDataFromJson()

        for i in range(self.featureNumbers):
            for currentJsonData in jsonList:
                currentFilename = currentJsonData.get('name')
                currentPacketsDataList = currentJsonData.get('packetInfoList')

                if currentPacketsDataList is None:
                    # 该文件内没有符合要求的报文，处理下一个文件，
                    continue

                for currentPacketData in currentPacketsDataList:
                    if currentPacketData.get('isFeature') != 0:  # 0才是未判断的
                        continue

                    currentMd5 = currentPacketData.get('MD5')
                    isFeature = True  # 内部循环开始判断是否为特征

                    for jsonData in jsonList:
                        if jsonData.get('name') == currentFilename or jsonData.get('packetInfoList') is None:
                            # 相同文件，不需要比较，跳过
                            # 或者说不存在报文数据
                            continue

                        for packetData in jsonData.get('packetInfoList'):
                            if currentMd5 == packetData.get('MD5'):
                                # 非特征
                                currentPacketData['isFeature'] = -1
                                currentPacketData['samePacket'] = dict(name=jsonData.get('name'),
                                                                       targetNo=packetData.get('packetNo'))

                                packetData['isFeature'] = -1
                                packetData['samePacket'] = dict(name=currentFilename,
                                                                targetNo = currentPacketData.get('packetNo'))
                                isFeature = False

                        if not isFeature:
                            # 后续文件不需要再判断，此时已经存在相同的md5了
                            break

                    if isFeature:
                        # 所有文件判断下来后都不存在相同的值，说明是特征，则继续下个文件的特征值判断
                        currentPacketData['isFeature'] = 1
                        currentJsonData['featureCount'] += 1
                        break

        # 所有MD5值比对完成
        self._saveJsonFiles(jsonList)
        self._saveMD5Files(jsonList)
        self._saveFeatureFiles(jsonList)

    def _getDataFromJson(self) -> list:
        jsonFiles = DirectoryHandler.getFilenamesByType(self.jsonDirectory, 'json')
        dataList = []
        for jsonFile in jsonFiles:
            f = self.jsonDirectory.joinpath(jsonFile).open('r')
            dataList.append(json.loads(f.read()))
            f.close()
        return dataList

    def _saveJsonFiles(self, jsonList):
        for jsonData in jsonList:
            filename = jsonData.get('name') + '.json'
            f = self.jsonDirectory.joinpath(filename).open('w')  # 覆盖
            f.write(json.dumps(jsonData))
            f.close()

    def _saveMD5Files(self, jsonList):
        for jsonData in jsonList:
            filename = jsonData.get('name') + '.txt'
            f = self.md5Directory.joinpath(filename).open('w')
            f.write(f'availablePacketsCount: {jsonData.get("availablePacketsCount")}\n')
            f.write('=' * 100 + '\n')
            i = 1
            for packetData in jsonData.get('packetInfoList'):
                f.write(f'PacketNo: {packetData.get("packetNo")}\n')
                f.write(f'PacketLength: {packetData.get("packetLength")}\n')
                f.write(f'FirstnBytes: {packetData.get("servicePayload")}\n')
                f.write(f'MD5: {packetData.get("MD5")}\n')
                f.write('=' * 100 + '\n')
                i += 1
            f.close()
            pass

    def _saveFeatureFiles(self, jsonList):
        for jsonData in jsonList:
            filename = jsonData.get('name') + '.txt'
            f = self.featureDirectory.joinpath(filename).open('w')
            f.write(f'FeatureNumbers: {jsonData.get("featureCount")}\n')
            f.write('=' * 100 + '\n')
            i = 1
            for packetData in jsonData.get('packetInfoList'):
                if packetData.get('isFeature') == 1:
                    f.write(f'Feature {i}:\n')
                    f.write(f'PacketNo: {packetData.get("packetNo")}\n')
                    f.write(f'FeatureString: {packetData.get("servicePayload")}\n')
                    f.write('=' * 100 + '\n')
                    i += 1
            f.close()
