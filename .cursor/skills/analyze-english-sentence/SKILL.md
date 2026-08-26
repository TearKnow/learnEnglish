---
name: analyze-english-sentence
description: >-
  Analyzes English sentences or paragraphs in a New Concept English study style:
  sentence pattern (SVO etc.), Chinese translation, slightly hard words/phrases
  with IPA, then a CET-4/CET-6/考研-style difficulty grade. Use when the user
  says 分析这句, 分析这段, 帮我分析, 按新概念分析, or pastes English and asks for
  vocabulary, sentence structure, or translation for learning.
---

# 英文句子学习分析（新概念风格）

用户给出英文句子或段落时，严格按以下顺序输出，不要调换章节顺序。

回复使用简体中文。

## 固定输出顺序

1. **原句**
2. **句型分析**
3. **翻译**
4. **稍难词汇 / 短语**
5. **难易度**

## 各节要求

### 1. 原句

原样给出用户提供的英文（可按句分段，不要改写）。

### 2. 句型分析

核心做法：**整句保持可读**；下行划线；**再下一行写出成分名**（主语 / 谓语…），这样不用靠记符号。不要把一句话拆成十多块。

固定写法：

1. **多句**：每句一个小节（可标【第 n 句】），小节之间空 **2～3 行**。
2. **每句三行一组**：
   - 第 1 行：英文（特长句可在主句 / 从句边界折行）
   - 第 2 行：划线（与上方字符一一对应）
   - 第 3 行：成分名，**左对齐到该成分第一个单词下方**（不要居中；标签可比划线短）
3. **符号只用半角**：`=` `-` `~` `.` `^`。禁止 `·` `─` 等。
4. **图例**（开头写一次）：`====主语  ----谓语  ~~~~宾语  ....状语  ^^^^定语`
5. **引导词** `that` / `which`：划线行留空，成分行仍可标「引导」。
6. 只点关键结构，不复述全文意思。

示例版式：

````
图例：====主语  ----谓语  ~~~~宾语  ....状语  ^^^^定语

【第 1 句】
结构：S + V + that 宾语从句

These augmented estimates indicate that the commonly cited forecast for hyperscaler capex of $794 billion
========================= --------      =================================================================
主语                      谓语     引导  从句主语
likely understates the total amount of global AI capex by around $200 billion.
...... ----------- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ .......................
状语   从句谓语     从句宾语                            程度状语


【第 2 句】
结构：状语 + S + V + O + 程度状语

At the same time, the $794 billion figure likely overstates the amount of US investment in AI by $200 billion.
................. ======================= ...... ---------- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ................
状语              主语                    状语   谓语       宾语                              程度状语
````

### 3. 翻译

- 给出准确、通顺的中文翻译。
- 一句英文对应一句（或自然分段的）中文；不要逐词生硬直译。

### 4. 稍难词汇 / 短语

- 只列**稍微有点难**的词或短语（中级偏上：专业词、固定搭配、易混义项、习语）。
- 跳过超基础词（a/the/is/of 等），除非在本句有特殊用法。
- **表格前先写一行词性图例**（固定写法，每段分析写一次即可）：

```
词性：n. 名词 | v. 动词 | adj. 形容词 | adv. 副词 | prep. 介词 | conj. 连词 | phr. 短语/搭配
```

  若本段用到其他标注，可临时补在同行末尾（如 `pron. 代词`、`num. 数词`），不必每次把全部词类写全。
- 用表格：`词/短语 | 音标 | 词性 | 释义`（**词性列标本句用法**）。
- 词性写法：
  - 单词用缩写：`n.` / `v.` / `adj.` / `adv.` 等。
  - 短语、固定搭配用 `phr.`；若短语核心是动词结构，也可写 `v. phr.`（如 `lie in`、`blind sb to sth`）。
  - 一词多性时，**只标本句实际用法**；必要时在释义里补一句「亦可作…」。
  - 分词作定语时：按句法功能标 `adj.`（或 `adj.（分词）`），不要只标成 `v.`。
- 音标用 IPA，单词写英式或美式均可，前后用斜杠包住（如 `/əˈdʒʌst/`）；短语可标核心词，或按意群分词标注。
- 释义简洁，必要时补一句本句中的含义。
- 专有名词、缩写（如 capex）要解释；缩写可写拼读或展开词的音标；词性一般标 `n.`。
- **非原形时补时态/词形**（仅对收入表中的动词、以及明显变形且值得记的形容词/分词）：
  - 在释义里先标明**本句中的形式**（如：过去式 / 过去分词 / 现在分词 / 第三人称单数 / 被动等）。
  - 再紧跟一行或同格内列出常用全套：原形、第三人称单数、过去式、过去分词、现在分词（不规则动词务必写全）。
  - 词已是原形、或变形极常规且无学习价值时（如简单规则过去式且释义已够）可省略全套，但本句若出现 `adjusted` / `understates` / `cited` 这类，优先补全。
  - 写法示例（释义列内）：`本句：过去式。全套：adjust / adjusts / adjusted / adjusted / adjusting`

### 5. 难易度

放在全文**最后**。用国内常见考试档次给整段（或主句）定级，方便用户对照自己的水平。

**档次（由易到难，只选一档为主结论）：**

| 档次 | 大致对应 |
|---|---|
| 初中 | 中考英语 |
| 高中 | 高考英语 |
| 四级 | 大学英语四级 CET-4 |
| 六级 | 大学英语六级 CET-6 |
| 考研 | 考研英语（一/二）阅读难度 |
| 专八 / 高级 | 英语专业八级，或同等学术/外刊难度 |
| 专业阅读 | 明显超出考试：投行研报、学术论文、强领域术语 |

**写法（固定两行，可再加半句理由）：**

```
### 难易度
**六级偏上 / 考研阅读** — 句式不绕，但 `hyperscaler`、`capex` 等财经术语拉高门槛。
```

规则：

- 综合看：**词汇**（术语占比）、**句长与嵌套**、**语域**（日常 / 新闻 / 研报）。
- 主结论用加粗档次名；若介于两档，写成 `六级偏上`、`考研～专八` 等，不要列一长串考试名。
- 一段多句时给**整体**一档；只有某句明显难很多时可括号点一句。
- 默认简短（1～2 行），不要写成评分报告。

## 可选加料（仅当用户额外要求时）

- 更口语 / 更书面的改写
- 近义替换、造句练习
- 整句重音 / 连读提示（词汇表中的单词音标已默认给出，不必再单开一节）

默认不要主动加这些，保持核心结构干净。

## 示例

**用户：** 分析这句：Goldman Sachs Research adjusted the widely cited measures of US hyperscaler capex to produce a more comprehensive estimate.

**助手输出结构：**

### 原句
Goldman Sachs Research adjusted the widely cited measures of US hyperscaler capex to produce a more comprehensive estimate.

### 句型分析
图例：====主语  ----谓语  ~~~~宾语  ....状语  ^^^^定语

结构：S + V + O + to do…（目的）

```
Goldman Sachs Research adjusted the widely cited measures of US hyperscaler capex to produce a more comprehensive estimate.
====================== -------- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ........................................
主语                   谓语     宾语                                              目的状语
```

### 翻译
高盛研究部调整了此前被广泛引用的美国超大规模云厂商资本支出指标，以便得出更为全面的估算。

### 稍难词汇 / 短语

词性：n. 名词 | v. 动词 | adj. 形容词 | adv. 副词 | prep. 介词 | conj. 连词 | phr. 短语/搭配

| 词/短语 | 音标 | 词性 | 释义 |
|---|---|---|---|
| adjusted | `/əˈdʒʌstɪd/` | v. | 调整。本句：过去式。全套：adjust / adjusts / adjusted / adjusted / adjusting |
| widely cited | `/ˈwaɪdli saɪtɪd/` | adj.（分词） | 被广泛引用的。cited 本句：过去分词（作定语）。cite：cite / cites / cited / cited / citing |
| hyperscaler | `/ˈhaɪpəˌskeɪlə/` | n. | 超大规模云厂商 |
| capex | `/ˈkæpeks/` | n. | capital expenditure，资本支出 |

### 难易度
**六级偏上 / 考研阅读** — 主干清楚（S+V+O+目的状语），难点在 `hyperscaler`、`capex`、`widely cited measures` 等书面财经表达。
