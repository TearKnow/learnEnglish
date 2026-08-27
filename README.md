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

## 课文抓取（bubeijuzi 等）

依赖：

```bash
pip install -r requirements-scraper.txt
```

**第一步：逐篇抓取**

```bash
python scripts/scrape_articles.py ^
  --url-template "https://www.bubeijuzi.com/nce/2/{n}" ^
  --start 1 --end 96 ^
  --output-dir output/nce2
```

也支持单个 URL（`--url`）或 URL 列表文件（`--url-file urls.txt`，每行一个）。

每篇保存为 JSON（含英文正文 `paragraphs`、中文译文 `paragraphs_cn`），并生成 `manifest.json` 清单。

**第二步：合并 PDF**

单册：

```bash
python scripts/merge_to_pdf.py ^
  --input-dir output/nce2 ^
  --output output/nce2/nce2.pdf ^
  --title "New Concept English Book 2"
```

三册合订（每课先英文后中文）：

```bash
python scripts/merge_to_pdf.py ^
  --input-dir output/nce2 --book-label "Book 2" ^
  --input-dir output/nce3 --book-label "Book 3" ^
  --input-dir output/nce4 --book-label "Book 4" ^
  --output output/nce2-4.pdf ^
  --title "New Concept English Books 2-4"
```

连续排版、可点击目录；`--no-chinese` 可只保留英文。

