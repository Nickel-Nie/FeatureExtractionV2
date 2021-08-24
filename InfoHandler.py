import hashlib
import json
from pathlib import Path


class InfoHandler:
    # def __init__(self, jsonDirectory):
    #     # self.featureNumbers = featureNumbers
    #     self.jsonDirectory = jsonDirectory
    #     # self.md5Directory = md5Directory
    #     # self.featureDirectory = featureDirectory

    @classmethod
    def handle(cls, filename, jsonDirectory, servicePayloadInfoList:list[dict]):
        cls._md5Calculate(servicePayloadInfoList)
        cls._saveJsonFile(filename, jsonDirectory, servicePayloadInfoList)

    @classmethod
    def _md5Calculate(cls, servicePayloadInfoList:list[dict]):
        # servicePayload是已经进行过过滤后满足条件的前n字节的数据
        # 为了使得能够与之前的md5计算结果相同，先化为16进制字符串，再进行编码获取其md4值
        # 直接在原字典内进行修改

        for servicePayloadInfo in servicePayloadInfoList:
            servicePayload = servicePayloadInfo.get('servicePayload')

            md5hash = hashlib.md5(servicePayload.hex().encode())
            md5str = md5hash.hexdigest()
            servicePayloadInfo['MD5'] = md5str
            servicePayloadInfo['isFeature'] = 0  # 表示暂未进行判断

    @classmethod
    def _saveJsonFile(cls, filename:str, jsonDirectory:str, servicePayloadInfoList:list[dict]):
        # 保存文件时需要将业务负载的字节流转换为十六进制字符串。
        packetInfoList = servicePayloadInfoList.copy()  # 得到其一个副本,防止在原对象内部进行修改
        for packetInfo in packetInfoList:
            packetInfo['servicePayload'] = packetInfo.get('servicePayload').hex()


        prefixName = filename.split('.')[0]
        jsonFilename = prefixName + ".json"
        file = Path(jsonDirectory).joinpath(jsonFilename)

        filePtr = file.open('w')
        filePtr.write(json.dumps(dict(name=prefixName,
                                      availablePacketsCount=len(servicePayloadInfoList),
                                      featureCount=0,
                                      packetInfoList=packetInfoList)))
        filePtr.close()

