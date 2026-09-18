# android-static-env

[![CI](https://github.com/johnsonconnor97815/android-static-env/actions/workflows/ci.yml/badge.svg)](https://github.com/johnsonconnor97815/android-static-env/actions/workflows/ci.yml)
[English](README.en.md) · [Agent 安装兼容性](docs/agent-compatibility.md) · [Skill](skills/android-static-env/SKILL.md)

为 Android App 静态分析准备可运行、可检查的工具链，覆盖 APK/AAB、DEX/Smali、`.so` 原生库、加固识别和规则扫描。使用标准 Agent Skills 格式，可从此 GitHub 仓库安装到 Codex、Claude Code、Cursor、GitHub Copilot、Gemini CLI、OpenCode、Windsurf、Cline 和 Roo Code。

## 从仓库安装 Skill

通用安装方式使用 [Vercel Skills CLI](https://github.com/vercel-labs/skills)，需要 **Node.js >=22.20.0** 和 npm：

```bash
npx skills@1.6.0 add johnsonconnor97815/android-static-env --skill android-static-env
```

按提示选择 Agent。默认安装到当前项目；添加 `--global` 可安装到个人目录。固定 `skills@1.6.0` 是为了使用本仓库验证过的安装器版本。

指定一个 Agent，无需交互：

```bash
npx skills@1.6.0 add johnsonconnor97815/android-static-env \
  --skill android-static-env --agent codex --yes
```

同时安装到多个 Agent：

```bash
npx skills@1.6.0 add johnsonconnor97815/android-static-env \
  --skill android-static-env \
  --agent codex claude-code cursor github-copilot gemini-cli opencode windsurf cline roo \
  --yes
```

安装器支持复制和软链接；需要独立文件副本时添加 `--copy`。只查看仓库里的 Skill 可用 `--list`。安装 Skill 仅放置说明、脚本与资源，**不会自动下载或运行 Android 工具链**。

Codex 也可使用内置安装器：

```text
$skill-installer 从 https://github.com/johnsonconnor97815/android-static-env/tree/main/skills/android-static-env 安装 Skill
```

Gemini CLI 的原生仓库安装命令：

```bash
gemini skills install https://github.com/johnsonconnor97815/android-static-env.git \
  --path skills/android-static-env --scope workspace
```

不使用 Node.js 时，可按 [手动安装说明](docs/agent-compatibility.md#手动安装) 从 Git 仓库复制完整 Skill 目录。

## 使用

在支持的 Agent 中请求：

```text
使用 android-static-env，在当前项目搭建完整 Android 静态分析环境，包含 .so 分析工具。
```

Codex 可显式使用 `$android-static-env`；Claude Code 可使用 `/android-static-env`。其他客户端按各自的 Skill 选择或自动发现方式调用。

**Skill 的客户端兼容性与分析脚本的主机支持范围不同。** 随附一键安装器面向 **Linux x86_64 / WSL2、Python 3.12+**，当前基线在 Ubuntu 24.04 验证。macOS、Linux ARM64、Windows 原生适配见 [平台说明](skills/android-static-env/references/platforms.md)。

## 包含的工具

| 范围 | 工具 |
| --- | --- |
| APK、资源、签名 | SDK Command-Line Tools / Build-Tools、apkanalyzer、aapt/aapt2、apksigner、zipalign、Apktool |
| 字节码与包格式 | JADX、Google smali/baksmali、dex2jar、bundletool、Androguard |
| `.so` / ELF | Ghidra、Rizin、LLVM/binutils、checksec、LIEF、pyelftools、Capstone |
| 规则与加固识别 | APKiD、YARA、Quark + 固定规则、Semgrep |
| 基础工具 | Temurin JDK 21、Python venv、ripgrep、jq、file、7z、OpenSSL、Graphviz |
| MCP 接入 | JADX + 插件、Apktool MCP、PyGhidra-MCP、Semgrep 内置 MCP；本地 stdio 与项目配置 |
| 可选 | MobSF 容器；特殊 Flutter、Unity IL2CPP、Hermes 工具按输入选择 |

`full` 为默认范围；`core` 适用于轻量环境；`--only` 可补装指定组件。完整选型见 [工具矩阵](skills/android-static-env/references/tool-matrix.md)。

## MCP 接入

需要 Agent 直接导航反编译结果、查询 `.so` 或调用规则扫描时：

```bash
python3 skills/android-static-env/scripts/mcp_setup.py install --workspace ../android-analysis
python3 skills/android-static-env/scripts/mcp_setup.py check --workspace ../android-analysis
python3 skills/android-static-env/scripts/mcp_setup.py configure --workspace ../android-analysis --client codex
```

支持 `--servers jadx,apktool,ghidra,semgrep` 选择服务，自动补装对应引擎。`--client` 支持 `codex`、`claude`、`cursor`、`vscode`；配置合并前备份，保留其他服务。JADX 需要专用 GUI 打开样本，默认不启用；其他三项可无界面运行。协议检查与样本分析分开验证。

固定版本、GUI 启动、配置位置、实际调用验证，以及 headless JADX、radare2、MobSF、FlowDroid 等候选的边界见 [MCP 文档](skills/android-static-env/references/mcp.md)。

## 直接运行安装器

也可以独立于 Agent 使用：

```bash
git clone https://github.com/johnsonconnor97815/android-static-env.git
cd android-static-env
python3 skills/android-static-env/scripts/setup.py plan --workspace ../android-analysis
python3 skills/android-static-env/scripts/setup.py install --workspace ../android-analysis \
  --profile full --install-system-deps --accept-sdk-licenses
source ../android-analysis/.android-static/env.sh
python3 skills/android-static-env/scripts/setup.py check --workspace ../android-analysis
python3 skills/android-static-env/scripts/smoke.py --workspace ../android-analysis
```

`--install-system-deps` 在 Ubuntu/Debian 安装所需 apt 包；非 root 使用 `sudo -n`。依赖已满足时可以省略。`--accept-sdk-licenses` 表示接受 [Android SDK 条款](https://developer.android.com/studio/terms)；未提供时不会自动接受新许可。

工具、Python venv 和下载锁位于目标项目的 `.android-static/`。已有 `.envrc`、`.venv` 和系统 Java 不会被替换；生成的日志和版本清单供复查。每个 Python 分析器独立安装，APKiD 的 YARA dex binding 与其他环境分开。

对授权 `.so` 做只读元数据与有限反汇编检查：

```bash
so-info path/to/libexample.so --source '样本来源或提取记录' --output so-info.json
```

原始 APK、`.so` 和扫描日志不随此仓库发布。下载工具仍遵循各自的许可。

## 验证

```bash
python3 scripts/validate_repository.py
python3 skills/android-static-env/scripts/test_setup.py
python3 skills/android-static-env/scripts/test_mcp.py
python3 scripts/test_agent_install.py --report .validation/agent-installs.json
```

安装兼容性测试调用真实 `skills@1.6.0`，逐个检查 9 种 Agent 的发现目录，并比较所有脚本、规则锁和参考文件的 SHA-256。CI 运行安装检查；它不调用模型，也不全量下载 Android 工具链。

此前已对 DEX、OWASP 示例 APK 和 ARM32/ARM64 `.so` 进行功能验证，范围和限制见 [验证摘要](skills/android-static-env/references/validation.md)。GUI、MobSF 服务和所有主机平台的运行能力不由 Skill 安装测试推断。

## 维护

仓库中的 `skills/android-static-env/` 是唯一源目录。修改工具版本时更新 `assets/toolchain.lock.json`，核对官方来源后执行对应验证。发布和贡献方式见 [维护说明](CONTRIBUTING.md)。

本仓库的说明与脚本使用 [MIT License](LICENSE)。
