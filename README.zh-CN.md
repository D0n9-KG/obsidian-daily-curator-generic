# Obsidian Daily Curator Generic

[English](README.md) · [简体中文](README.zh-CN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Release](https://img.shields.io/badge/release-public--v0.1-blue)
![Obsidian](https://img.shields.io/badge/Obsidian-Markdown-purple)
![Safety](https://img.shields.io/badge/safety-dry--run%20first-orange)

> **白天只管随手记，晚上让 Agent 把混乱输入整理成可复习、可检索、会持续进化的 Obsidian 知识库。**

Obsidian Daily Curator Generic 是一个可配置的 Agent skill，适合每天都会记录想法、学习笔记、网页剪藏、论文、视频、代码片段、任务和问题的人。

它解决的问题不是“如何写更漂亮的日记”，而是：

> **如何把低摩擦的每日输入，稳定沉淀成长期可用的知识库。**

---

## 为什么需要它

Daily note 很适合捕捉，但不适合作为最终知识存储层。

如果缺少日终整理，vault 很容易变成：

- 半消化的网页剪藏；
- 复制来的论文摘要；
- 以后再也找不到的代码片段；
- 没有链接路径的灵感；
- 混在学习记录里的任务和疑问；
- 很难复习的流水账日记。

这个 skill 的工作流很简单：

```text
混乱的每日记录 → 日终 Agent 整理 → 可复习、可检索的知识库
```

你白天不需要为了格式打断学习。晚上让 Agent 做一次稳定的整理、归类和链接管理。

---

## 它会产出什么

| 白天记录的内容 | 日终整理后的去向 |
|---|---|
| 想法、假设、灵感 | 日终总结、项目线索或可复用笔记 |
| 概念、方法、模型 | 原子化知识卡片 |
| Python/API/代码片段 | 可复用代码用法笔记或项目笔记 |
| 网页、文档、工具 | 资料 / source notes |
| 论文、视频、课程 | 资料笔记 + 可复用知识卡片 |
| 资讯、当前信息 | 资料笔记或总结；必要时标记未验证 |
| 任务、问题 | 日终总结 + unresolved queue |
| 复盘、体会 | 每日复盘和经验沉淀 |

一次好的整理不只是总结今天，而是要告诉你：**学到了什么、创建了什么、分别放到了哪里。**

---

## 快速开始

### 1. 安装 skill

把这个目录复制到你的 Agent skills 目录：

```text
<skills-dir>/obsidian-daily-curator-generic/SKILL.md
```

如果你只是评估或开发这个发布包，建议先不要放进 active skills 目录，避免误触发。

### 2. 安全初始化 vault

在 Obsidian vault 根目录下，先预览初始化计划：

```bash
python /path/to/obsidian-daily-curator-generic/scripts/bootstrap_vault.py --vault . --dry-run
```

确认没问题后再应用：

```bash
python /path/to/obsidian-daily-curator-generic/scripts/bootstrap_vault.py --vault . --apply
```

### 3. 白天随手记录

你可以随便记。下面这些前缀不是强制的，但能帮助 Agent 更快识别类型：

```markdown
- [idea] 笔记标题应该匹配未来检索时会想到的关键词。
- [knowledge] MOC 应该是导航层，而不是内容垃圾桶。
- [code] Python pathlib: `Path.mkdir(parents=True, exist_ok=True)` 可以安全创建多级目录。
- [resource] 标题：Obsidian Help - Internal links  
  URL: https://help.obsidian.md/links  
  为什么有用：解释 wikilink 行为。
- [question] source notes 和 knowledge cards 是否应该使用不同的状态字段？
```

### 4. 晚上运行整理

告诉你的 Agent：

```text
Use obsidian-daily-curator-generic to curate today.
```

或者指定日期：

```text
Run a daily curation for 2026-01-02.
```

---

## 安全模型

这个 skill 默认非常保守：

- 保留原始 daily notes 和导入资料；
- 默认不覆盖已有文件；
- 未经明确确认，不批量移动、重命名或删除笔记；
- 初始化支持 `--dry-run` 预览；
- 配置保存在 vault 内部的 `.daily-curator/config.json`；
- 分类不确定的内容进入 `.daily-curator/unresolved.md`。

在重要 vault 中使用前，建议开启 Git、Obsidian Sync 历史版本或其它备份方式。

---

## 默认 vault 结构

初始化脚本只会创建缺失的文件和目录：

```text
.daily-curator/
  config.json
  curation-rules.md
  vault-architecture.md
  unresolved.md
  curation-log.md
Daily/
Templates/
Reviews/Daily/
Knowledge/
Sources/
Maps/
Projects/
Career/
```

所有路径都可以在 `.daily-curator/config.json` 中修改。

---

## 配置

初始化后编辑 `.daily-curator/config.json`。

重要字段：

- `paths.daily_notes`：daily notes / quick capture 存放位置。
- `paths.knowledge_cards`：长期知识卡片存放位置。
- `paths.sources`：网页、论文、视频、工具等资料笔记位置。
- `paths.mocs`：MOC / map 位置。
- `paths.daily_summaries`：日终总结位置。
- `paths.unresolved`：无法确定归类的内容位置。
- `scan.include_dirs`：限制扫描范围。为空时扫描整个 vault，但排除忽略目录。
- `scan.exclude_dirs`：扫描时忽略的目录。
- `behavior.prepare_next_day_note`：整理结束后是否创建第二天 quick-capture note。
- `behavior.bulk_move_requires_approval`：建议保持为 true，避免未经确认的大规模迁移。

---

## 辅助脚本

```bash
# 预览或初始化 vault
python scripts/bootstrap_vault.py --vault /path/to/vault --dry-run
python scripts/bootstrap_vault.py --vault /path/to/vault --apply

# 创建 daily quick-capture note
python scripts/prepare_quick_capture.py --vault /path/to/vault --date 2026-01-02
python scripts/prepare_quick_capture.py --vault /path/to/vault --tomorrow

# 扫描当天整理上下文
python scripts/scan_vault.py --vault /path/to/vault --date 2026-01-02

# 验证发布包
python scripts/test_smoke.py
python scripts/check_release.py
```

---

## 示例

- `examples/minimal-vault/`：英文最小示例。
- `examples/chinese-vault/`：中文随时记示例。

示例只展示输入风格和整理方向。真正的整理内容由 Agent 在运行时生成。

---

## 它不是什么

- 不是 Obsidian 插件。
- 不是自动定时任务系统。
- 不能替代你对“什么值得长期保存”的判断。
- 不是事实核查引擎；资讯和高风险事实仍需要验证。

如果你想自动定时运行，需要额外使用 cron、Windows Task Scheduler 或支持定时任务的 Agent 环境。

---

## 项目状态

当前版本：`public-v0.1`

这是早期公开版本。它优先保证安全和可配置性，但建议先在有备份的 vault 中测试。

## 许可证

MIT
