# 本次验证范围

日期：2026-09-16（Pacific/Honolulu）；原始日志使用 UTC。主机：Ubuntu 24.04.5 x86_64、Python 3.12.3。

- 在含空格路径的临时工作区实际安装并检查 14 个组件组：JDK、SDK、JADX、Apktool、smali/baksmali、bundletool、Androguard、dex2jar、APKiD、Quark、Semgrep、Rizin、Ghidra、native-python。
- 同目录重复安装成功；已有 `.envrc` 保持不变。APKiD venv 移出后，按 `--require-hashes` 依赖锁重新创建成功。
- 自建 Smali → DEX → Smali / Java / JAR；Androguard 解析、APKiD 扫描、DEX checksum 校验和已知 YARA/Semgrep 规则均通过。
- OWASP UnCrackable Level 1 APK：Manifest 读取、签名验证、Apktool 解码、固定 Quark 规则扫描通过。样本 SHA-256：`1da8bf57d266109f9a07c01bf7111a1975ce01f190b9d914bcd3ae3dbef96f21`；来源：OWASP/mastg Git blob `9a4f638f1c4a5296fb4eace04b328aecce659b79`。
- 用 Android NDK 29.0.14206865 从本地 C 源码生成 ARM32/ARM64 `.so`：LIEF、pyelftools、Capstone、readelf、LLVM、checksec、Rizin、Ghidra headless 均通过相应检查。核对 JNI 导出、外部依赖、保护位及指令解码，原库哈希保持不变。
- 安装器 6 项本地回归通过：plan 无副作用、保留不受管理目录、拒绝损坏缓存、拒绝归档路径穿越、部分失败返回非零且继续独立组件、含空格路径的重复环境激活。
- Skill 格式校验通过，Python 脚本语法校验通过。

## 实测中修正的问题

SDK 不能把 Command-Line Tools 根目录直接软链到不符合其目录约定的位置。固定版本启动脚本还会在 Java/工具路径含空格时错误拆参；安装器改为标准目录布局和等价的 Java Main/classpath wrapper，保留原发布包不改写。

Rizin 在读取无入口的 DSO 时会向 stderr 写提示，同时向 stdout 输出有效 JSON；功能检查将两者分别保存，避免把诊断文本当 JSON 解析。

## 尚未验证

- MobSF 镜像实际拉取、容器启动与报告生成；本次只核对官方方式和安装器的配置生成逻辑。
- Ghidra/JADX GUI 的桌面显示与交互。
- macOS、Windows 原生、Linux ARM64 主机；随附制品锁只覆盖 Linux x86_64。
- AAB/APKS 的实际转换、特殊 Flutter/Unity/Hermes 样本；这些能力不能从 APK 测试推断。
- apt 实际修改系统。依赖解析通过 `apt-get --simulate`；checksec 使用发行版下载包解压验证，LLVM 使用已有 NDK 工具。Graphviz 只有安装方案核对。

以上是发布前开发验证的摘要。原始日志、下载缓存、APK 和本地构建产物不随 Skill 分发。可以使用 `scripts/test_setup.py` 与 `scripts/smoke.py` 在自己的工作区重做对应检查；仓库的 CI 另外验证各 Agent 安装后的文件完整性。
