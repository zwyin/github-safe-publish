# github-safe-publish

## 版本管理

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

位置 1-3、5-6 已存在。位置 4 (README.md) 尚未创建。

## 测试

```bash
pytest tests/ -q
scripts/validate_skill.sh
```

## 项目结构要点

- **SKILL.md 是唯一事实源**：所有扫描规则、步骤流程、修复逻辑都定义在 `skills/github-safe-publish/SKILL.md` 中
- **scanning-rules.md 是规则参考**：`docs/scanning-rules.md` 是第 1 层规则的完整正则定义，供维护者参考，SKILL.md 引用但不重复全部正则
- **旧版 SKILL.md**：根目录的 `SKILL.md` 是 v1 版本，已迁移到 `skills/` 目录下，根目录版本已删除
