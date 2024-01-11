# 架构图  
   **juiceFS**



   **jindoFS** <br>
               
   ![架构图](https://static1.juicefs.com/images/arch_o6akMdB.original.png)


# 架构对比分析：

1. OSS-HDFS（JindoFS ）有集中式的中心服务，把元数据存储引擎（RocksDB）和元数据管理功能全部封装在服务端，用户开箱即用，JindoFS 客户端是轻量级瘦客户端，直接调用服务端暴露提供的 API。
2. JuiceFS 没有集中式中心服务，直接暴露元数据存储引擎（Redis），所有文件目录树和元数据管理逻辑都是在客户端，属于胖客户端。
3. 在存储 IO 上面，两个系统没有本质区别，都是客户端直接读写 OSS/S3。
   
# 性能影响对比分析：

1. JindoFS 在 rename、delete、du/count 上面显著领先于 JuiceFS。对于千万级文件数超大目录，即将上线的版本，du/count 可实现秒级算出。<br>
2. JuiceFS 在 open、create 上显著优于 JindoFS。JindoFS 在 open、create 操作上还有很大优化空间，目前较大性能开销主要花在 logging 特别是审计日志上面，而为了企业级安全考虑，审计日志是强制的，这方面的优化在进行中。JuiceFS 在性能上面受限于 Redis，优化空间有限；JindoFS 目前在用 Raft + RocksDB，后续会基于盘古飞天的 ArkDB 技术，有望大幅提升元数据服务性能。<br>
3. 两个系统在 IO 上面基本持平，JuiceFS 略优。<br>
   
# 系统影响对比分析：

1. JindoFS 是集中式的，因此可以在服务端实现各种开箱即用的企业级特性，包括但不限于：<br>
    a. 回收站等数据保护能力<br>
    b. 分层存储、归档/解冻能力，大幅降低存储成本<br>
    c. 权限集中管理和实施，审计日志支持<br>
    d. 对象协议支持<br>
    e. 近实时的元数据统计分析和异常监测能力<br>
    f. 服务后台平滑升级，优化随时上线，客户端无须升级<br>
    g. HDFS RPC 和 WebHDFS 协议无缝支持<br>
    h. HDFS 数据平滑迁移<br>
   
2. JuiceFS 受限于元数据服务逻辑都在客户端，上述功能特性比较难以实现，或者勉强在客户端实现，或者通过各种客户端外挂实现，比较凌乱，有潜在各种数据问题隐患。

# 总结

整体上来看，OSS-HDFS/JindoFS 在往全托管方向发展，也就是把元数据管理、OSS bucket 存储都统一封装管理起来，给客户提供开箱即用的云原生 HDFS 
体验。JuiceFS 把 Redis、OSS bucket 都暴露给客户端，有较大的数据安全和破坏风险。OSS-HDFS 目前存在的一些性能短板，都是暂时的，
还有很大的性能优化空间。
