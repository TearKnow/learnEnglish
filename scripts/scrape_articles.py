#!/usr/bin/env python3
"""抓取 bubeijuzi 等结构相同的课文页面，保存为 JSON。"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path
from typing import Iterable

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("缺少依赖：pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

USER_AGENT = "learnEnglish-scraper/1.0 (+local study tool)"
DEFAULT_DELAY = 0.5


def fetch_html(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def extract_paragraphs(article_el) -> list[str]:
    paragraphs = [
        unescape(p.get_text(" ", strip=True))
        for p in article_el.find_all("p")
        if p.get_text(strip=True)
    ]
    if paragraphs:
        return paragraphs
    text = unescape(article_el.get_text("\n", strip=True))
    return [text] if text else []


def parse_article(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    title_el = soup.select_one("#title-en")
    if not title_el:
        raise ValueError(f"未找到 #title-en: {url}")

    article_el = soup.select_one("#english-article article")
    if not article_el:
        raise ValueError(f"未找到 #english-article article: {url}")

    paragraphs = extract_paragraphs(article_el)
    if not paragraphs:
        raise ValueError(f"英文正文为空: {url}")

    cn_article_el = soup.select_one("#chinese-translation article")
    paragraphs_cn = extract_paragraphs(cn_article_el) if cn_article_el else []

    title_cn_el = soup.select_one("#title-cn")
    title_pos_el = soup.select_one("#title-pos")

    return {
        "url": url,
        "title_en": unescape(title_el.get_text(strip=True)),
        "title_cn": unescape(title_cn_el.get_text(strip=True)) if title_cn_el else "",
        "title_pos": unescape(title_pos_el.get_text(strip=True)) if title_pos_el else "",
        "paragraphs": paragraphs,
        "text": "\n\n".join(paragraphs),
        "paragraphs_cn": paragraphs_cn,
        "text_cn": "\n\n".join(paragraphs_cn),
    }


def slugify(title: str, fallback: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.strip().lower()).strip("-")
    return slug or fallback


def save_article(article: dict, output_dir: Path, index: int) -> Path:
    slug = slugify(article["title_en"], f"article-{index:03d}")
    filename = f"{index:03d}_{slug}.json"
    path = output_dir / filename
    payload = {"index": index, **article}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def expand_urls(args: argparse.Namespace) -> list[tuple[int, str]]:
    urls: list[tuple[int, str]] = []

    if args.url:
        urls.append((args.start_index, args.url))

    if args.url_template:
        for n in range(args.start, args.end + 1):
            urls.append((n, args.url_template.format(n=n, index=n)))

    if args.url_file:
        lines = Path(args.url_file).read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines, start=args.start_index):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append((i, line))

    # 去重，保留首次出现
    seen: set[str] = set()
    unique: list[tuple[int, str]] = []
    for index, url in urls:
        if url in seen:
            continue
        seen.add(url)
        unique.append((index, url))
    return unique


def scrape_one(url: str) -> dict:
    html = fetch_html(url)
    return parse_article(html, url)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="抓取页面中的 #title-en 标题与 #english-article article 正文。"
    )
    parser.add_argument("--url", help="单个页面 URL")
    parser.add_argument(
        "--url-template",
        help="URL 模板，可用 {n} 或 {index}，例如 https://www.bubeijuzi.com/nce/2/{n}",
    )
    parser.add_argument("--url-file", help="每行一个 URL 的文本文件")
    parser.add_argument("--start", type=int, default=1, help="模板起始编号（含）")
    parser.add_argument("--end", type=int, default=96, help="模板结束编号（含）")
    parser.add_argument(
        "--start-index",
        type=int,
        default=1,
        help="单 URL / URL 文件模式下的起始序号",
    )
    parser.add_argument(
        "--output-dir",
        default="output/articles",
        help="输出目录，默认 output/articles",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help=f"请求间隔秒数，默认 {DEFAULT_DELAY}",
    )
    parser.add_argument(
        "--manifest",
        default="manifest.json",
        help="清单文件名，默认 manifest.json",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not any([args.url, args.url_template, args.url_file]):
        parser.error("请至少提供 --url、--url-template 或 --url-file 之一")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    targets = expand_urls(args)
    manifest: list[dict] = []
    failed: list[dict] = []

    print(f"共 {len(targets)} 个 URL，输出到 {output_dir.resolve()}")

    for i, (index, url) in enumerate(targets):
        if i > 0 and args.delay > 0:
            time.sleep(args.delay)

        try:
            article = scrape_one(url)
            path = save_article(article, output_dir, index)
            manifest.append(
                {
                    "index": index,
                    "file": path.name,
                    "title_en": article["title_en"],
                    "url": url,
                }
            )
            print(f"[{index:03d}] OK  {article['title_en']}")
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError, TimeoutError) as exc:
            failed.append({"index": index, "url": url, "error": str(exc)})
            print(f"[{index:03d}] FAIL {url} -> {exc}", file=sys.stderr)

    manifest_path = output_dir / args.manifest
    manifest_path.write_text(
        json.dumps(
            {
                "source": "scrape_articles.py",
                "count": len(manifest),
                "articles": sorted(manifest, key=lambda item: item["index"]),
                "failed": failed,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\n完成：成功 {len(manifest)}，失败 {len(failed)}")
    print(f"清单：{manifest_path.resolve()}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
