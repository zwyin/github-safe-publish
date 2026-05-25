---
name: github-safe-publish
version: "0.1.0"
description: |
  将本地 Git 项目安全地发布到 GitHub 公开仓库。包含两层脱敏扫描
  （确定性规则 + AI 语义）、自动修复、备份回滚、仓库创建、SEO 优化。
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
  - Agent
---

# GitHub Safe Publish

将本地 Git 项目安全地发布到 GitHub 公开仓库。

## 参数

```
/github-safe-publish                    # 核心流程（脱敏+发布）
/github-safe-publish --seo              # 核心 + SEO 优化
/github-safe-publish --ci               # 核心 + CI 生成
/github-safe-publish --seo --ci         # 全部
/github-safe-publish --scan-only        # 只做脱敏扫描，输出报告，不修复不发布
/github-safe-publish --dry-run          # 模拟完整流程：扫描+模拟修复建议，但不做任何实际修改
```

**参数互斥与冲突处理**：
- `--scan-only` 和 `--dry-run` 不能与 `--seo` / `--ci` 组合（SEO 和 CI 只对已推送的仓库有意义，扫描模式不推送）
- `--seo` 和 `--ci` 可以同时使用（完整功能模式）
- 无效组合直接报错并退出
- `--dry-run` 与 `--scan-only` 的区别：`--scan-only` 只输出扫描报告；`--dry-run` 在报告基础上还会展示每个发现项的推荐修复方案（但不执行修复）

**流程控制矩阵**：

| 步骤 | 完整流程 | --scan-only | --dry-run |
|------|---------|-------------|-----------|
| Step 1: 前置检查+参数确认 | 执行 | 执行 | 执行 |
| Step 2: 创建备份分支 | 执行 | 跳过 | 跳过 |
| Step 3: 脱敏扫描 | 执行 | 执行 | 执行 |
| Step 4: 自动修复+用户确认 | 执行 | 跳过 | 输出修复建议但不执行 |
| Step 5: 仓库决策+推送 | （迭代 2） | 跳过 | 跳过 |
| Step 6: 验证+报告 | （迭代 2） | 仅扫描报告 | 仅扫描报告+修复建议 |

## 前提

- 当前目录是 Git 仓库，至少有一个 commit
- `gh` CLI 已安装并登录（可选，支持手动推送）
- 用户确认项目可以公开（已过脱敏）

## Step 1: 前置检查 + 参数确认（集中交互 #1）

<!-- 迭代 1 实现完整内容 -->

## Step 2: 创建备份分支

<!-- 迭代 1 实现完整内容 -->

## Step 3: 脱敏扫描（两层架构）

<!-- 迭代 1 实现完整内容 -->

## Step 4: 自动修复 + 用户确认

<!-- 迭代 1 实现完整内容 -->

## Step 5: 仓库决策确认 + 创建推送（集中交互 #2）

<!-- 迭代 2 实现 -->

## Step 6: 验证 + 输出报告

<!-- 迭代 2 实现 -->

## 可选模块

### --seo 模块

<!-- 迭代 3 实现 -->

### --ci 模块

<!-- 迭代 3 实现 -->

## 注意事项

- 不删除 `origin` remote（通常是内部 NAS Git）
- 不改变当前分支名
- 不 force push
- 脱敏发现的真实密钥必须处理，不能跳过
- 备份分支 `pre-publish-backup` 不推送到远程
