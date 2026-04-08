#!/usr/bin/env python3
"""
fetch_and_score.py — 抓取 HuggingFace Trending + arXiv 论文，关键词打分，输出 Top N。

零 token 消耗。纯 Python，无外部依赖。

Usage:
    python3 fetch_and_score.py                          # 当天
    python3 fetch_and_score.py --days 3                 # 过去 3 天
    python3 fetch_and_score.py --date 2026-04-07        # 指定日期
    python3 fetch_and_score.py --history /path/to/.history.json

Stderr: 进度日志。Stdout: JSON array。
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

# ── 加载配置 ──────────────────────────────────────────────────────────────

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

_CONFIG = load_config()

KEYWORDS = [kw.lower() for kw in _CONFIG["keywords"]]
ARXIV_CATEGORIES = _CONFIG["arxiv_categories"]
MIN_SCORE = _CONFIG["min_score"]
TOP_N = _CONFIG["top_n"]
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


# ── 打分 ───────────────────────────────────────────────────────────────────

def score_paper(paper: dict) -> int:
    """按 keyword 命中次数打分。标题命中 +3，摘要命中 +1。"""
    title_lower = paper["title"].lower()
    text = (title_lower + " " + paper["abstract"]).lower()
    score = 0
    for kw in KEYWORDS:
        if kw in title_lower:
            score += 3
        elif kw in text:
            score += 1
    return score


# ── 数据抓取 ───────────────────────────────────────────────────────────────

def fetch_url(url: str, timeout: int = 30) -> str:
    try:
        req = Request(url, headers={"User-Agent": "daily-papers-bot/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"  [WARN] fetch failed {url}: {e}", file=sys.stderr)
        return ""


def _parse_hf_item(item: dict, source: str) -> tuple[str, dict] | None:
    """解析单个 HF API 条目。返回 (arxiv_id, paper_dict) 或 None。"""
    p = item.get("paper", {})
    arxiv_id = p.get("id", "")
    if not arxiv_id:
        return None

    authors_raw = p.get("authors", [])
    if isinstance(authors_raw, list):
        names = []
        for a in authors_raw:
            if isinstance(a, dict):
                names.append(a.get("name", ""))
            elif isinstance(a, str):
                names.append(a)
        authors = ", ".join(n for n in names if n)
    else:
        authors = str(authors_raw)

    paper = {
        "title": p.get("title", ""),
        "authors": authors,
        "abstract": p.get("summary", ""),
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "date": (p.get("publishedAt") or "")[:10],
        "score": 0,
        "source": source,
        "hf_upvotes": p.get("upvotes", 0),
    }
    paper["score"] = score_paper(paper)
    # upvote scaling: ≥50 → must read (inf), <50 → score × (1 + upvotes/10)
    upvotes = paper.get("hf_upvotes", 0) or 0
    if upvotes >= 50:
        paper["score"] = 9999
    elif upvotes > 0:
        paper["score"] = int(paper["score"] * (1 + upvotes / 10))
    return arxiv_id, paper


def fetch_hf_papers(start_date, end_date) -> list[dict]:
    """抓取 HF Daily（逐天）+ HF Trending（一次，过滤旧论文）。"""
    papers = {}

    # HF Daily：逐天抓取
    d = start_date
    while d <= end_date:
        date_str = d.isoformat()
        endpoint = f"https://huggingface.co/api/daily_papers?date={date_str}&limit=100"
        print(f"  Fetching hf-daily {date_str}...", file=sys.stderr)
        raw = fetch_url(endpoint)
        if raw:
            try:
                items = json.loads(raw)
            except json.JSONDecodeError:
                items = []
            for item in items:
                result = _parse_hf_item(item, "hf-daily")
                if result:
                    aid, paper = result
                    if aid not in papers or paper["score"] > papers[aid]["score"]:
                        papers[aid] = paper
        d += timedelta(days=1)

    # HF Trending：一次抓取
    endpoint = "https://huggingface.co/api/daily_papers?sort=trending&limit=50"
    print(f"  Fetching hf-trending...", file=sys.stderr)
    raw = fetch_url(endpoint)
    if raw:
        try:
            items = json.loads(raw)
        except json.JSONDecodeError:
            items = []
        for item in items:
            result = _parse_hf_item(item, "hf-trending")
            if result:
                aid, paper = result
                if aid not in papers or paper["score"] > papers[aid]["score"]:
                    papers[aid] = paper

    result = list(papers.values())
    print(f"  HF: {len(result)} papers", file=sys.stderr)
    return result


def fetch_arxiv_papers(start_date, end_date, days: int = 1) -> list[dict]:
    max_results = min(400 * days, 3000)
    cats = "+OR+".join(f"cat:{c}" for c in ARXIV_CATEGORIES)
    url = (
        f"https://export.arxiv.org/api/query?"
        f"search_query=({cats})"
        f"&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    )

    timeout = max(60, 30 * days)
    print(f"  Fetching arXiv (max_results={max_results}, timeout={timeout}s)...", file=sys.stderr)
    xml_text = fetch_url(url, timeout=timeout)
    if not xml_text:
        return []

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"  [WARN] arXiv XML parse error: {e}", file=sys.stderr)
        return []

    papers = []
    filtered_by_date = 0
    for entry in root.findall("atom:entry", ATOM_NS):
        title_el = entry.find("atom:title", ATOM_NS)
        summary_el = entry.find("atom:summary", ATOM_NS)
        published_el = entry.find("atom:published", ATOM_NS)
        id_el = entry.find("atom:id", ATOM_NS)

        if title_el is None or summary_el is None:
            continue

        title = " ".join(title_el.text.split())
        abstract = " ".join(summary_el.text.split())
        entry_url = id_el.text.strip() if id_el is not None else ""
        date = published_el.text[:10] if published_el is not None else ""
        arxiv_id = entry_url.split("/abs/")[-1] if "/abs/" in entry_url else ""

        # 多天模式按日期过滤（单天模式不过滤，因为 arXiv 日期常有偏差）
        if days > 1 and start_date and end_date and date:
            try:
                pub_date = datetime.strptime(date, "%Y-%m-%d").date()
                if pub_date < start_date or pub_date > end_date:
                    filtered_by_date += 1
                    continue
            except ValueError:
                pass

        author_els = entry.findall("atom:author", ATOM_NS)
        names = []
        for a in author_els:
            name_el = a.find("atom:name", ATOM_NS)
            if name_el is not None and name_el.text:
                names.append(name_el.text.strip())

        cat_el = entry.find("arxiv:primary_category", ATOM_NS)

        paper = {
            "title": title,
            "authors": ", ".join(names),
            "abstract": abstract,
            "url": entry_url,
            "date": date,
            "score": 0,
            "source": "arxiv",
        }
        paper["score"] = score_paper(paper)
        if paper["score"] >= 0:
            papers.append(paper)

    print(
        f"  arXiv: {len(papers)} papers"
        f" (from {len(papers) + filtered_by_date} parsed, {filtered_by_date} filtered by date)",
        file=sys.stderr,
    )
    return papers


# ── 合并去重 ──────────────────────────────────────────────────────────────

def extract_arxiv_id(url: str) -> str:
    m = re.search(r"(\d{4}\.\d{4,5})", url)
    return m.group(1) if m else ""


def load_history(path: Path) -> list[dict]:
    if path and path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            pass
    return []


def update_history(history_path: Path, papers: dict[str, dict], target_date) -> None:
    """将本次推荐论文追加到 history，保留最近 30 天记录。"""
    if not history_path:
        return

    history = load_history(history_path)
    existing = {h["id"]: h for h in history if "id" in h}

    today_str = target_date.isoformat() if hasattr(target_date, "isoformat") else str(target_date)
    added = 0
    for aid, p in papers.items():
        if aid not in existing:
            existing[aid] = {"id": aid, "date": today_str, "title": p["title"]}
            added += 1
        # 同一 ID 已存在 → 保留最早 date（不覆盖）

    # 只保留最近 30 天
    cutoff = (datetime.now().date() - timedelta(days=30)).isoformat()
    records = [r for r in existing.values() if r.get("date", "") >= cutoff]

    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  History updated: +{added} new, {len(records)} total (30-day window)", file=sys.stderr)


def merge_and_rank(
    hf_papers: list[dict],
    arxiv_papers: list[dict],
    target_date,
    history_path: Path | None,
    days: int = 1,
    top_n: int = TOP_N,
) -> list[dict]:
    # 按 arXiv ID 合并，保留高分
    by_id: dict[str, dict] = {}
    for p in hf_papers + arxiv_papers:
        aid = extract_arxiv_id(p["url"])
        if not aid:
            continue
        if aid not in by_id or p["score"] > by_id[aid]["score"]:
            by_id[aid] = p

    print(f"  Merged: {len(by_id)} unique papers", file=sys.stderr)

    # 多天模式跳过历史去重
    if days > 1:
        print(f"  Multi-day mode (days={days}): skipping history dedup", file=sys.stderr)
    else:
        # 单天模式：历史去重
        history = load_history(history_path)
        history_ids = {h["id"] for h in history if "id" in h}
        before = len(by_id)
        by_id = {aid: p for aid, p in by_id.items() if aid not in history_ids}
        removed = before - len(by_id)
        if removed:
            print(f"  History dedup: removed {removed}", file=sys.stderr)

    # 过滤 + 排序
    candidates = [p for p in by_id.values() if p["score"] >= MIN_SCORE]
    candidates.sort(key=lambda x: x["score"], reverse=True)
    top = candidates[:top_n]
    print(f"  Final: {len(top)} papers", file=sys.stderr)
    return top


# ── 主入口 ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch and score daily papers")
    parser.add_argument("--date", help="Target date YYYY-MM-DD (default: today)")
    parser.add_argument("--days", type=int, default=1, help="Number of days to fetch")
    parser.add_argument("--history", help="Path to .history.json for dedup")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    target_date = (
        datetime.strptime(args.date, "%Y-%m-%d").date()
        if args.date
        else datetime.now().date()
    )
    days = max(1, args.days)
    start_date = target_date - timedelta(days=days - 1)
    top_n = min(TOP_N * days, 100)

    history_path = Path(args.history) if args.history else None

    is_weekend = target_date.weekday() >= 5
    print(
        f"[fetch_and_score] {target_date} ({'weekend' if is_weekend else 'weekday'})"
        + (f", days={days} [{start_date} ~ {target_date}], top_n={top_n}" if days > 1 else ""),
        file=sys.stderr,
    )

    hf_papers = fetch_hf_papers(start_date, target_date)
    arxiv_papers = fetch_arxiv_papers(start_date, target_date, days)
    top = merge_and_rank(hf_papers, arxiv_papers, target_date, history_path, days=days, top_n=top_n)

    # 记录 top-n 到 history
    if history_path:
        top_by_id = {}
        for p in top:
            aid = extract_arxiv_id(p["url"])
            if aid:
                top_by_id[aid] = p
        update_history(history_path, top_by_id, target_date)

    output = json.dumps(top, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"  Output written to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(output)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
