from ParserContext import ParserContext

if __name__ == '__main__':
    filepath = r"C:\Users\a9241\Desktop\Learning materials\研究生\抓包任务20210611\FacebookCapture\App_Facebook_Post_01"
    filename = "App_Facebook_Post_01_PH5.pcapng"
    context = ParserContext(filename, filepath)
    packetDataList = context.parse()

    pass