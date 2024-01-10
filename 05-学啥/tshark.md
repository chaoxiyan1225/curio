# wireshark的命令行抓包版本
参考 [tshark命令行抓包](https://juejin.cn/post/6994232948618690591)

参数说明：
-i 设置抓包的网络接口，不设置则默认为第一个非自环接口。
-D 列出当前存在的网络接口。在不了解OS所控制的网络设备时，一般先用“tshark -D”查看网络接口的编号以供-i参数使用。
-f 设定抓包过滤表达式（capture filter expression）。抓包过滤表达式的写法雷同于tcpdump，可参考tcpdump man page的有关部分。
-s 设置每个抓包的大小，默认为65535，多于这个大小的数据将不会被程序记入内存、写入文件。（这个参数相当于tcpdump的-s，tcpdump默认抓包的大小仅为68）
-c 抓指定个包后终止
-a 终止条件 duration:NUM - stop after NUM seconds
          filesize:NUM - stop this file after NUM KB
          files:NUM - stop after NUM files
-w 设置raw数据的输出文件。这个参数不设置，tshark将会把解码结果输出到stdout。“-w-”表示把raw输出到stdout。如果要把解码结果输出到文件，使用重定向“>”而不要-w参数。 
-r 设置tshark分析的输入文件。tshark既可以抓取分析即时的网络流量，又可以分析dump在文件中的数据。-r不能是命名管道和标准输入。
-R 设置读取过滤表达式（read filter expression）。不符合此表达式的流量同样不会被写入文件。注意，读取（显示）过滤表达式的语法和底层相关的抓包过滤表达式语法不相同，它的语法表达要丰富得多，请参考http://www.ethereal.com/docs/dfref/和http://www.ethereal.com/docs/man-pages/ethereal-filter.4.html。类似于抓包过滤表达式，在命令行使用时最好将它们quote起来。-Y （显示）过滤。
-T 设置解码结果输出的格式，包括fileds,text,ps,psml和pdml，默认为text。
-E 配合-T使用，制定输出格式，分隔符等。
-t 设置解码结果的时间格式。“ad”表示带日期的绝对时间，“a”表示不带日期的绝对时间，“r”表示从第一个包到现在的相对时间，“d”表示两个相邻包之间的增量时间（delta）。
-q 设置安静的stdout输出（例如做统计时）
-z 设置统计参数。
-p 设置网络接口以非混合模式工作，即只关心和本机有关的流量。
-B 设置内核缓冲区大小，仅对windows有效。
-y 设置抓包的数据链路层协议，不设置则默认为-L找到的第一个协议，局域网一般是EN10MB等。
-L 列出本机支持的数据链路层协议，供-y参数使用。
-n 禁止所有地址名字解析（默认为允许所有）。
-N 启用某一层的地址名字解析。“m”代表MAC层，“n”代表网络层，“t”代表传输层，“C”代表当前异步DNS查找。如果-n和-N参数同时存在，-n将被忽略。如果-n和-N参数都不写，则默认打开所有地址名字解析。
-d 将指定的数据按有关协议解包输出。如要将tcp 8888端口的流量按http解包，应该写为“-d tcp.port==8888,http”。注意解包协议之间不能留空格。
-F 设置输出raw数据的格式，默认为libpcap。“tshark -F”会列出所有支持的raw格式。
**V 设置将解码结果的细节输出，否则解码结果仅显示一个packet一行的summary***
-x 设置在解码输出结果中，每个packet后面以HEX dump的方式显示具体数据。
-S 在向raw文件输出的同时，将解码结果打印到控制台。
-l 在处理每个包时即时刷新输出。
-X 扩展项。
-h 显示命令行帮助。
-v 显示tshark的版本信息。
-o 重载选项。

## 详细的过滤
在  -f 参数之后添加如下内容

port 53：抓取发到/来自端口53的UDP/TCP数据流（典型是DNS数据流）
not port 53：抓取除了发到/来自端口53以外的UDP/TCP数据流
port 80：抓取发到/来自端口80的UDP/TCP数据流（典型是HTTP数据流）
udp port 67：抓取发到/来自端口67的UDP数据流（典型是DHCP据流）
tcp port 21：抓取发到/来自端口21的TCP数据流（典型是FTP命令通道）
portrange 1-80：抓取发到/来自端口1-80的所有UDP/TCP数据流
tcp portrange 1-80：抓取发到/来自端口1-80的所有TCP数据流
ip broadcast：抓取广播报文
ip multicast：抓取多播报文
dst host ff02::1：抓取到IPv6多播地址所有主机的数据流
dst host ff02::2：抓取到IPv6多播地址所有路由器的数据流
net 10.3.0.0/16：抓取网络10.3.0.0上发到/来自所有主机的数据流(16表示长度)
net 10.3.0.0 mask 255.255.0.0：与之前的过滤结果相同
ip[2:2]==<number>：ip报文大小
ip[8]==<number>：TTL(Time to Live)值 
ip[9]==<number>：协议值
src host 10.1.1.1：抓取来自10.1.1.1的数据流 
dst host 10.1.1.1：抓取发到10.1.1.1的数据流
host 10.1.1.1：抓取发到/来自10.1.1.1的数据流 
ether dst 02:0A:42:23:41:AC：抓取发到02:0A:42:23:41:AC的数据流
not ether host 00:08:15:00:08:15：抓取除了发到/来自00:08:15:00:08:15以外的所有数据流 
ether broadcast或ether dst ff:ff:ff:ff:ff:ff：抓取广播报文
ether multicast：多播报文




