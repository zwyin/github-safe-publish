# github-safe-publish

## 推送命令

本地代理拦截 HTTPS（端口 443），需显式绕过：

```bash
git -c http.proxy="" -c https.proxy="" push github master
```

SSH 密钥绑定 `openclaw-jarvis-lab` 账户，无法推送到 `zwyin/` 仓库。使用 gh CLI 的 OAuth token（`gh auth setup-git`）+ 上述绕过代理方式推送。

### 唯一版本源

版本号定义在 `skills/github-safe-publish/SKILL.md` frontmatter 的 `version` 字段。

### 版本号出现位置（6 处）

| # | 文件 | 位置 | 说明 |
|---|------|------|------|
| 1 | `skills/github-safe-publish/SKILL.md` | frontmatter `version: "X.Y.Z"` | **唯一版本源** |
| 2 | `.claude-plugin/plugin.json` | `"version": "X.Y.Z"` | 迭代 4 创建 |
| 3 | `.claude-plugin/marketplace.json` | `"version": "X.Y.Z"` | 迭代 4 创建 |
| 4 | `README.md` | version badge URL | 迭代 4 创建 |
| 5 | `CHANGELOG.md` | 版本标题 | 迭代 4 创建 |
| 6 | `scripts/release.sh` | 读取并同步 | 迭代 4 创建 |

所有 6 处位置均已存在。

## 测试

```bash
pytest tests/ -q
scripts/validate_skill.sh
```

## 项目结构要点

- **SKILL.md 是唯一事实源**：所有扫描规则、步骤流程、修复逻辑都定义在 `skills/github-safe-publish/SKILL.md` 中
- **scanning-rules.md 是规则参考**：`docs/scanning-rules.md` 是第 1 层规则的完整正则定义，供维护者参考，SKILL.md 引用但不重复全部正则
- **convert.sh 多平台转换**：`scripts/convert.sh` 将 SKILL.md 转换为 Cursor (.mdc)、Windsurf (.windsurfrules)、OpenCode (AGENTS.md) 格式，输出到 `dist/`
- **已发布**：https://github.com/zwyin/github-safe-publish
