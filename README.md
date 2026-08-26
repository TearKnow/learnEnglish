# learnEnglish

在 Cursor 里用「新概念」风格分析英文句子／段落：句型划线、翻译、稍难词汇（含音标）、考试档次难易度。

## 怎么用

在 Cursor 对话里粘贴英文，并说例如：

- 分析这句 / 分析这段
- 帮我分析
- 按新概念分析

Agent 会按固定结构输出：**原句 → 句型分析 → 翻译 → 稍难词汇 / 短语 → 难易度**。

## 项目结构

| 路径 | 作用 |
|---|---|
| `.cursor/skills/analyze-english-sentence/SKILL.md` | 分析格式与细则（技能本体） |
| `.cursor/rules/analyze-english-sentence.mdc` | 规则：遇到分析请求必须走上述技能 |

改版式或增删章节时，优先改 `SKILL.md`；规则文件只负责「必须走技能」，一般不用动。
