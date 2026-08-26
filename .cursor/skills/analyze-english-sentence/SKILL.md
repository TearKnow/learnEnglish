---
name: analyze-english-sentence
description: >-
  Analyzes English sentences or paragraphs in a New Concept English study style:
  sentence pattern (SVO etc.), Chinese translation, then slightly hard
  words/phrases with IPA. Use when the user says 分析这句, 分析这段, 帮我分析,
  按新概念分析, or pastes English and asks for vocabulary, sentence structure,
  or translation for learning.
---

# 英文句子学习分析（新概念风格）

用户给出英文句子或段落时，严格按以下顺序输出，不要调换章节顺序。

回复使用简体中文。

## 固定输出顺序

1. **原句**
2. **句型分析**
3. **翻译**
4. **稍难词汇 / 短语**

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
- 用表格：`词/短语 | 音标 | 释义`。
- 音标用 IPA，单词写英式或美式均可，前后用斜杠包住（如 `/əˈdʒʌst/`）；短语可标核心词，或按意群分词标注。
- 释义简洁，必要时补一句本句中的含义。
- 专有名词、缩写（如 capex）要解释；缩写可写拼读或展开词的音标。
- **非原形时补时态/词形**（仅对收入表中的动词、以及明显变形且值得记的形容词/分词）：
  - 在释义里先标明**本句中的形式**（如：过去式 / 过去分词 / 现在分词 / 第三人称单数 / 被动等）。
  - 再紧跟一行或同格内列出常用全套：原形、第三人称单数、过去式、过去分词、现在分词（不规则动词务必写全）。
  - 词已是原形、或变形极常规且无学习价值时（如简单规则过去式且释义已够）可省略全套，但本句若出现 `adjusted` / `understates` / `cited` 这类，优先补全。
  - 写法示例（释义列内）：`本句：过去式。全套：adjust / adjusts / adjusted / adjusted / adjusting`

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

| 词/短语 | 音标 | 释义 |
|---|---|---|
| adjusted | `/əˈdʒʌstɪd/` | 调整。本句：过去式。全套：adjust / adjusts / adjusted / adjusted / adjusting |
| widely cited | `/ˈwaɪdli saɪtɪd/` | 被广泛引用的。cited 本句：过去分词（作定语）。cite：cite / cites / cited / cited / citing |
| hyperscaler | `/ˈhaɪpəˌskeɪlə/` | 超大规模云厂商 |
| capex | `/ˈkæpeks/` | capital expenditure，资本支出 |
