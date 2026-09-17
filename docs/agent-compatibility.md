# Agent 安装兼容性

本仓库只维护一份 Skill：`skills/android-static-env/`。`SKILL.md` 使用通用的 `name`、`description` 和 `license` 元数据；环境要求写在正文。`agents/openai.yaml` 是可选 Codex UI 元数据，其他客户端可忽略它。脚本通过自身文件位置定位资源，不依赖某个 Agent 的安装路径或专有工具 API。

## 通用仓库安装

使用已经核对过的 `skills@1.6.0`（Node.js >=22.20.0）：

```bash
npx skills@1.6.0 add johnsonconnor97815/android-static-env \
  --skill android-static-env --agent codex --yes
```

替换 `--agent` 即可。下表是该版本安装器实际使用的**项目安装路径**，不是所有客户端唯一支持的路径。

| Agent | `--agent` 参数 | 项目安装目录 |
| --- | --- | --- |
| Codex | `codex` | `.agents/skills/android-static-env/` |
| Claude Code | `claude-code` | `.claude/skills/android-static-env/` |
| Cursor | `cursor` | `.agents/skills/android-static-env/` |
| GitHub Copilot | `github-copilot` | `.agents/skills/android-static-env/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/android-static-env/` |
| OpenCode | `opencode` | `.agents/skills/android-static-env/` |
| Windsurf | `windsurf` | `.windsurf/skills/android-static-env/` |
| Cline | `cline` | `.agents/skills/android-static-env/` |
| Roo Code | `roo` | `.roo/skills/android-static-env/` |

- `--global` 安装到该 Agent 的个人目录，具体路径由 Skills CLI 决定；不手工覆盖现有 Skill。
- `--copy` 安装独立副本；默认模式会在需要时使用软链接。
- 安装特定版本可使用 GitHub tree URL，例如将 `main` 替换为仓库的发布标签：`https://github.com/johnsonconnor97815/android-static-env/tree/main/skills/android-static-env`。
- 旧版客户端若不扫描 `.agents/skills`，应更新客户端或改用其专属 Skill 目录；安装成功并不证明旧版客户端支持新目录。

## Codex 原生安装

在 Codex 中输入：

```text
$skill-installer 从 https://github.com/johnsonconnor97815/android-static-env/tree/main/skills/android-static-env 安装 Skill
```

它只需要完整的 Skill 子目录。实际工具执行无需 Exa、Tavily、Context7 或任何 OpenAI API；这些连接器只在开发或更新文档时可选使用。

## Gemini CLI 原生安装

```bash
gemini skills install https://github.com/johnsonconnor97815/android-static-env.git \
  --path skills/android-static-env --scope workspace
```

在 Gemini CLI 会话中用 `/skills list` 检查发现情况。这个原生命令来自官方文档；自动兼容性测试使用通用 Skills CLI，不把两者混称为同一次验证。

## 手动安装

先克隆仓库，然后把**整个** `skills/android-static-env/` 复制到目标 Agent 的 Skill 根目录，不能只复制 `SKILL.md`。

例如安装到当前项目的 Claude Code 目录（从当前项目运行）：

```bash
git clone https://github.com/johnsonconnor97815/android-static-env.git android-static-env-source
mkdir -p .claude/skills
cp -R android-static-env-source/skills/android-static-env .claude/skills/
```

复制前先确认 `.claude/skills/android-static-env` 不存在；已有安装应按其安装器的更新流程处理。Codex、Cursor、Copilot、Gemini CLI 和 OpenCode 可用通用 `.agents/skills/`；Windsurf 和 Roo Code 使用上表目录。也可选择客户端官方文档列出的用户级目录。

## 验证能证明什么

`python3 scripts/test_agent_install.py` 调用真实 `skills@1.6.0`，在独立临时项目中逐个执行安装，并检查：

1. 安装器返回成功。
2. Skill 位于对应客户端的发现目录。
3. `SKILL.md`、LICENSE、全部脚本、参考文档、版本锁与源文件的 SHA-256 一致。
4. 安装 Skill 时没有触发 `.android-static/` 工具链安装。

`--mode symlink` 验证默认安装方式。CI 在 Linux、macOS、Windows 上验证复制安装，在 Linux/macOS 上另外验证默认方式。CI 的当前实际结果以 [Actions](https://github.com/johnsonconnor97815/android-static-env/actions) 为准。

这些是安装与资源完整性测试，不是调用 9 种 Agent 的模型完成全量分析。Android 工具链的自动安装支持 Linux x86_64/WSL2；其余平台的安装 Skill 操作和执行分析工具操作应分别判断。

## 官方依据

核对日期：2026-09-16。

- [Agent Skills specification](https://agentskills.io/specification)
- [Skills CLI：来源格式、安装范围、Agent 目录和发现规则](https://github.com/vercel-labs/skills/blob/1a6f8649f93dda000a9672e63e8c9c9eeed24da4/README.md)
- [Skills CLI 1.6.0 / Node.js 要求](https://github.com/vercel-labs/skills/blob/1a6f8649f93dda000a9672e63e8c9c9eeed24da4/package.json)
- [OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Cursor Agent Skills](https://cursor.com/docs/context/skills)
- [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/)
- [OpenCode Agent Skills](https://opencode.ai/docs/skills/)
