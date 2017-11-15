# Computer_Networking

## Transport_Layer

### 概述
> 传输层在端系统中实现
>
> 为运行在不同主机上的进程之间提供了逻辑通信
>
> 与网络层的关系 
>
>> 网络层提供主机到主机的通信
>>
>> 运输层协议提供的报文受限制于底层网络层下协议
>>
>>> 时延保证与带宽保证依赖于网络层
>>>
>> 运输层协议也能提供某些服务而不依赖于底层网络层协议
>>
>>> 可靠数据传输，数据加密
>>>

### 多路复用和多路分解
> 含义
>
> UDP套接字由一个二元组来标识：目的IP，目的端口号
>
> TCP套接字由一个四元组来标识：本地IP，本地端口号，目的IP，目的端口号
> 
> 连接套接字与进程并非一一对应
> 
>> 当前流行做法：一个进程多个线程多个套接字
>>
> 持久HTTP：在整个连接持续的期间，只使用一个套接字
>
> 非持久HTTP：每一对请求响应都会创建一个TCP连接并随后关闭
>

### 无连接传输协议 用户数据报协议 UDP
> 概述
>
>> 在IP协议的基础上只增加了多路复用分解以及少量的差错检测功能
>>
>> 优点
>>
>>> 对于发送数据的应用层时间控制更为细化
>>>
>>> 无序连接的建立
>>>
>>> 无状态连接
>>>
>>> UDP报文首部overhead小，8字节
>>>
>> 使用UDP的应用可以实现可靠数据传输：通过在应用程序自身建立可靠性机制来完成
>>
>> UDP报文结构
>>
>> UDP校验和
>>
>>> 为什么在链路层拥有差错检测的情况下，UDP还要提供校验和？
>>>
>>> 思路：系统设计中的端到端原则
>>>

### 可靠数据传输原理
> 构造可靠数据传输协议
>
> 基于流水线技术的可靠传输协议
>
> Go-back-N (GBN)
>
>> GBN发送方必须响应三种类型的事件
>>
>>> 上层调用
>>>
>>> 收到一个ACK，GBN采用累计确认的方式，表明接收方正确接收N以前的所有分组。包含N。
>>>
>>> 超时事件，重新传送所有已经被发送但还没有被确认的分组。
>>> 
>> 接收方维护expectedseqnum
>>
>> 发送方维护窗口上下边界以及nextseqnum，以及最早的已被发送但未被确认的分组
>>
> 选择重传 Selective Resend (SR)
>
>> 发送方的事件与动作
>>
>> 接收方的事件与动作
>>
>> 窗口长度必须小于等于序号空间大小的一半
>>
> 一个问题：一个具有序号或者确认号的X的分组的旧副本可能重新出现
>
>> 实际应用的方法：假设存活时间
>>

### 面向连接的传输 Transmission Control Protocol TCP
> TCP连接
>
>> 概述
>>
>>> 面向连接:连接之前2个进程必须先握手
>>>
>>> 全双工
>>>
>>> 点对点
>>>
>>> 发送缓存
>>>
>>> MSS 最大报文段长度, 通常根据本地发送主机的MTU设置, 典型值为1460Bytes. 不包含TCP首部
>>>
>> 报文段结构
>>
>>> 源端口号，目的端口号
>>>
>>> 序号和确认号：实现可靠数据传输
>>>
>>>> 字节流上的序号
>>>>
>>>> 确认号是该主机期待接受的下一个字节的编号。累计确认
>>>>
>>>> TCP收到失序报文怎么办？TCP没有规定规则，实践中一般保留失序的字节
>>>>
>>>> 初始序号由TCP连接各方自由决定
>>>>
>>>> 即使报文段中没有数据，也应该添加序号字段。接下来的带有数据的序号应该是什么呢？
>>>>
>>> 接受窗口：流量控制
>>>
>>> 首部长度
>>>
>>> 选项字段，用于发送方与接收方协调MSS
>>>
>>> 6-bit的标志字段，RST，SYN，FIN，PSH，URG，ACK
>>>
>> RTT 往返时间的估计 p161
>>> 在某个时刻做一次sampleRTT测量而不是为每个发送的报文都做
>>>
>>> 不对已被重传的报文段计算sampleRTT
>>>
>> 实践原则
>>
>>> TCP使用确认和定时器提供可靠数据传输
>>>
>>> TCP使用流水线
>>>
>> 可靠数据传输
>>
>>> 一些有趣的情况 p165
>>>
>>> 超时间隔加倍
>>>
>>> 快速重传
>>>
>>> 与GBN，SR的关系
>>>
>>>> 与GBN有类似的地方
>>>>
>>>>> TCP发送方维护SendBase, NextSeqNum, CWND, RWND
>>>>>
>>>> 当丢失某分组时，TCP与GBN的差异 p167
>>>>
>>>> 另一种修改意见，选择确认，选择重传像SR
>>>>
>> 流量控制 p168
>>
>>> 作用：消除发送方使接收方缓存溢出的可能性
>>>
>>> 速度匹配服务
>>>
>>> 让发送方维护一个接收窗口的变量来提供流量控制。TCP是全双工,所以双方都维护一个接收窗口
>>>
>> 连接管理
>>
>>> 建立连接，三次握手
>>>
>>>> 客户端向服务器发送特殊的TCP报文段，不包含应用层数据，SYN设置为1.随机选择初始序号cilent_isn
>>>>
>>>> 服务器从数据包中提取出TCP SYN报文段。为TCP分配TCP缓存与变量。并向客户端发送SYN ACK 报文段。SYN设置为  1，确认号字段设置为client_isn+1.最后服务器选择自己的初始序号
>>>>
>>>> 收到SYN ACK报文段后。客户分配缓存与变量。客户想服务器发送另一个报文段，这一个报文段确认SYN ACK报文段。SYN设置为0.这一阶段可以携带客户到服务器的数据
>>>> 一旦完成以上三个步骤。一个TCP连接就建立完成了（SYN泛洪攻击)
>>>>
>>>> TCP为什么需要三次握手？
>>>>
>>> 拆除连接
>>>
>>>> 客户TCP向服务器发送特殊的TCP SEGMENT，FIN设置为1
>>>>
>>>> 服务器向客户发送ACK
>>>>
>>>> 服务器发送他自己的终止报文段，FIN设置为1
>>>>
>>>> 客户向服务器发送ACK
>>>>
>>>> 完成以上四个步骤，用于该连接的资源就完全被释放掉了
>>>>
>>> nmap的工作原理
>>>
>> 拥塞控制原理
>>
>>> 拥塞原因与代价
>>>
>>> 拥塞控制方法
>>>
>>>> 端到端的拥塞控制 TCP
>>>>
>>>> 网络辅助的拥塞控制 ATM ABR
>>>>
>> TCP拥塞控制AIMD （加性增长，乘性递减）
>>
>>> TCP的self-clocking p182
>>>
>>> 实践原则：TCP分岔：优化云服务的性能
>>>
>>> TCP 拥塞控制算法 有限状态自动机FSM见p184
>>>> 慢启动
>>>>
>>>>> 初始CWND设置为一个MSS的较小值
>>>>>
>>>>> 发送方对每一个确认报文增加一个MSS
>>>>>
>>>>> 何时结束？
>>>>>
>>>>>> 超时，CWND设置为1，重新慢启动。ssthresh设置为cwnd/2
>>>>>>
>>>>>> 到达或者超过ssthresh时，结束慢启动进入拥塞避免
>>>>>>
>>>>>> 检测到三个冗余ACK，TCP执行快速重传并进入快速恢复状态
>>>>>>
>>>> 拥塞避免
>>>>
>>>>> 每个RTT将CWND增加一个MSS
>>>>>
>>>>> 实现上述操作的方法：每个新的确认。给CWND增加MSS/CWND字节
>>>>> 何时结束
>>>>>
>>>>>> 超时、同慢启动状态的行为
>>>>>>
>>>>>> 检测到三个冗余ACK, ssthresh设置为CWND的一半。CWND设置为ssthresh+3MSS进入快速恢复状态
>>>>>>
>>>> 快速恢复
>>>>
>>>>> 每个冗余ACK，CWND增加一个MSS
>>>>>
>>>>> 何时结束
>>>>>
>>>>>> 当丢失报文段的ACK到达时，TCP将CWND设置为ssthresh，进入拥塞避免状态
>>>>>>
>>>>>> 当超时，执行如同慢启动的行为
>>>>>>
>>>>> 推荐但非必须
>>>>>
>>>>> Reno版本与Tahoe(早期)版本的不同 p185
>>>>>

## Application_Layer
