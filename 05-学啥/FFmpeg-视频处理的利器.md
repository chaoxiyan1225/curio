FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。采用LGPL或GPL许可证。它提供了录制、转换以及流化音视频的完整解决方案。它包含了非常先进的音频/视频编解码库libavcodec，为了保证高可移植性和编解码质量，libavcodec里很多code都是从头开发的。

[三十分钟带你熟悉](https://zhuanlan.zhihu.com/p/89872960)

[使用指导文档](https://ffmpeg.xianwaizhiyin.net/base-ffmpeg/ffmpeg-mux.html)_

[linux下ffmpeg使用指导](https://itsfoss.com/ffmpeg/)

[中文指导](https://ffmpeg.github.net.cn/ffmpeg.html)


# 剔除视频中的水印：

FFmpeg 可以使用 maskfilter 滤镜来剔除视频中的水印。例如，以下命令可以去除视频中的水印，假设水印区域为 (x,y,w,h)：
ffmpeg -i input.mp4 -filter_complex "[0:v]delogo=x=x:y=y:w=w:h=h" -c:a copy output.mp4
其中，-filter_complex 表示复杂滤镜链，[0:v] 表示输入视频的视频流，delogo 表示使用 delogo 滤镜，x、y、w、h 分别表示水印区域的左上角坐标和宽高。这个命令会将 input.mp4 中的水印去除，并生成一个新的视频文件 output.mp4。

# 剔除视频中的马赛克

FFmpeg 可以使用 minterpolate 滤镜来剔除视频中的马赛克。例如，以下命令可以对 input.mp4 中的第 0 分钟到第 1 分钟的视频进行去马赛克处理：
ffmpeg -i input.mp4 -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:mb_size=8'" -ss 0 -t 60 -c:a copy output.mp4
其中，-filter:v 表示视频滤镜，minterpolate 表示使用 minterpolate 滤镜，mi_mode=mci、mc_mode=aobmc、mb_size=8 分别表示帧间插值算法、运动补偿算法和块大小。-ss 0 和 -t 60 表示从视频的第 0 秒开始取 60 秒的视频进行处理。这个命令会将 input.mp4 中的马赛克去除，并生成一个新的视频文件 output.mp4。

[通过ffmpeg把图片转换成视频](http://blog.360converter.com/archives/894)
[FFmpeg命令(一)、使用filter_complex命令拼接视频](https://blog.csdn.net/Gary__123456/article/details/88742705)
[FFmpeg 视频处理入门教程](http://www.ruanyifeng.com/blog/2020/01/ffmpeg.html)
[给新手的 20 多个 FFmpeg 命令示例]("https://zhuanlan.zhihu.com/p/67878761")
[FFmpeg命令行转码]("https://blog.csdn.net/Lyman_Ye/article/details/80305904")
[ffmpeg 翻译文档 (ffmpeg-all 包含重要组件]("https://www.bookstack.cn/read/other-doc-cn-ffmpeg/README.md")
[FFmpeg Filters Documentation]("http://ffmpeg.org/ffmpeg-filters.html#drawtext-1")
[FFmpeg命令行滤镜使用]("https://www.shangmayuan.com/a/46d1902c245842e586ddea9b.html")
[ffmpeg命令行使用nvidia CUDA scaling高速转分辨率转]("https://blog.csdn.net/n66040927/article/details/84525611"）
[FFmpeg—源码编译]("https://www.cnblogs.com/carle-09/p/11736390.html")
[FFmpeg常用命令]("https://www.jianshu.com/p/c56d5d79ce8b")
[Linux上的ffmpeg完全使用指南]("https://eyehere.net/2019/the-complete-guide-for-using-ffmpeg-in-linux/")
[视频和视频ie FFMPEG 硬件解码API介绍]("https://zhuanlan.zhihu.com/p/168240163")

文章目录
ffmpeg
install ffmpeg
debian install
简介
基础概念
容器(Container)
流(Stream)
帧(Frame)
编解码器(Codec)
复用/解复用(mux/demux)
帧率
码率
FFplay使用指南
FFplay是什么
FFplay 使用示例
通用选项
主要选项
高级选项
快捷键
参考资料
FFmpeg常用命令
常用命令
参考资料
格式转换
参考资料
FFmpeg是什么
FFmpeg使用方法
主要选项
视频选项
音频选项
高级选项
参考资料
FFprobe使用指南
FFprobe 是什么 ？
FFprobe 使用示例
主要选项
参考资料
FFmpeg推流到SRS
SRS安装
推流
拉流
参考资料
ffmpeg
install ffmpeg
debian install
编辑/etc/apt/sources.list加入    
deb http://www.deb-multimedia.org jessie main
apt update
apt-get install deb-multimedia-keyring
apt install ffmpeg
复制
简介
​ FFmpeg的名称来自MPEG视频编码标准，前面的“FF”代表“Fast Forward”，FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。可以轻易地实现多种视频格式之间的相互转换。包括如下几个部分：

libavformat：用于各种音视频封装格式的生成和解析，包括获取解码所需信息以生成解码上下文结构和读取音视频帧等功能，包含demuxers和muxer库。
libavcodec：用于各种类型声音/图像编解码。
libavutil：包含一些公共的工具函数。
libswscale：用于视频场景比例缩放、色彩映射转换。
libpostproc：用于后期效果处理。
ffmpeg：是一个命令行工具，用来对视频文件转换格式，也支持对电视卡实时编码。
ffsever：是一个HTTP多媒体实时广播流服务器，支持时光平移。
ffplay：是一个简单的播放器，使用ffmpeg 库解析和解码，通过SDL显示。
ffprobe：收集多媒体文件或流的信息，并以人和机器可读的方式输出。
基础概念
容器(Container)
​ 一种文件格式，比如flv，mkv等。包含下面5种流以及文件头信息。

流(Stream)
​ 一种视频数据信息的传输方式，5种流：音频，视频，字幕，附件，数据。

帧(Frame)
​ 帧代表一幅静止的图像，分为I帧，P帧，B帧。

编解码器(Codec)
​ 是对视频进行压缩或者解压缩，CODEC = COde（编码） +DECode（解码）。

复用/解复用(mux/demux)
​ 把不同的流按照某种容器的规则放入容器，这种行为叫做复用（mux）。

​ 把不同的流从某种容器中解析出来，这种行为叫做解复用(demux)。

帧率
​ 帧率也叫帧频率，帧率是视频文件中每一秒的帧数，肉眼想看到连续移动图像至少需要15帧。

码率
​ 比特率(也叫码率，数据率)是一个确定整体视频/音频质量的参数，秒为单位处理的字节数，码率和视频质量成正比，在视频文件中中比特率用bps来表达。

FFplay使用指南
FFplay是什么
FFplay 使用示例
通用选项
'-L'    显示 license
'-h, -?, -help, --help [arg]' 打印帮助信息；可以指定一个参数 arg ，如果不指定，只打印基本选项
    可选的 arg 选项：
    'long'    除基本选项外，还将打印高级选项
    'full'    打印一个完整的选项列表，包含 encoders, decoders, demuxers, muxers, filters 等的共享以及私有选项
    'decoder=decoder_name'    打印名称为 "decoder_name" 的解码器的详细信息
    'encoder=encoder_name'    打印名称为 "encoder_name" 的编码器的详细信息
    'demuxer=demuxer_name'    打印名称为 "demuxer_name" 的 demuxer 的详细信息
    'muxer=muxer_name'        打印名称为 "muxer_name" 的 muxer 的详细信息
    'filter=filter_name'      打印名称为 "filter_name" 的过滤器的详细信息
	
'-version'     显示版本信息
'-formats'     显示有效的格式
'-codecs'      显示 libavcodec 已知的所有编解码器
'-decoders'    显示有效的解码器
'-encoders'    显示有效的编码器
'-bsfs'        显示有效的比特流过滤器
'-protocols'   显示有效的协议
'-filters'     显示 libavfilter 有效的过滤器
'-pix_fmts'    显示有效的像素格式 
'-sample_fmts' 显示有效的采样格式
'-layouts'     显示通道名称以及标准通道布局
'-colors'      显示认可的颜色名称
'-hide_banner' 禁止打印欢迎语；也就是禁止默认会显示的版权信息、编译选项以及库版本信息等
复制
主要选项
'-x width'        强制以 "width" 宽度显示
'-y height'       强制以 "height" 高度显示
'-an'	          禁止音频
'-vn'             禁止视频
'-ss pos'         跳转到指定的位置(秒)
'-t duration'     播放 "duration" 秒音/视频
'-bytes'          按字节跳转
'-nodisp'         禁止图像显示(只输出音频)
'-f fmt'          强制使用 "fmt" 格式
'-window_title title'  设置窗口标题(默认为输入文件名)
'-loop number'    循环播放 "number" 次(0将一直循环)
'-showmode mode'  设置显示模式
    可选的 mode ：
    '0, video'    显示视频
    '1, waves'    显示音频波形
    '2, rdft'     显示音频频带
    默认值为 'video'，你可以在播放进行时，按 "w" 键在这几种模式间切换

'-i input_file'   指定输入文件
复制
高级选项
'-sync type'          设置主时钟为音频、视频、或者外部。默认为音频。主时钟用来进行音视频同步
'-threads count'      设置线程个数
'-autoexit'           播放完成后自动退出
'-exitonkeydown'      任意键按下时退出
'-exitonmousedown'    任意鼠标按键按下时退出
'-acodec codec_name'  强制指定音频解码器为 "codec_name"
'-vcodec codec_name'  强制指定视频解码器为 "codec_name"
'-scodec codec_name'  强制指定字幕解码器为 "codec_name"
复制
快捷键
'q, ESC'            退出
'f'                 全屏
'p, SPC'            暂停
'w'                 切换显示模式(视频/音频波形/音频频带)
's'                 步进到下一帧
'left/right'        快退/快进 10 秒
'down/up'           快退/快进 1 分钟
'page down/page up' 跳转到前一章/下一章(如果没有章节，快退/快进 10 分钟)
'mouse click'       跳转到鼠标点击的位置(根据鼠标在显示窗口点击的位置计算百分比)
复制
参考资料
《FFplay使用指南》
FFmpeg常用命令
常用命令
1.分离视频音频流

ffmpeg -i input_file -vcodec copy -an output_file_video　　//分离视频流
ffmpeg -i input_file -acodec copy -vn output_file_audio　　//分离音频流
复制
2.视频解复用

ffmpeg –i test.mp4 –vcodec copy –an –f m4v test.264
ffmpeg –i test.avi –vcodec copy –an –f m4v test.264
复制
3.视频转码

ffmpeg –i test.mp4 –vcodec h264 –s 352*278 –an –f m4v test.264              //转码为码流原始文件
ffmpeg –i test.mp4 –vcodec h264 –bf 0 –g 25 –s 352*278 –an –f m4v test.264  //转码为码流原始文件
ffmpeg –i test.avi -vcodec mpeg4 –vtag xvid –qsame test_xvid.avi            //转码为封装文件
//-bf B帧数目控制，-g 关键帧间隔控制，-s 分辨率控制
复制
4.视频封装

ffmpeg –i video_file –i audio_file –vcodec copy –acodec copy output_file
复制
5.视频剪切

ffmpeg –i test.avi –r 1 –f image2 image-%3d.jpeg        //提取图片
ffmpeg -ss 0:1:30 -t 0:0:20 -i input.avi -vcodec copy -acodec copy output.avi    //剪切视频
//-r 提取图像的频率，-ss 开始时间，-t 持续时间
复制
6.视频录制

ffmpeg –i rtsp://192.168.3.205:5555/test –vcodec copy out.avi
复制
参考资料
FFmpeg常用命令
格式转换
# 将mp4文件转换为flv
ffmpeg -i IU.mp4 -acodec aac test.flv   
复制
-i "1.avi"		# 输入文件是
-title "Test" 	# 影片的标题
-s 368x208 		# 输出的分辨率为368x208，注意片源一定要是16:9的不然会变形
-r 29.97		# 帧数
-b 1500			# 视频数据流量，用-b xxxx的指令则使用固定码率,还可以用动态码率如：-qscale 4和-qscale 6，4的质量比6高
-acodec 		# aac音频编码用AAC
-ac 			# 声道数1或2
-ar 24000		# 声音的采样频率
-ab 128			# 音频数据流量，一般选择32、64、96、128
-vol 200		# 200%的音量，自己改
-ab bitrate     # 设置音频码率
-ar freq 		# 设置音频采样率
-ss 			# 指定时间点开始转换任务(time_off set the start time offset),-ss后跟的时间单位为秒 .
-s 320x240 		# 指定分辨率   
-bitexact 		# 使用标准比特率 
-vcodec xvid    # 使用xvid压缩
复制
参考资料
FFMpeg 常用命令格式转换和视频合成
使用ffmpeg转换文件格式
FFmpeg是什么
​ ffmpeg(命令行工具) 是一个快速的音视频转换工具。

FFmpeg使用方法
​ ffmpeg [全局选项] {[输入文件选项] -i ‘输入文件’} … {[输出文件选项] ‘输出文件’}

主要选项
‘-f fmt (input/output)’ 
	强制输入或输出文件格式。通常，输入文件的格式是自动检测的，
	输出文件的格式是通过文件扩展名来进行猜测的，所有该选项大
	多数时候不需要。
‘-i filename (input)’ 
	输入文件名
‘-y (global)’ 
	覆盖输出文件而不询问
‘-n (global)’ 
	不覆盖输出文件，如果一个给定的输出文件已经存在，则立即
	退出
‘-c[:stream_specifier] codec (input/output,per-stream)’
‘-codec[:stream_specifier] codec (input/output,per-stream)’
	为一个或多个流选择一个编码器(当使用在一个输出文件之前时)
	或者一个解码器(当使用在一个输入文件之前时)。codec 是一个
	编码器/解码器名称或者一个特定值“copy”(只适用输出)。
‘-t duration (output)’ 
	当到达 duration 时，停止写输出。
	duration 可以是一个数字(秒)，或者使用hh:mm:ss[.xxx]形式。
	-to 和 -t 是互斥的，-t 优先级更高。
‘-to position (output)’ 
	在 position 处停止写输出。
	duration 可以是一个数字(秒)，或者使用hh:mm:ss[.xxx]形式。
	-to 和 -t 是互斥的，-t 优先级更高。
‘-fs limit_size (output)’
	设置文件大小限制，以字节表示
‘-ss position (input/output)’
	当作为输入选项时(在 -i 之前)，在输入文件中跳转到 position。
	需要注意的是，在大多数格式中，不太可能精确的跳转，因此，
	ffmpeg 将跳转到 position 之前最接近的位置。当进行转码
	并且 ‘-accurate_seek’ 打开时(默认)，位于跳转点和 position 
	之间的额外部分将被解码并且丢弃。当做流拷贝或者当使用
	‘-noaccurate_seek’时，它将被保留下来。
	当作为输出选项时(在输出文件名前)，解码但是丢弃输入，直到
	时间戳到达 position。
	position 可以是秒或者 hh:mm:ss[.xxx] 形式
‘-itsoffset offset (input)’
	设置输入时间偏移。 offset 将被添加到输入文件的时间戳。指定
	一个正偏移，意味着相应的流将被延时指定时间。
‘-timestamp date (output)’
	在容器中设置录音时间戳
‘-metadata[:metadata_specifier] key=value (output,per-metadata)’
	设置metadata key/value对
‘-target type (output)’
	指定目标文件类型(vcd, svcd, dvd, dv, dv50)。
	type 可以带有 pal-, ntsc- 或 film- 前缀，以使用相应的标准。
	所有的格式选项(bitrate, codecs, buffer sizes)将自动设定。
‘-dframes number (output)’
	设置要录制数据帧的个数。这是 -frames:d 的别名
‘-frames[:stream_specifier] framecount (output,per-stream)’  
	framecount 帧以后，停止写流。
‘-q[:stream_specifier] q (output,per-stream)’
‘-qscale[:stream_specifier] q (output,per-stream)’ 
	使用固定质量范围(VBR)。
‘-filter[:stream_specifier] filtergraph (output,per-stream)’
	创建filtergraph 指定的过滤图，并使用它来过滤流。
‘-filter_script[:stream_specifier] filename (output,per-stream)’
	该选项与‘-filter’相似，唯一的不同是，它的参数是一个存放
	过滤图的文件的名称。
‘-pre[:stream_specifier] preset_name (output,per-stream)’ 
	指定匹配流的预设
‘-stats (global)’
	打印编码进程/统计信息。默认打开，可以使用 -nostats 禁用。
‘-stdin’ 
	开启标准输入交互。默认打开，除非标准输入作为一个输入。
	可以使用 -nostdin 禁止。
‘-debug_ts (global)’
	打印时间戳信息。默认关闭。
‘-attach filename (output)’
	添加一个附件到输出文件中
‘-dump_attachment[:stream_specifier] filename (input,per-stream)’ 
	提取匹配的附件流到filename指定的文件中。
复制
视频选项
‘-vframes number (output)’
	设置录制视频帧的个数。这是 -frames:v 的别名
‘-r[:stream_specifier] fps (input/output,per-stream)’
	设置帧率(Hz 值， 分数或缩写)
‘-s[:stream_specifier] size (input/output,per-stream)’
	设置帧大小。格式为 ‘wxh’ (默认与源相同)
‘-aspect[:stream_specifier] aspect (output,per-stream)’
	设置视频显示长宽比
‘-vn (output)’
	禁止视频录制
‘-vcodec codec (output)’
	设置视频 codec。这是 -codec:v 的别名
‘-pass[:stream_specifier] n (output,per-stream)’
	选择pass number (1 or 2)。用来进行双行程视频编码。
‘-passlogfile[:stream_specifier] prefix (output,per-stream)’
	设置 two-pass 日志文件名前缀，默认为“ffmpeg2pass”。
‘-vf filtergraph (output)’
	创建 filtergraph 指定的过滤图，并使用它来过滤流。
‘-pix_fmt[:stream_specifier] format (input/output,per-stream)’
	设置像素格式。
‘-sws_flags flags (input/output)’
	设置软缩放标志
‘-vdt n’
	丢弃阈值
‘-psnr’
	计算压缩帧的 PSNR 
‘-vstats’
	复制视频编码统计信息到‘vstats_HHMMSS.log’
‘-vstats_file file’
	复制视频编码统计信息到 file
‘-force_key_frames[:stream_specifier] time[,time...] (output,per-stream)’
‘-force_key_frames[:stream_specifier] expr:expr (output,per-stream)’
	在指定的时间戳强制关键帧
‘-copyinkf[:stream_specifier] (output,per-stream)’
	当进行流拷贝时，同时拷贝开头的非关键帧
‘-hwaccel[:stream_specifier] hwaccel (input,per-stream)’
	使用硬件加速来解码匹配的流
‘-hwaccel_device[:stream_specifier] hwaccel_device (input,per-stream)’
	选择硬件加速所使用的设备。该选项只有‘-hwaccel’同时指定时才有意义。
复制
音频选项
‘-aframes number (output)’
	设置录制音频帧的个数。这是 -frames:a 的别名
‘-ar[:stream_specifier] freq (input/output,per-stream)’
	设置音频采样率。
‘-aq q (output)’
	设置音频质量。这是 -q:a 的别名
‘-ac[:stream_specifier] channels (input/output,per-stream)’
	设置音频通道数。
‘-an (output)’
	禁止音频录制
‘-acodec codec (input/output)’
	设置音频codec。这是-codec:a的别名
‘-sample_fmt[:stream_specifier] sample_fmt (output,per-stream)’
	设置音频采样格式
‘-af filtergraph (output)’
	创建filtergraph 所指定的过滤图，并使用它来过滤流
复制
高级选项
‘-map [-]input_file_id[:stream_specifier][,sync_file_id[:stream_specifier]] | [linklabel] (output)’
	指定一个或多个流作为输出文件的源。
	命令行中的第一个 -map 选项，指定输出流0的源，
	第二个 -map 选项，指定输出流1的源，等等。
‘-map_channel [input_file_id.stream_specifier.channel_id|-1][:output_file_id.stream_specifier]’
	将一个给定输入的音频通道映射到一个输出。
‘-map_metadata[:metadata_spec_out] infile[:metadata_spec_in] (output,per-metadata)’
	设置下一个输出文件的 metadata 信息。
‘-map_chapters input_file_index (output)’
	从索引号为 input_file_index 的输入文件中拷贝章节到下一个输出文件中。
‘-timelimit duration (global)’
	ffmpeg 运行 duration 秒后推出
‘-dump (global)’
	将每一个输入包复制到标准输出
‘-hex (global)’
	复制包时，同时复制负载
‘-re (input)’
	以本地帧率读取数据。主要用来模拟一个采集设备，
	或者实时输入流(例如：当从一个文件读取时).
‘-vsync parameter’
	视频同步方法
‘-async samples_per_second’
	音频同步方法
‘-shortest (output)’
	当最短的输入流结束时，终止编码
‘-muxdelay seconds (input)’
	设置最大解封装-解码延时
‘-muxpreload seconds (input)’
	设置初始解封装-解码延时
‘-streamid output-stream-index:new-value (output)’
	为一个输出流分配一个新的stream-id。
‘-bsf[:stream_specifier] bitstream_filters (output,per-stream)’
	为匹配的流设置比特流过滤器
‘-filter_complex filtergraph (global)’
	定义一个复杂的过滤图
‘-lavfi filtergraph (global)’
	定义一个复杂的过滤图。相当于‘-filter_complex’
‘-filter_complex_script filename (global)’
   该选项类似于‘-filter_complex’，唯一的不同是
   它的参数是一个定义过滤图的文件的文件名
‘-accurate_seek (input)’
   打开或禁止在输入文件中的精确跳转。默认打开。
复制
参考资料
FFmpeg 使用指南
FFprobe使用指南
FFprobe 是什么 ？
​ ffprobe 是一个多媒体流分析工具。它从多媒体流中收集信息，并且以人类和机器可读的形式打印出来。它可以用来检测多媒体流的容器类型，以及每一个多媒体流的格式和类型。它可以作为一个独立的应用来使用，也可以结合文本过滤器执行更复杂的处理。

FFprobe 使用示例
主要选项
‘-f format’    强制使用的格式  
‘-unit’        显示值的单位  
‘-prefix’      显示的值使用标准国际单位制词头  
‘-byte_binary_prefix’ 对字节值强制使用二进制前缀  
‘-sexagesimal’ 时间值使用六十进位的格式 HH:MM:SS.MICROSECONDS  
‘-pretty’      美化显示值的格式。它相当于 "-unit -prefix -byte_binary_prefix -sexagesimal"  
‘-of, -print_format writer_name[=writer_options]’   
              设置输出打印格式。writer_name 指定打印程序 (writer) 的名称，writer_options   
              指定传递给 writer 的选项。例如：将输出打印为 JSON 格式：-print_format json   
‘-select_streams stream_specifier’   
              只选择 stream_specifier 指定的流。该选项只影响那些与流相关的选项  
              (例如：show_streams, show_packets, 等)。  
              举例：只显示音频流，使用命令：  
                ffprobe -show_streams -select_streams a INPUT  
‘-show_data’ 显示有效载荷数据，以十六进制和ASCII转储。与 ‘-show_packets’ 结合使用，它将   
              dump 包数据；与 ‘-show_streams’ 结合使用，它将 dump codec 附加数据。  
‘-show_error’    显示探测输入文件时的错误信息  
‘-show_format’   显示输入多媒体流的容器格式信息  
‘-show_packets’  显示输入多媒体流中每一个包的信息  
‘-show_frames’   显示输入多媒体流中的每一帧以及字幕的信息  
‘-show_streams’  显示输入多媒体流中每一个流的信息  
‘-show_programs’ 显示输入多媒体流中程序以及它们的流的信息  
‘-show_chapters’ 显示格式中存储的章节信息  
‘-count_frames’  计算每一个流中的帧数，在相应的段中进行显示  
‘-count_packets’ 计算每一个流中的包数，在相应的段中进行显示  
‘-show_program_version’   显示程序版本及配置相关信息  
‘-show_library_versions’  显示库版本相关信息  
‘-show_versions’          显示程序和库版本相关信息。相当于同时设置‘-show_program_version’ 和   
                          ‘-show_library_versions’  
‘-i input_file’           指定输入文件  
复制
参考资料
FFprobe使用指南
FFmpeg推流到SRS
SRS安装
unzip SRS-CentOS6-x86_64-2.0.243.zip
cd SRS-CentOS6-x86_64-2.0.243/
bash   INSTALL 
/etc/init.d/srs start
复制
推流
ffmpeg -re -i "/root/test.flv" -vcodec copy -acodec copy -f flv rtmp://172.17.229.3/live/test001 

ffmpeg -re -i 20190314.mp4 -c copy -f flv rtmp://172.17.229.3/live/test001
# -r 以本地帧频读数据，主要用于模拟捕获设备。
# 表示ffmpeg将按照帧率发送数据，不会按照最高的效率发送
复制
拉流
ffmpeg -i rtmp://server/live/streamName -c copy dump.flv
复制





