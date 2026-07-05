"""姓名转拼音及常见变体。"""

from __future__ import annotations

from pypinyin import Style, lazy_pinyin


def name_to_variants(name: str) -> dict[str, list[str]]:
    """将中文姓名转为拼音变体，各键对应独立变体（不混用）。"""
    empty: dict[str, list[str]] = {
        "name_full": [],
        "name_full_cap": [],
        "name_full_upper": [],
        "name_first_cap": [],
        "name_initials": [],
        "name_initials_upper": [],
        "name_initials_cap": [],
    }
    name = name.strip()
    if not name:
        return empty

    syllables = lazy_pinyin(name, style=Style.NORMAL, errors="ignore")
    syllables = [s for s in syllables if s]
    if not syllables:
        return empty

    full_lower = "".join(syllables)
    full_cap = "".join(s.capitalize() for s in syllables)
    full_upper = full_lower.upper()
    first_cap = syllables[0].capitalize() + "".join(syllables[1:]) if len(syllables) > 1 else full_cap
    initials_lower = "".join(s[0] for s in syllables if s)
    initials_upper = initials_lower.upper()
    initials_cap = initials_lower.capitalize()

    return {
        "name_full": [full_lower],
        "name_full_cap": [full_cap],
        "name_full_upper": [full_upper],
        "name_first_cap": _unique([first_cap, full_cap]),
        "name_initials": [initials_lower],
        "name_initials_upper": [initials_upper],
        "name_initials_cap": [initials_cap],
    }


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result
