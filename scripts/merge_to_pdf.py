#!/usr/bin/env python3
"""将 scrape_articles.py 输出的 JSON 合并为一个 PDF。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

try:
    from fpdf import FPDF
except ImportError:
    print("缺少依赖：pip install fpdf2", file=sys.stderr)
    sys.exit(1)


def find_unicode_font() -> Path | None:
    candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\msyhbd.ttc"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


class ArticlePDF(FPDF):
    def __init__(self, unicode_font: Path | None = None) -> None:
        super().__init__(format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)
        self.body_font = "Helvetica"
        self.heading_font = "Helvetica"
        self.meta_font = "Helvetica"

        if unicode_font:
            self.add_font("Uni", "", str(unicode_font))
            self.add_font("Uni", "B", str(unicode_font))
            self.body_font = "Uni"
            self.heading_font = "Uni"
            self.meta_font = "Uni"

    def write_cover(self, title: str, count: int) -> None:
        self.set_font(self.heading_font, "B", 22)
        self.multi_cell(0, 12, title)
        self.ln(4)
        self.set_font(self.meta_font, "", 11)
        self.set_text_color(90, 90, 90)
        self.multi_cell(0, 6, f"{count} articles")
        self.set_text_color(0, 0, 0)
        self.ln(8)

    def write_book_heading(self, text: str) -> None:
        if self.get_y() > self.h - self.b_margin - 48:
            self.add_page()
        self.set_font(self.heading_font, "B", 18)
        self.multi_cell(0, 10, text)
        self.ln(4)

    def write_heading(self, text: str, size: int = 14) -> None:
        if self.get_y() > self.h - self.b_margin - 36:
            self.add_page()
        self.set_font(self.heading_font, "B", size)
        self.multi_cell(0, 8, text)
        self.ln(2)

    def write_subheading(self, text: str) -> None:
        self.set_font(self.heading_font, "B", 11)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 7, text)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def write_paragraph(self, text: str) -> None:
        self.set_font(self.body_font, "", 11)
        self.multi_cell(0, 6.5, text)
        self.ln(2)

    def write_separator(self, blank_lines: int = 3) -> None:
        self.ln(blank_lines * 6)


def load_articles(input_dir: Path, manifest_name: str) -> list[dict]:
    manifest_path = input_dir / manifest_name
    articles: list[dict] = []

    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for item in manifest.get("articles", []):
            file_path = input_dir / item["file"]
            if not file_path.exists():
                raise FileNotFoundError(f"manifest 指向的文件不存在: {file_path}")
            articles.append(json.loads(file_path.read_text(encoding="utf-8")))
        return sorted(articles, key=lambda article: article.get("index", 0))

    for file_path in sorted(input_dir.glob("*.json")):
        if file_path.name == manifest_name:
            continue
        articles.append(json.loads(file_path.read_text(encoding="utf-8")))
    return sorted(articles, key=lambda article: article.get("index", 0))


def load_book_groups(
    input_dirs: list[Path],
    book_labels: list[str] | None,
    manifest_name: str,
) -> list[tuple[str, list[dict]]]:
    groups: list[tuple[str, list[dict]]] = []
    for i, input_dir in enumerate(input_dirs):
        if not input_dir.exists():
            raise FileNotFoundError(f"输入目录不存在: {input_dir}")
        label = (
            book_labels[i]
            if book_labels and i < len(book_labels)
            else input_dir.name
        )
        groups.append((label, load_articles(input_dir, manifest_name)))
    return groups


def estimate_toc_pages(section_count: int, article_count: int, lines_per_page: int = 36) -> int:
    rows = section_count + article_count + 4
    return max(1, (rows + lines_per_page - 1) // lines_per_page)


def render_toc(pdf: ArticlePDF, outline) -> None:
    pdf.set_font(pdf.heading_font, "B", 16)
    pdf.multi_cell(0, 10, "Contents")
    pdf.ln(4)

    for section in outline:
        name = section.name if hasattr(section, "name") else section[1]
        page = section.page_number if hasattr(section, "page_number") else section[2]
        level = section.level if hasattr(section, "level") else 0

        link = pdf.add_link()
        pdf.set_link(link, page=page)

        indent = "    " * max(level, 0)
        title = f"{indent}{name}"
        page_str = str(page)
        pdf.set_x(pdf.l_margin)
        available = pdf.epw
        font_size = 12 if level == 0 else 10
        pdf.set_font(pdf.body_font, "B" if level == 0 else "", font_size)
        title_width = pdf.get_string_width(title) + 2
        page_width = pdf.get_string_width(page_str) + 1
        dots_width = max(available - title_width - page_width, 8)
        dots = "." * max(3, int(dots_width / max(pdf.get_string_width("."), 0.1)))

        line = f"{title} {dots} {page_str}"
        pdf.cell(0, 6.5 if level else 8, line, link=link, new_x="LMARGIN", new_y="NEXT")


def paragraphs_of(article: dict, en: bool = True) -> list[str]:
    if en:
        paragraphs = article.get("paragraphs")
        if not paragraphs:
            text = (article.get("text") or "").strip()
            return [text] if text else []
        return paragraphs

    paragraphs = article.get("paragraphs_cn")
    if not paragraphs:
        text = (article.get("text_cn") or "").strip()
        return [text] if text else []
    return paragraphs


def build_pdf(
    book_groups: list[tuple[str, list[dict]]],
    output_path: Path,
    title: str,
    font_path: Path | None,
    blank_lines: int,
    include_chinese: bool,
) -> None:
    total = sum(len(articles) for _, articles in book_groups)
    if total == 0:
        raise ValueError("没有可合并的文章")

    unicode_font = font_path or find_unicode_font()
    if include_chinese and not unicode_font:
        raise RuntimeError("需要中文内容，但未找到 Unicode 字体，请用 --font 指定")

    pdf = ArticlePDF(unicode_font=unicode_font)

    pdf.add_page()
    pdf.write_cover(title, total)

    toc_pages = estimate_toc_pages(len(book_groups), total)
    pdf.insert_toc_placeholder(render_toc, pages=toc_pages)

    first_article = True
    for book_label, articles in book_groups:
        if not first_article:
            pdf.write_separator(blank_lines + 1)
        pdf.start_section(book_label, level=0)
        pdf.write_book_heading(book_label)

        for article in articles:
            if not first_article:
                pdf.write_separator(blank_lines)
            first_article = False

            index = article.get("index", 0)
            heading = article.get("title_en") or f"Article {index}"
            label = f"{index}. {heading}"

            pdf.start_section(label, level=1)
            pdf.write_heading(label)

            for paragraph in paragraphs_of(article, en=True):
                pdf.write_paragraph(paragraph)

            if include_chinese:
                cn_paragraphs = paragraphs_of(article, en=False)
                if cn_paragraphs:
                    pdf.ln(3)
                    title_cn = article.get("title_cn") or "中文翻译"
                    pdf.write_subheading(title_cn)
                    for paragraph in cn_paragraphs:
                        pdf.write_paragraph(paragraph)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="合并 JSON 文章为一个 PDF。")
    parser.add_argument(
        "--input-dir",
        action="append",
        dest="input_dirs",
        help="scrape_articles.py 的输出目录，可重复传入多个目录",
    )
    parser.add_argument(
        "--book-label",
        action="append",
        dest="book_labels",
        help="与 --input-dir 对应的册标题，可重复传入",
    )
    parser.add_argument(
        "--manifest",
        default="manifest.json",
        help="清单文件名，默认 manifest.json",
    )
    parser.add_argument(
        "--output",
        default="output/merged.pdf",
        help="输出 PDF 路径，默认 output/merged.pdf",
    )
    parser.add_argument(
        "--title",
        default="Collected Articles",
        help="PDF 封面标题",
    )
    parser.add_argument(
        "--blank-lines",
        type=int,
        default=3,
        help="文章之间空行数，默认 3",
    )
    parser.add_argument(
        "--include-chinese",
        action="store_true",
        default=True,
        help="每课英文后附中文翻译（默认开启）",
    )
    parser.add_argument(
        "--no-chinese",
        action="store_true",
        help="不输出中文翻译",
    )
    parser.add_argument(
        "--font",
        help="自定义 TTF/TTC 字体路径",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    input_dirs = [Path(p) for p in (args.input_dirs or ["output/articles"])]
    book_groups = load_book_groups(input_dirs, args.book_labels, args.manifest)
    output_path = Path(args.output)
    build_pdf(
        book_groups,
        output_path,
        args.title,
        font_path=Path(args.font) if args.font else None,
        blank_lines=args.blank_lines,
        include_chinese=not args.no_chinese,
    )

    total = sum(len(articles) for _, articles in book_groups)
    print(f"已合并 {total} 篇文章 -> {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
