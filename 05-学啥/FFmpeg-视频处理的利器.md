FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。采用LGPL或GPL许可证。它提供了录制、转换以及流化音视频的完整解决方案。它包含了非常先进的音频/视频编解码库libavcodec，为了保证高可移植性和编解码质量，libavcodec里很多code都是从头开发的。

[三十分钟带你熟悉](https://zhuanlan.zhihu.com/p/89872960)

[使用指导文档](https://ffmpeg.xianwaizhiyin.net/base-ffmpeg/ffmpeg-mux.html)_

https://itsfoss.com/ffmpeg/


# 剔除视频中的水印：

FFmpeg 可以使用 maskfilter 滤镜来剔除视频中的水印。例如，以下命令可以去除视频中的水印，假设水印区域为 (x,y,w,h)：
ffmpeg -i input.mp4 -filter_complex "[0:v]delogo=x=x:y=y:w=w:h=h" -c:a copy output.mp4
其中，-filter_complex 表示复杂滤镜链，[0:v] 表示输入视频的视频流，delogo 表示使用 delogo 滤镜，x、y、w、h 分别表示水印区域的左上角坐标和宽高。这个命令会将 input.mp4 中的水印去除，并生成一个新的视频文件 output.mp4。

# 剔除视频中的马赛克

FFmpeg 可以使用 minterpolate 滤镜来剔除视频中的马赛克。例如，以下命令可以对 input.mp4 中的第 0 分钟到第 1 分钟的视频进行去马赛克处理：
ffmpeg -i input.mp4 -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:mb_size=8'" -ss 0 -t 60 -c:a copy output.mp4
其中，-filter:v 表示视频滤镜，minterpolate 表示使用 minterpolate 滤镜，mi_mode=mci、mc_mode=aobmc、mb_size=8 分别表示帧间插值算法、运动补偿算法和块大小。-ss 0 和 -t 60 表示从视频的第 0 秒开始取 60 秒的视频进行处理。这个命令会将 input.mp4 中的马赛克去除，并生成一个新的视频文件 output.mp4。

[通过ffmpeg把图片转换成视频]("http://blog.360converter.com/archives/894")
[FFmpeg命令(一)、使用filter_complex命令拼接视频]("https://blog.csdn.net/Gary__123456/article/details/88742705")
[FFmpeg 视频处理入门教程]("http://www.ruanyifeng.com/blog/2020/01/ffmpeg.html")
[给新手的 20 多个 FFmpeg 命令示例]("https://zhuanlan.zhihu.com/p/67878761")
[FFmpeg命令行转码]("https://blog.csdn.net/Lyman_Ye/article/details/80305904")
[ffmpeg 翻译文档 (ffmpeg-all 包含重要组件]("https://www.bookstack.cn/read/other-doc-cn-ffmpeg/README.md")
[FFmpeg Filters Documentation]("http://ffmpeg.org/ffmpeg-filters.html#drawtext-1")

[FFmpeg命令行滤镜使用]("https://www.shangmayuan.com/a/46d1902c245842e586ddea9b.html")

[ffmpeg命令行使用nvidia CUDA scaling高速转分辨率转码(libnpp)]("https://blog.csdn.net/n66040927/article/details/84525611"）
[FFmpeg—源码编译]("https://www.cnblogs.com/carle-09/p/11736390.html")
[FFmpeg常用命令]("https://www.jianshu.com/p/c56d5d79ce8b")
[Linux上的ffmpeg完全使用指南]("https://eyehere.net/2019/the-complete-guide-for-using-ffmpeg-in-linux/")
[视频和视频帧&#xff1a;FFMPEG 硬件解码API介绍]("https://zhuanlan.zhihu.com/p/168240163") )


