# 维护与发布

`skills/android-static-env/` 是唯一的发布源。所有 Agent 安装同一目录；不要增加各 Agent 的重复 Skill 副本，也不要把规则文件或运行脚本放到 Skill 目录外。

## 修改后检查

需要 Python 3.12+；安装兼容性测试另需 Node.js >=22.20.0 和 npm。

```bash
python3 scripts/validate_repository.py
python3 skills/android-static-env/scripts/test_setup.py
python3 scripts/test_agent_install.py --report .validation/agent-installs.json
python3 scripts/test_agent_install.py --mode symlink --report .validation/agent-symlinks.json
```

格式和安装测试不下载 Android 工具链。涉及工具安装、CLI 参数或分析行为的改动，需要在支持的 Linux x86_64 环境执行对应的 `setup.py` / `smoke.py` 测试，并记录版本、输入来源和 SHA-256。单纯分发格式改动不必重复下载全部工具。

## 工具版本更新

修改 `skills/android-static-env/assets/toolchain.lock.json` 前核对上游发行说明、运行时要求和目标架构。有上游 checksum 时使用上游值；没有时保持“首次下载哈希”标记，不能把自行计算的哈希写成上游签名验证。

更新所用 Skills CLI 版本时，同时修改 `scripts/test_agent_install.py`、README 命令和兼容性说明，重新验证所有目标目录。

## 发布

1. 本地检查通过，审查 `git diff` 和待提交文件。
2. 确认没有 APK、DEX、`.so`、JAR、下载缓存、设备信息、扫描日志、凭据或个人路径。
3. 推送后等待 CI 完成。
4. 从远端 GitHub URL 再次运行 `scripts/test_agent_install.py --source <owner/repo>`，核对上传版本的完整性。
5. 用版本标签标记已验证提交，保持已发布标签不变。

本仓库代码与说明采用 MIT；下载工具保留各自许可。不向仓库提交第三方工具二进制或分析样本。
