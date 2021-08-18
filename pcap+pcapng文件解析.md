# pcap文件解析

## 1. pcap简介：

pcap文件是一种常用的数据报存储文件，这种文件可以保存我们所抓到的报文。它有这固定的存储格式，通过notepad++中的插件Hex-Editor我们可以观察其中的16进制数据，从而来进行pcap文件的分析。



## 2. Pcap文件格式：

![pcap文件格式](C:\Users\a9241\Desktop\Learning materials\typora-user-images\pcap文件格式.jpg)

pcap文件格式如图所示：

1. 以24字节的Pcap Header开头

2. 随后跟上每一个报文的相关信息

    - Packet Header：记录报文信息

    - Packet Data：记录报文数据

        

## 3. pcap Header

![Pcap Header](C:\Users\a9241\Desktop\Learning materials\typora-user-images\Pcap Header.jpg)

```C
// pcap.h文件中定义如下
struct pcap_file_header
{
    bpf_u_int32   magic;
    u_short       version_major;
    u_short       version_minor;
    bpf_int32     thiszone;
    bpf_u_int32   sigfigs;
    bpf_u_int32   snaplen;
    bpf_u_int32   linktype;
};
```

![image-20210818225527834](C:\Users\a9241\Desktop\Learning materials\typora-user-images\image-20210818225527834.png)



**字段说明：**

pcap Header占用24个字节，其中各字段含义如下：

1. Magic：标识文件开头，可以存在两个值（以字节顺序为例），

    - "\xd4\xc3\xb2\xa1"：表示小端模式(目前大部分计算机都为小端模式)。

        > 本文以该情况为例，下文中所有数字均以转换后的16进制数为例。

    - "\xa1\xb2\xc3\xd4"：表示大端模式。

2. Major：当前文件的主要版本号，一般为0x0200

3. Minor：当前文件的次要版本号，一般为0x0400

4. ThisZone：当地的标准时间，如果用的是GMT则全零，一般全0。

5. SigFigs：时间戳精度，一般全0。

6. SnapLen：最大的存储长度，设置所抓获的数据包的最大长度。

7. LinkType： 链路类型。解析数据包首先要判断它的LinkType，所以这个值很重要。一般的值为1，即以太网。

    > 常用的LinkType（链路类型）：
    >
    >    0              BSD loopback devices, except for later OpenBSD
    >
    >    1              Ethernet, and Linux loopback devices
    >
    >    6              802.5  Token Ring
    >
    >    7              ARCnet
    >
    >    8              SLIP
    >
    >    9               PPP
    >
    >    10             FDDI
    >
    >    100            LLC/SNAP-encapsulated  ATM 
    >
    >    101            "raw IP", with no link
    >
    >    102             BSD/OS  SLIP
    >
    >    103             BSD/OS  PPP
    >
    >    104             Cisco  HDLC
    >
    >    105             802.11
    >
    >    108             later OpenBSD loopback devices (with the AF_value in network byte order)
    >
    >    113             special  Linux  "cooked"  capture
    >
    >    114             LocalTalk



## 4. Packet Header

![Pcaket Header](C:\Users\a9241\Desktop\Learning materials\typora-user-images\Pcaket Header.jpg)

以抓到的某一报文为例：

![image-20210818230003615](C:\Users\a9241\Desktop\Learning materials\typora-user-images\image-20210818230003615.png)



**字段说明（每个字段均为4B）：**

Timestamp：时间戳高位，精确到seconds（值是自从January 1, 1970 00:00:00 GMT以来的秒数来记）

Timestamp：时间戳低位，精确到microseconds （数据包被捕获时候的微秒（microseconds）数，是自ts-sec的偏移量）

CapLen：当前数据区(Packet Data部分)的长度，即抓取到的数据帧长度，由此可以得到下一个数据帧的位置。

Len：离线数据长度**：**网络中实际数据帧的长度，一般不大于CapLen，多数情况下和CapLen数值相等。（例如，实际上有一个包长度是1500 bytes（L*en*=1500），但是因为在Global Header(即Pcap Header)的SnapLen=1300有限制，所以只能抓取这个包的前1300个字节，这个时候，CapLen = 1300 ）



## 5. Packet Data

Packet是链路层的数据帧，长度就是Packet Header中定义的Caplen值，所以每个Packet Header后面都跟着Caplen长度的Packet Data。也就是说pcap文件并没有规定捕获的数据帧之间有什么间隔字符串。Packet数据帧部分的格式就是标准的网络协议格式了。


# 参考：

1. https://blog.csdn.net/ytx2014214081/article/details/80112277

2. https://www.bbsmax.com/A/nAJvAZM8zr/