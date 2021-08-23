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

Len：离线数据长度：网络中实际数据帧的长度，一般不小于CapLen，多数情况下和CapLen数值相等。（例如，实际上有一个包长度是1500 bytes（Len=1500），但是因为在Global Header(即Pcap Header)的SnapLen=1300有限制，所以只能抓取这个包的前1300个字节，这个时候，CapLen = 1300 ）



## 5. Packet Data

Packet是链路层的数据帧，长度就是Packet Header中定义的Caplen值，所以每个Packet Header后面都跟着Caplen长度的Packet Data。也就是说pcap文件并没有规定捕获的数据帧之间有什么间隔字符串。Packet数据帧部分的格式就是标准的网络协议格式了。


## 参考：

1. https://blog.csdn.net/ytx2014214081/article/details/80112277

2. https://www.bbsmax.com/A/nAJvAZM8zr/





# pcapng文件解析

## 1. pcapng简介：

pcap next generation，pcap下一代转储文件格式，简单来说就是pcap文件的升级版。

pcapng文件追求以下三个目标：

- 可扩展性：除了一些常见的功能，第三方应该能够在文件中嵌入丰富的信息，无法理解这些信息的工具可以直接忽略它。
- 可移植性：一个捕捉跟踪必须包含读取时所需要的所有信息，而不依赖于捕获数据时的网络、硬件和操作系统。 
- 合并/附加数据：应该可以在给定文件的末尾添加数据，并将得到的文件仍然必须是可读的。 



## 2. pcapng文件格式

### 2.1 块结构

一个pcapng文件由各种**Block(块)**组成，所有Block都符合以下格式：

![img](C:\Users\a9241\Desktop\Learning materials\typora-user-images\Block Format.jpg)

每个字段含义如下：

1. Block Type: 块类型，不同的块有不同的类型值。
2. Block Total Length：当前块的**总长度**，每个块包含该字段两次。
3. Block Body：块内容，变长，但必须是**4字节对齐**的。



### 2.2 块类型

目前主要分为四类。

#### 2.2.1 **强制性块(MANDATORY blocks)**

强制性块必须在每个文件中出现至少一次，强制性块有以下两个:

- 节头块(Section Header Block，SHB)：它定义了捕获文件的最重要的特征。 
- 接口描述块(Interface Description Block，IDB) ：它定义了用于捕获流量的接口的最重要的特征。 



#### 2.2.2 **可选块(OPTIONAL blocks)**

可选块表示可以出现在文件中，也可以不存在。有以下四个：

- 增强分组块(Enhanced Packet Block, EPB)：它包含一个捕获数据包，或它的一部分，代表了原有的分组块(Packet Block)的演进。 
- 简单分组块(Simple Packet Block, SPB) ：它包含一个捕获数据包，或它的一部分，以及很少的关于数据包描述信息。
- 名称解析块(Name Resolution Block, NRB)：它定义由存在于数据包转储和规范名称的对应数字地址的映射。 
- 接口统计块(Interface Statistics Block, ISB)：它定义了如何存储一些统计数据（例如分组丢弃，等等），它对于了解数据包捕获的条件是有用的。



#### 2.2.3 **已过时块(OBSOLETE blocks)**

不应该出现在新写入的文件（但在这里留下供参考）： 

- 分组块(Packet Block)：它包含单个捕获分组，或它的一部分。它应该被视为过时的，由增强分组块取代。 

    

#### 2.2.4 **实验块(EXPERIMENTAL blocks)**

实验块被认为是有意义的，但作者认为他们应该在被定义以前有更深入的讨论： 

- Alternative Packet Blocks替代性包块 
- Compression Block压缩块 
- Encryption Block加密块 
- Fixed Length Block固定长度块 
- Directory Block目录块 
- Traffic Statistics and Monitoring Blocks流量统计和监控模块 
- Event/Security Blocks事件/安全模块 



### 2.3 文件布局

一个pcapng文件必须包含节头块，并且在一个捕获文件中可以存在多个节头块（这通常是文件拼接的结果）。下文均以某一简单pcapng文件为例：

一个经典的pcapng文件布局结构如下图所示，由一个节头块和接口描述块以及若干个增强分组块构成。

![img](C:\Users\a9241\Desktop\Learning materials\typora-user-images\Classical Format.jpg)

> 也存在其他布局，但不在本文讨论范围内。



## 3. 节头块(Section Header Block)

