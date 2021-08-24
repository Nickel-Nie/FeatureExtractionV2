import getopt
import sys

from DirectoryHandler import DirectoryHandler
from FeatureHandler import FeatureHandler
from InfoHandler import InfoHandler
from PacketFilter import PacketFilter
from PacketLengthRange import PacketLengthRange
from ParserContext import ParserContext

def main(args):
    try:
        opts,args = getopt.getopt(args, "hi:r:m:n:x:")
    except getopt.GetoptError:
        print('ModuleTest.py -i <input filepath> -r <packet length range> -m <lte m packets> -n <first n bytes> -x <x features>' )
        sys.exit()

    inputFilepath = ""
    rangeString = ""
    firstmPackets = 0
    firstnBytes = 0
    featureNumbers = 0

    for opt, arg in opts:
        if opt == '-h':
            print("main.py -i <input filepath> -r <packet length range> -m <lte m packets> -n <first n bytes> -x <x features>\n"
                  "input filepath: 待处理目录\n"
                  "packet length range: 用于限定报文长度范围，e.g. [100:200]\n"
                  "lte m packets: 得到前m个报文\n"
                  "first n bytes: 每个报文业务载荷中的前n个字节用于计算特征值\n"
                  "x features: 每个文件获取x个特征值\n")
            sys.exit()
        elif opt == '-i':
            inputFilepath = arg
        elif opt == '-r':
            rangeString = arg
        elif opt == '-m':
            firstmPackets = int(arg)
        elif opt == '-n':
            firstnBytes = int(arg)
        elif opt == '-x':
            featureNumbers = int(arg)


def test1():
    filepath = r"C:\Users\a9241\Desktop\Learning materials\研究生\抓包任务20210611\FacebookCapture\App_Facebook_Post_01"
    # filename = "App_Facebook_Post_01_PH3.pcapng"

    range1 = PacketLengthRange("[200:300]")
    firstmPackets = 10
    firstnBytes = 32
    featureNumbers = 2

    # 第一步，进行目录处理：1.获取目录内所有捕获文件；2.创建相应的文件夹
    directoryHandler = DirectoryHandler(filepath, range1, firstmPackets, firstnBytes)
    dumpFiles = directoryHandler.getAllDumpFile()  # 获取得到的是全路径名
    # 第二步，进行文件处理: 1.获取捕获文件内所有报文数据；2.根据长度范围，m,n值进行报文数据过滤;
    packetFilter = PacketFilter(range1, firstmPackets, firstnBytes)  # 得到过滤器实例
    for dumpFile in dumpFiles:
        context = ParserContext(dumpFile, filepath, packetFilter)
        servicePayloadInfoList = context.parse()

        # 第三步，进行报文信息处理，将过滤后得到的数据进行进一步处理
        InfoHandler.handle(dumpFile, directoryHandler.jsonDirectory, servicePayloadInfoList)

    # 第四步，对保存的文件进行后续处理，从而得到唯一的特征值
    featureHandler = FeatureHandler(directoryHandler.jsonDirectory,
                                    directoryHandler.md5Directory,
                                    directoryHandler.featureDirectory,
                                    featureNumbers)
    featureHandler.handle()

def test2():
    filepath = r"C:\Users\a9241\Desktop\Learning materials\研究生\抓包任务20210611\FacebookCapture\App_Facebook_Post_01"
    range1 = PacketLengthRange("[50:55]")
    # handler = DirectoryHandler(filepath, range1, 32)
    # print(handler.getAllDumpFile())


if __name__ == '__main__':
    test1()
