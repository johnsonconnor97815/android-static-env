# android-static-env

[中文](README.md) · [Agent compatibility](docs/agent-compatibility.md) · [Skill](skills/android-static-env/SKILL.md)

An Agent Skills package that provisions and verifies an Android static-analysis toolchain: APK/AAB, DEX/Smali, native `.so` libraries, packer identification, and local rule-based scanning.

## Install from GitHub

With **Node.js >=22.20.0** and npm:

```bash
npx skills@1.6.0 add johnsonconnor97815/android-static-env --skill android-static-env
```

Select your agent interactively, or specify it:

```bash
npx skills@1.6.0 add johnsonconnor97815/android-static-env \
  --skill android-static-env --agent codex --yes
```

Tested installer targets: `codex`, `claude-code`, `cursor`, `github-copilot`, `gemini-cli`, `opencode`, `windsurf`, `cline`, and `roo`. Use `--global` for a user-level install or `--copy` instead of symlinks. The CLI version is pinned to the version used by the compatibility tests.

Codex's built-in installer can install the skill directly from:

```text
$skill-installer Install https://github.com/johnsonconnor97815/android-static-env/tree/main/skills/android-static-env
```

Gemini CLI also supports a native repository installer:

```bash
gemini skills install https://github.com/johnsonconnor97815/android-static-env.git \
  --path skills/android-static-env --scope workspace
```

Installing the skill copies instructions and resources. It does not provision the Android toolchain until you ask your agent to do so. Skill instructions are in Chinese; agents can use them with an English task request.

## Ask your agent

```text
Use android-static-env to set up the full Android static-analysis environment in this project, including native .so analysis.
```

Codex supports `$android-static-env`; Claude Code supports `/android-static-env`. Other agents use their own skill discovery and activation UI.

**The bundled provisioning script requires Linux x86_64 or WSL2 and Python 3.12+.** It was functionally tested on Ubuntu 24.04. Client installation compatibility does not imply that the analysis binaries run on every host OS. See the [platform notes](skills/android-static-env/references/platforms.md).

## Toolchain

- APK and bytecode: Android SDK CLI / Build-Tools, JADX, Apktool, Google smali/baksmali, dex2jar, bundletool, Androguard, Droid ASC.
- Native `.so`: Ghidra, Rizin, LLVM/binutils, checksec, LIEF, pyelftools, Capstone.
- Scanners: APKiD, YARA, Quark with pinned rules, Semgrep.
- Utilities: JDK 21, isolated Python environments, ripgrep, jq, file, 7z, OpenSSL, Graphviz.
- Optional: MobSF container preparation; format-specific Flutter, Unity IL2CPP, and Hermes guidance.

Use the default `full` profile, the smaller `core` profile, or `--only` for selected components. Tools live under the target project's `.android-static/`; existing `.envrc` and `.venv` files are preserved.

## Run without an agent

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

`--install-system-deps` installs apt packages on Ubuntu/Debian and uses `sudo -n` when needed. Omit it when dependencies are already present. `--accept-sdk-licenses` explicitly accepts the Android SDK terms. Downloaded tools retain their respective upstream licenses.

## Verification

```bash
python3 scripts/validate_repository.py
python3 skills/android-static-env/scripts/test_setup.py
python3 scripts/test_agent_install.py --report .validation/agent-installs.json
```

Installer tests use the real Skills CLI and verify discovery paths and every bundled resource hash. They do not run models or provision the Android toolchain. Previous APK, DEX, and ARM/ARM64 `.so` functional validation is summarized [here](skills/android-static-env/references/validation.md), with untested areas listed explicitly.

[Contributing](CONTRIBUTING.md) · [MIT License](LICENSE)

## Local MCP integrations

The optional MCP installer supports JADX (paired GUI plugin and bridge), Apktool MCP, PyGhidra-MCP, and Semgrep's built-in MCP. It pins releases, isolates Python environments, generates stdio configurations, and checks `initialize` plus paginated `tools/list`.

```bash
python3 skills/android-static-env/scripts/mcp_setup.py install --workspace ../android-analysis
python3 skills/android-static-env/scripts/mcp_setup.py check --workspace ../android-analysis
python3 skills/android-static-env/scripts/mcp_setup.py configure --workspace ../android-analysis --client codex
```

Select a subset with `--servers apktool,ghidra,semgrep`. Project configuration targets are `codex`, `claude`, `cursor`, and `vscode`; existing unrelated configuration is retained and changes are backed up. JADX requires an open GUI with the matching plugin and is disabled in the default Codex configuration. A successful protocol probe does not verify decompilation; use `mcp_probe.py --calls` for sample-based checks. See the [MCP guide](skills/android-static-env/references/mcp.md) for exact prerequisites, evidence paths, and optional tool candidates.
