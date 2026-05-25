---
name: publish-github
description: |
  首次将本地项目推送到 GitHub public 仓库。包含脱敏检查、仓库创建、
  链接更新、远程配置、推送。适用于已经完成本地开发、准备开源的项目。
  Use when: "push to github", "publish to github", "开源", "推送到 GitHub",
  "create github repo", "发布到 github"。
triggers:
  - push to github
  - publish to github
  - create github repo
  - 开源发布
  - 推送到 GitHub
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Publish to GitHub Public Repo

将本地 Git 项目首次推送到 GitHub 公开仓库的完整流程。

## 前提

- 当前目录是 Git 仓库，至少有一个 commit
- `gh` CLI 已安装并登录（`gh auth status` 可通过）
- 用户确认项目可以公开（已过脱敏）

## Step 1: Pre-flight 检查

```bash
git status --short
git remote -v
gh auth status 2>&1 | head -5
```

如果已有 `github` remote，说明已经推送过。告知用户并退出。

确认当前分支。如果用户没有指定分支名，使用当前分支。

## Step 2: 多轮独立脱敏扫描（必做）

推送 public 仓库前，使用独立子 agent 进行多轮脱敏审查。每轮 agent 不共享上下文，
独立审查，逐步收紧。主 agent 只负责收集结果和呈现给用户。

### 扫描范围

每轮 agent 必须检查以下维度：

1. **密钥与凭证**：API key、password、token、secret、credential、private key
2. **个人信息**：真实姓名、手机号、邮箱（非 GitHub 公开邮箱）、地址、身份证号
3. **内部基础设施**：内网 IP、域名、服务器路径、NAS 地址、VPN 配置
4. **业务数据**：真实用户数据、订单号、交易金额、内部项目代号
5. **Git 历史**：commit message 中的内部系统名、同事姓名、内部链接
6. **.gitignore 充分性**：是否有 .env、.db、证书文件被跟踪
7. **文档中的可溯源描述**：具体到可通过搜索引擎定位到个人/组织的叙述

### 结果分类

- **CRITICAL**：真实密钥、凭证、个人信息 → 必须移除，阻塞推送
- **WARNING**：可能敏感但不确定 → 列出给用户判断
- **SAFE**：示例占位符（`your_xxx`、`REPLACE_ME`）、README 中的通用描述

### 执行流程

**第 1 轮：基础扫描**

启动 1 个独立子 agent，做全面但快速的第一遍扫描。

```
Agent prompt 要点：
- 扫描所有将被推送到 GitHub 的文件内容（git ls-files）
- 对每个维度逐一检查
- 输出结构化报告：维度 / 文件:行号 / 内容 / 严重级别
- 不修改任何文件
```

收集第 1 轮结果，呈现给用户看基本情况。如果第 1 轮发现 CRITICAL 问题，
先用 AskUserQuestion 确认是否要先修复再继续。

**第 2-5 轮：深度复查**

在第 1 轮基础上，每轮启动 1 个独立子 agent 进行复查。

```
Agent prompt 要点：
- 你是第 N 轮独立审查员，不信任之前的任何审查结果
- 已知前几轮发现的问题列表：（附上摘要，但不附原文上下文）
- 你的任务：找出前几轮遗漏的问题
- 重点检查：容易被忽视的文件（配置文件、注释、changelog、commit 历史）
- 重点检查：间接泄露（如通过文件路径推断内部结构、通过时间戳推断工作节奏）
- 输出格式同第 1 轮
```

**终止条件**：
- 某轮复查 0 个新发现 → 停止，不再继续
- 已完成 5 轮 → 停止
- 用户在任意轮次后说"够了" → 停止

**汇总**：所有轮次结束后，合并去重，按严重级别排序，一次性呈现给用户。

### 修复流程

扫描汇总后，按严重级别进入不同的处理路径：

**CRITICAL（必须处理，阻塞推送）**：

对每个 CRITICAL 项，用 AskUserQuestion 让用户选择处理方式：

- A) **自动替换** — agent 将敏感内容替换为泛化占位符（如 `your-api-key`、`user@example.com`）
- B) **手动修复** — 用户自己在编辑器里改，改完后 agent 重新扫描该文件验证
- C) **删除文件** — 从 git 中移除整个文件（`git rm`）
- D) **确认安全** — 用户确认该内容实际不敏感，标记为 SAFE（需要用户输入理由）

自动替换规则（选 A 时）：
- 真实密钥/token → `REPLACE_ME_<类型>`（如 `REPLACE_ME_API_KEY`）
- 个人邮箱 → `user@example.com` 或 GitHub 公开邮箱
- 内部 IP/域名 → `192.168.x.x` / `internal.example.com`
- 真实姓名 → `FIRST_NAME` / `LAST_NAME`
- 手机号 → `1XX-XXXX-XXXX`
- 可溯源叙事 → 泛化为通用描述，保留语义但去掉可定位细节

**WARNING（用户决定）**：

- A) 同上处理（修复）
- B) 接受风险，标记为已知，继续推送

**git 历史中的敏感信息**（特殊情况）：

如果敏感信息存在于已 commit 的历史中（不仅仅是当前工作区）：

1. 先评估影响范围：`git log --all -S "敏感字符串" --oneline`
2. 呈现给用户：哪些 commit 包含、涉及哪些文件
3. 处理方式（用 AskUserQuestion）：
   - A) **重写历史** — `git filter-repo` 或 BFG Repo Cleaner 清除（仅限尚未推送的 commit）
   - B) **新建干净仓库** — 从当前工作区初始化全新 git 仓库，不带历史（最安全）
   - C) **接受风险** — 历史中存在但影响可控（用户需明确确认）

注意：如果历史已被推送到任何 remote，重写历史后需要 force push。
此 skill 不自动执行 force push，必须用户明确确认。

### 修复验证

所有 CRITICAL 项处理完成后，启动 1 轮验证扫描（独立子 agent）：

```
Agent({
  description: "Post-fix verification scan",
  prompt: "你是脱敏验证 agent。项目路径 [PATH]。
          以下敏感项已被修复：[修复清单]。
          你的任务是验证：(1) 每个修复项确实已清除 (2) 修复未引入新的敏感信息。
          扫描所有 git 跟踪文件。输出：每项 PASS/FAIL + 是否有新发现。",
  subagent_type: "general-purpose"
})
```

验证结果：
- 全部 PASS → 进入 Step 3（创建仓库）
- 有 FAIL → 回到修复流程，重新处理失败项
- 有新发现 → 追加到发现列表，重新走修复流程

### 技术实现

使用 Agent tool 启动独立子 agent：

```
# 第 1 轮扫描
Agent({
  description: "Round 1: desensitization scan",
  prompt: "你是一个安全审查 agent。扫描项目目录 [PATH] 中所有 git 跟踪文件，
          检查 7 个维度的敏感信息。输出结构化报告。不修改任何文件。",
  subagent_type: "general-purpose"
})

# 第 N 轮复查（N >= 2）
Agent({
  description: "Round N: deep desensitization review",
  prompt: "你是第 N/5 轮独立脱敏审查员。项目路径 [PATH]。
          之前轮次发现了 [摘要列表]。你的任务是找出遗漏。
          重点：间接泄露、边缘文件、注释和 commit 历史。",
  subagent_type: "general-purpose"
})
```

注意：
- 并发限制：同时最多 2 个子 agent（见 CLAUDE.md 并发规则）
- 脱敏扫描轮次之间有依赖（后续轮次需要前序结果），应串行执行
- 每轮 agent 的 prompt 必须自包含，不依赖对话上下文

## Step 3: 创建 GitHub 仓库

获取用户偏好（可通过参考已有项目或询问）：

1. **仓库名**：默认用当前目录名
2. **描述**：从 README 第一段提取，或让用户提供
3. **可见性**：默认 public

```bash
REPO_NAME=$(basename "$(pwd)")
gh repo create "$REPO_NAME" --public --description "DESCRIPTION" --clone=false
```

如果仓库已存在同名，`gh` 会报错。告知用户选择：
- A) 使用已有仓库（直接添加 remote）
- B) 换个名字

## Step 4: 更新占位链接

扫描 README 和文档中的占位链接：

```bash
grep -rn "yourname/\|your-username/\|USERNAME/" --include="*.md" . 2>/dev/null | grep -v .git | head -10
```

常见占位模式：
- `github.com/yourname/repo` → `github.com/zwyin/repo`
- `github.com/your-username/repo` → `github.com/zwyin/repo`
- Badge 链接中的占位用户名

获取 GitHub 用户名（从 `gh` 或已有 remote）：

```bash
gh api user --jq '.login' 2>/dev/null
```

批量替换所有占位链接为实际用户名。展示改动清单给用户确认。

## Step 5: 提交并配置远程

如果有链接更新，先提交：

```bash
git add README.md [其他修改的文件]
git commit -m "docs: update placeholder links to actual GitHub repo"
```

添加 remote（使用 `github` 命名约定，保留 `origin` 给内部 Git）：

```bash
git remote add github https://github.com/USERNAME/REPO_NAME.git
```

## Step 6: 推送

```bash
git push github CURRENT_BRANCH
```

推送完成后输出仓库 URL。

## Step 7: 验证

```bash
gh repo view --json url,visibility -q '.url + " (" + .visibility + ")"'
```

确认仓库可见性和 URL 正确。

## 输出

推送完成后输出总结：

```
Published to GitHub:
  URL: https://github.com/USERNAME/REPO
  Branch: BRANCH
  Commits: N
  Visibility: public
  Desensitization: passed/warnings (N items reviewed)
```

## Step 8: 项目首页 SEO 优化

推送成功后，优化 GitHub 项目首页的可见性和转化率。
包含平台侧元数据（Description + Topics）和 README 内容优化。

### 8.1 设置 Description（About 简介）

GitHub 搜索排名第一因子，也出现在 topic 页推荐中。

```bash
gh repo edit USERNAME/REPO --description "DESCRIPTION"
```

**规则：**
- 控制在 **120 字符以内**（理想），最长不超过 250 字符
- 以**主关键词开头**，说明项目是什么、做什么
- 包含核心技术关键词（语言、框架、格式等）
- 如有独特卖点，简洁提及（如"boosts coverage to ~90%"）

**写法参考：**
- CV/resume generator for academics and engineers, YAML to PDF.
- Data validation using Python type hints.
- Batch geotag camera photos from GPS tracks (GPX/KML/TCX). Two-pass neighbor algorithm boosts match coverage to ~90%.

### 8.2 设置 Topics（标签）

Topic 页是 GitHub 最主要的流量入口（99% 搜索来自 Google/ChatGPT 跳转的 topic 页）。

```bash
gh repo edit USERNAME/REPO --add-topic "tag1,tag2,tag3,..."
```

**规则：**
- 至少 **6 个**标签（上限 20 个）
- 标签分三类，均衡覆盖：
  - **用途**（`geotag`, `data-visualization`, `automation`）
  - **技术栈**（`python`, `pyside6`, `flask`, `nextjs`）
  - **领域**（`machine-learning`, `nlp`, `api`, `gis`）
- 不用项目主语言做标签（GitHub 自动显示，无 SEO 价值）
- 不用无意义标签（`beta`, `v2`, `release`, `app`）
- 选**中等竞争度**的标签：太冷门没人搜，太热门排不上

### 8.3 README Badges

在标题（`#`）下方、正文之前添加 badges，提升可信度。

```markdown
# Project Name

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-N%20passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-XX%25-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/platform-Win%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)]()
```

**常用 badge 类型：**
| Badge | 何时用 |
|-------|--------|
| License | 所有项目 |
| Tests + Coverage | 有测试的项目 |
| Platform | 跨平台项目 |
| Python/Node/etc | 有运行时版本要求 |

使用 [shields.io](https://shields.io/) 生成，手动写 URL 即可，不需要 CI 动态 badge。

### 8.4 README 截图/GIF

首屏（标题 + 一句话描述之后）放一张应用截图或操作演示 GIF。

**规则：**
- 截图是最重要的转化元素，优先级高于 badges
- 理想状态：应用有数据/结果的状态，而非空白界面
- 用窗口截图而非全屏截图，避免干扰
- 存放位置：`docs/images/screenshot.png`
- 格式选择：静态展示用 PNG，交互流程用 GIF

**macOS 窗口截图方法：**

```bash
# 方法 1: 用 Quartz 获取窗口 ID 后截取
python3 -c "
import Quartz, json
windows = Quartz.CGWindowListCopyWindowInfo(
    Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
for w in windows:
    owner = w.get('kCGWindowOwnerName', '')
    name = w.get('kCGWindowName', '')
    if 'TARGET_APP' in name:
        print(w.get('kCGWindowNumber'))
"
screencapture -l WINDOW_ID -o docs/images/screenshot.png

# 方法 2: 手动截图（最简单）
# Cmd+Shift+4 → Space → 点击目标窗口
```

**README 中引用：**

```markdown
![Project Name](docs/images/screenshot.png)
```

### 8.5 SEO 内容规范

**不要做的事：**
- 不要写 "Keywords" 段落（GitHub/Google 不使用 meta keywords，纯占空间）
- 不要堆砌关键词（影响可读性且搜索引擎会降权）
- 不要在标题中用过长的描述（H1 保持项目名 + 简短 tagline）

**要做的：**
- 关键词**自然分布**在正文、标题、表格中（"geotag photos"、"GPS track"、"EXIF" 等在描述功能时自然出现）
- README 标题层级遵循 HTML 规范：`#` 项目名 → `##` 章节 → `###` 子章节
- README 结构覆盖搜索引擎和用户都关心的问题：
  - 这是什么？（首段描述）
  - 给谁用的？（Target users）
  - 和同类比有什么优势？（Comparison / Why This Tool）
  - 怎么用？（Quick Start + 截图）
  - 技术栈是什么？（Badges + Development 章节）

### 8.6 中英文 README

如果项目面向国际用户且作者中文为母语，提供双语 README：

- 英文 `README.md` 放根目录（主文档，SEO 入口）
- 中文 `docs/README_zh.md` 放 docs 目录
- 两份文档顶部互相链接

```markdown
# 英文 README 顶部
[中文文档](docs/README_zh.md)

# 中文 README 顶部
[English](../README.md)
```

**两份文档的 SEO 元素同步维护：**
- badges 一致
- 截图可共用同一张（UI 语言用英文截图覆盖更广用户群）
- description 各用各的语言，但关键词覆盖相同概念

## 注意事项

- 不删除 `origin` remote（通常是内部 NAS Git）
- 不改变当前分支名
- 不 force push
- 脱敏发现的真实密钥必须处理，不能跳过
- Description 和 Topics 是 GitHub 平台侧元数据，不在代码仓库中，通过 `gh repo edit` 设置
