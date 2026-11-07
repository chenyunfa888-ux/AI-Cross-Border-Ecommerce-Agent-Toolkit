#!/usr/bin/env python3
"""Deterministic narration timing and subtitle checks for short product videos."""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path

DEFAULT_WPS = 2.5
DEFAULT_SUBTITLE_MAX = 42
TOLERANCE = 0.15
TARGETS = {
    "tiktok12": (12.0, 1.5),
    "tiktok15": (15.0, 1.5),
    "tiktok20": (20.0, 1.5),
    "tiktok30": (30.0, 1.5),
    "shopee15": (15.0, 3.0),
    "shopee30": (30.0, 3.0),
    "mercadolivre15": (15.0, 3.0),
    "mercadolivre30": (30.0, 3.0),
}


def load_lines(path: str) -> list[tuple[int, str]]:
    source = Path(path)
    if not source.exists():
        raise SystemExit(f"[INPUT_MISSING] 找不到配音稿文件：{path}")
    rows = [
        (line_no, raw.strip())
        for line_no, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1)
        if raw.strip() and not raw.lstrip().startswith("#")
    ]
    if not rows:
        raise SystemExit(f"[INPUT_MISSING] {path} 没有有效台词。")
    return rows


def has_emoji(text: str) -> bool:
    return any(unicodedata.category(ch) in {"So", "Sk"} or ord(ch) >= 0x1F000 for ch in text)


def parse_target(raw: str | None) -> tuple[float | None, float]:
    if not raw:
        return None, 3.0
    key = raw.lower()
    if key in TARGETS:
        return TARGETS[key]
    try:
        return float(raw), 3.0
    except ValueError as exc:
        valid = ", ".join(sorted(TARGETS))
        raise SystemExit(f"[INPUT_INVALID] --target 应为秒数或：{valid}") from exc


def analyze(lines: list[tuple[int, str]], wps: float, subtitle_max: int, hook_window: float) -> dict:
    if wps <= 0 or subtitle_max <= 0 or hook_window <= 0:
        raise SystemExit("[INPUT_INVALID] wps、subtitle-max 和 hook-window 必须大于 0。")
    timeline, current, issues = [], 0.0, []
    for index, (source_line, text) in enumerate(lines, 1):
        words = len(text.split())
        duration = words / wps
        row = {
            "index": index,
            "source_line": source_line,
            "text": text,
            "words": words,
            "start": round(current, 2),
            "end": round(current + duration, 2),
            "duration": round(duration, 2),
            "subtitle_chars": len(text),
        }
        current += duration
        if len(text) > subtitle_max:
            issues.append(f"第 {index} 句字幕 {len(text)} 字符，超过 {subtitle_max}。")
        if has_emoji(text):
            issues.append(f"第 {index} 句疑似含 emoji/特殊符号。")
        timeline.append(row)

    max_hook_words = max(1, int(wps * hook_window))
    first = timeline[0]
    hook_passed = first["duration"] <= hook_window
    if not hook_passed:
        issues.append(
            f"第一句约 {first['duration']:.1f}s，超过钩子窗口 {hook_window:.1f}s；"
            f"建议不超过 {max_hook_words} 词。"
        )
    return {
        "rows": timeline,
        "total_seconds": round(current, 2),
        "hook_window": hook_window,
        "hook_max_words": max_hook_words,
        "hook_passed": hook_passed,
        "issues": issues,
    }


def check_target(total: float, target: float | None) -> dict | None:
    if target is None:
        return None
    low, high = target * (1 - TOLERANCE), target * (1 + TOLERANCE)
    return {
        "target": target,
        "window": [round(low, 2), round(high, 2)],
        "passed": low <= total <= high,
        "delta": round(total - target, 2),
    }


def markdown(result: dict, target: dict | None, wps: float, subtitle_max: int) -> str:
    lines = [
        "# 配音时长与字幕校验报告",
        "",
        f"- 语速：{wps} 词/秒",
        f"- 总时长：{result['total_seconds']:.1f}s",
        f"- 钩子窗口：{result['hook_window']:.1f}s（建议 ≤ {result['hook_max_words']} 词）",
        f"- 钩子：{'✅' if result['hook_passed'] else '❌'}",
        f"- 字幕单行上限：{subtitle_max} 字符",
    ]
    if target:
        lines.append(f"- 目标：{target['target']:.0f}s，允许 {target['window'][0]:.1f}–{target['window'][1]:.1f}s → {'✅' if target['passed'] else '❌'}")
    lines += ["", "| # | 时间 | 词数 | 字符 | 台词 |", "|---|---|---:|---:|---|"]
    for row in result["rows"]:
        excerpt = row["text"].replace("|", "\\|")
        lines.append(f"| {row['index']} | {row['start']:.1f}–{row['end']:.1f}s | {row['words']} | {row['subtitle_chars']} | {excerpt} |")
    lines += ["", "## 需要处理"]
    lines += [f"- {issue}" for issue in result["issues"]] or ["- 无 ✅"]
    lines += ["", "> 词数模型不能替代实际配音试听；正式交付按真实音频回听校正。"]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="短视频配音时长、钩子和字幕确定性校验")
    parser.add_argument("--script", required=True)
    parser.add_argument("--target")
    parser.add_argument("--wps", type=float, default=DEFAULT_WPS)
    parser.add_argument("--subtitle-max", type=int, default=DEFAULT_SUBTITLE_MAX)
    parser.add_argument("--hook-window", type=float, help="钩子首句秒数；TikTok target 默认 1.5，其余默认 3.0")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    target_seconds, default_hook_window = parse_target(args.target)
    hook_window = args.hook_window if args.hook_window is not None else default_hook_window
    result = analyze(load_lines(args.script), args.wps, args.subtitle_max, hook_window)
    target = check_target(result["total_seconds"], target_seconds)
    payload = {"analysis": result, "target_check": target}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else markdown(result, target, args.wps, args.subtitle_max))
    if not result["hook_passed"] or (target and not target["passed"]):
        sys.exit(1)


if __name__ == "__main__":
    main()

