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
