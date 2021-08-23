import getopt
import sys

from DirectoryHandler import DirectoryHandler
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
    filename = "App_Facebook_Post_01_PH3.pcapng"

    range1 = PacketLengthRange("[200:300]")
    firstmPackets = 10
    firstnBytes = 32
    packetFilter = PacketFilter(range1, firstmPackets, firstnBytes)

    context = ParserContext(filename, filepath, packetFilter)
    servicePayloadDict = context.parse()

    for k,v in servicePayloadDict.items():
        print("packet" + str(k) + ": " + v.hex())

def test2():
    filepath = r"C:\Users\a9241\Desktop\Learning materials\研究生\抓包任务20210611\FacebookCapture\App_Facebook_Post_01"
    range1 = PacketLengthRange("[50:55]")
    handler = DirectoryHandler(filepath, range1, 32)
    print(handler.getAllDumpFile())


if __name__ == '__main__':
    test1()
