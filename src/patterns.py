"""教育 SRC 场景密码模式 — 按常人习惯 curated，避免无意义笛卡尔积。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PatternGroup:
    id: str
    label: str
    description: str
    patterns: list[str]
    default_enabled: bool = False


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# ── 姓名 + 生日 ─────────────────────────────────────────────
_NAME_BIRTH = _dedupe([
    # 全拼 + 完整日期 / 年份
    "{name_full}{birth_full}",
    "{name_full}{birth_short}",
    "{name_full}{birth_year}",
    "{name_full_cap}{birth_full}",
    "{name_full_cap}{birth_short}",
    "{name_full_cap}{birth_year}",
    "{name_first_cap}{birth_full}",
    "{name_first_cap}{birth_short}",
    "{name_first_cap}{birth_year}",
    "{name_full_upper}{birth_full}",
    "{name_full_upper}{birth_short}",
    "{name_full_upper}{birth_year}",
    # 首字母 + 完整日期 / 年份（如 zs20060708）
    "{name_initials}{birth_full}",
    "{name_initials}{birth_short}",
    "{name_initials}{birth_year}",
    "{name_initials_upper}{birth_full}",
    "{name_initials_upper}{birth_short}",
    "{name_initials_upper}{birth_year}",
    "{name_initials_cap}{birth_full}",
    "{name_initials_cap}{birth_short}",
    "{name_initials_cap}{birth_year}",
    # 少量常见分隔符
    "{name_full}_{birth_full}",
    "{name_full}.{birth_full}",
    "{name_full}_{birth_year}",
    "{name_initials}_{birth_full}",
    "{name_initials}_{birth_year}",
])

# ── 生日 + 姓名 ─────────────────────────────────────────────
_BIRTH_NAME = _dedupe([
    "{birth_full}{name_full}",
    "{birth_short}{name_full}",
    "{birth_year}{name_full}",
    "{birth_full}{name_full_cap}",
    "{birth_short}{name_full_cap}",
    "{birth_year}{name_full_cap}",
    "{birth_full}{name_full_upper}",
    "{birth_short}{name_full_upper}",
    "{birth_year}{name_full_upper}",
    "{birth_full}{name_first_cap}",
    "{birth_short}{name_first_cap}",
    "{birth_year}{name_first_cap}",
    "{birth_full}{name_initials}",
    "{birth_short}{name_initials}",
    "{birth_year}{name_initials}",
    "{birth_full}{name_initials_upper}",
    "{birth_short}{name_initials_upper}",
    "{birth_year}{name_initials_upper}",
    "{birth_full}{name_initials_cap}",
    "{birth_short}{name_initials_cap}",
    "{birth_year}{name_initials_cap}",
])

# ── 纯姓名 ──────────────────────────────────────────────────
_NAME_ONLY = _dedupe([
    "{name_full}",
    "{name_full_cap}",
    "{name_first_cap}",
    "{name_initials}",
    "{name_initials_upper}",
    "{name_full}123",
    "{name_full}123456",
    "{name_initials}123",
])

# ── 纯生日 ────────────────────────────────────────────────────
_BIRTH_ONLY = [
    "{birth_full}",
    "{birth_short}",
    "{birth_year}",
]

# ── 学号 ──────────────────────────────────────────────────────
_STUDENT_ID = _dedupe([
    "{sid}",
    "{sid_last6}",
    "{sid_last8}",
    "{sid}123",
    "{sid}@123",
    "{sid_last6}123",
    "{sid}{birth_year}",
    "{sid}{birth_full}",
])

# ── 手机号 ────────────────────────────────────────────────────
_PHONE = _dedupe([
    "{phone}",
    "{name_full}{phone}",
    "{name_full_cap}{phone}",
    "{name_full_upper}{phone}",
    "{name_first_cap}{phone}",
    "{name_initials}{phone}",
    "{name_initials_upper}{phone}",
    "{name_initials_cap}{phone}",
    "{phone}{name_full}",
    "{phone}{name_initials}",
])

# ── 学号 + 生日 ───────────────────────────────────────────────
_SID_BIRTH = _dedupe([
    "{sid}{birth_full}",
    "{sid}{birth_short}",
    "{sid}{birth_year}",
    "{sid_last6}{birth_year}",
    "{sid_last6}{birth_full}",
])

# ── 学号 + 姓名 ───────────────────────────────────────────────
_SID_NAME = _dedupe([
    "{sid}{name_full}",
    "{sid}{name_initials}",
    "{name_full}{sid}",
    "{name_initials}{sid}",
    "{sid_last6}{name_full}",
])

# ── 身份证 / 邮箱 ─────────────────────────────────────────────
_IDCARD_EMAIL = _dedupe([
    "{idcard_last6}",
    "{idcard_last6}123",
    "{name_full}{idcard_last6}",
    "{email_prefix}",
    "{email_prefix}123",
    "{email_prefix}{birth_year}",
])

# ── 分隔符变体（精简） ────────────────────────────────────────
_SEPARATORS = _dedupe([
    "{name_full}_{birth_full}",
    "{name_full}.{birth_full}",
    "{name_full}-{birth_year}",
    "{name_full}_{birth_short}",
    "{name_full}_{birth_year}",
    "{name_full_cap}_{birth_full}",
    "{name_full_cap}.{birth_full}",
    "{name_full_cap}-{birth_year}",
    "{name_full_cap}_{birth_short}",
    "{name_full_cap}_{birth_year}",
    "{name_full_upper}_{birth_full}",
    "{name_full_upper}.{birth_full}",
    "{name_full_upper}-{birth_year}",
    "{name_first_cap}_{birth_full}",
    "{name_first_cap}.{birth_full}",
    "{name_first_cap}-{birth_year}",
    "{name_initials}_{birth_full}",
    "{name_initials}.{birth_full}",
    "{name_initials}-{birth_year}",
    "{name_initials_upper}_{birth_full}",
    "{name_initials_upper}.{birth_full}",
    "{name_initials_upper}-{birth_year}",
    "{name_initials_cap}_{birth_full}",
    "{name_initials_cap}.{birth_full}",
    "{name_initials_cap}-{birth_year}",
])

# ── 后缀变体（丰富） ──────────────────────────────────────────
_SUFFIX = _dedupe([
    # 姓名+生日+符号后缀
    "{name_full}{birth_full}!",
    "{name_full}{birth_short}!",
    "{name_full}{birth_year}!",
    "{name_full_cap}{birth_full}!",
    "{name_full_cap}{birth_short}!",
    "{name_full_cap}{birth_year}!",
    "{name_full_upper}{birth_full}!",
    "{name_full_upper}{birth_short}!",
    "{name_full_upper}{birth_year}!",
    "{name_first_cap}{birth_full}!",
    "{name_first_cap}{birth_short}!",
    "{name_first_cap}{birth_year}!",
    
    "{name_initials}{birth_full}!",
    "{name_initials}{birth_short}!",
    "{name_initials}{birth_year}!",
    "{name_initials_upper}{birth_full}!",
    "{name_initials_upper}{birth_short}!",
    "{name_initials_upper}{birth_year}!",
    "{name_initials_cap}{birth_full}!",
    "{name_initials_cap}{birth_short}!",
    "{name_initials_cap}{birth_year}!",
    
    # 姓名+生日+@符号
    "{name_full}{birth_full}@",
    "{name_full}{birth_short}@",
    "{name_full}{birth_year}@",
    "{name_full_cap}{birth_full}@",
    "{name_full_cap}{birth_short}@",
    "{name_full_cap}{birth_year}@",
    "{name_full_upper}{birth_full}@",
    "{name_full_upper}{birth_short}@",
    "{name_full_upper}{birth_year}@",
    "{name_first_cap}{birth_full}@",
    "{name_first_cap}{birth_short}@",
    "{name_first_cap}{birth_year}@",
    
    "{name_initials}{birth_full}@",
    "{name_initials}{birth_short}@",
    "{name_initials}{birth_year}@",
    "{name_initials_upper}{birth_full}@",
    "{name_initials_upper}{birth_short}@",
    "{name_initials_upper}{birth_year}@",
    "{name_initials_cap}{birth_full}@",
    "{name_initials_cap}{birth_short}@",
    "{name_initials_cap}{birth_year}@",
    
    # 姓名+生日+#符号
    "{name_full}{birth_full}#",
    "{name_full}{birth_short}#",
    "{name_full}{birth_year}#",
    "{name_full_cap}{birth_full}#",
    "{name_full_cap}{birth_short}#",
    "{name_full_cap}{birth_year}#",
    "{name_full_upper}{birth_full}#",
    "{name_full_upper}{birth_short}#",
    "{name_full_upper}{birth_year}#",
    "{name_first_cap}{birth_full}#",
    "{name_first_cap}{birth_short}#",
    "{name_first_cap}{birth_year}#",
    
    "{name_initials}{birth_full}#",
    "{name_initials}{birth_short}#",
    "{name_initials}{birth_year}#",
    "{name_initials_upper}{birth_full}#",
    "{name_initials_upper}{birth_short}#",
    "{name_initials_upper}{birth_year}#",
    "{name_initials_cap}{birth_full}#",
    "{name_initials_cap}{birth_short}#",
    "{name_initials_cap}{birth_year}#",
    
    # 姓名+生日+$符号
    "{name_full}{birth_full}$",
    "{name_full}{birth_short}$",
    "{name_full}{birth_year}$",
    "{name_full_cap}{birth_full}$",
    "{name_full_cap}{birth_short}$",
    "{name_full_cap}{birth_year}$",
    "{name_full_upper}{birth_full}$",
    "{name_full_upper}{birth_short}$",
    "{name_full_upper}{birth_year}$",
    "{name_first_cap}{birth_full}$",
    "{name_first_cap}{birth_short}$",
    "{name_first_cap}{birth_year}$",
    
    "{name_initials}{birth_full}$",
    "{name_initials}{birth_short}$",
    "{name_initials}{birth_year}$",
    "{name_initials_upper}{birth_full}$",
    "{name_initials_upper}{birth_short}$",
    "{name_initials_upper}{birth_year}$",
    "{name_initials_cap}{birth_full}$",
    "{name_initials_cap}{birth_short}$",
    "{name_initials_cap}{birth_year}$",
    
    # 数字后缀
    "{name_full}{birth_full}123",
    "{name_full}{birth_short}123",
    "{name_full}{birth_year}123",
    "{name_full_cap}{birth_full}123",
    "{name_full_cap}{birth_short}123",
    "{name_full_cap}{birth_year}123",
    "{name_full_upper}{birth_full}123",
    "{name_full_upper}{birth_short}123",
    "{name_full_upper}{birth_year}123",
    "{name_first_cap}{birth_full}123",
    "{name_first_cap}{birth_short}123",
    "{name_first_cap}{birth_year}123",
    
    "{name_initials}{birth_full}123",
    "{name_initials}{birth_short}123",
    "{name_initials}{birth_year}123",
    "{name_initials_upper}{birth_full}123",
    "{name_initials_upper}{birth_short}123",
    "{name_initials_upper}{birth_year}123",
    "{name_initials_cap}{birth_full}123",
    "{name_initials_cap}{birth_short}123",
    "{name_initials_cap}{birth_year}123",
    
    # 更多数字后缀
    "{name_full}{birth_full}1234",
    "{name_full}{birth_full}123456",
    "{name_full}{birth_full}520",
    "{name_full}{birth_full}1314",
    "{name_full}{birth_full}0000",
    "{name_full}{birth_full}8888",
    "{name_full}{birth_full}6666",
    
    "{name_initials}{birth_full}1234",
    "{name_initials}{birth_full}123456",
    "{name_initials}{birth_full}520",
    "{name_initials}{birth_full}1314",
    "{name_initials}{birth_full}0000",
    "{name_initials}{birth_full}8888",
    "{name_initials}{birth_full}6666",
    
    # 生日+姓名+符号后缀
    "{birth_full}{name_full}!",
    "{birth_short}{name_full}!",
    "{birth_year}{name_full}!",
    "{birth_full}{name_full}@",
    "{birth_short}{name_full}@",
    "{birth_year}{name_full}@",
    "{birth_full}{name_full}#",
    "{birth_short}{name_full}#",
    "{birth_year}{name_full}#",
    "{birth_full}{name_full}$",
    "{birth_short}{name_full}$",
    "{birth_year}{name_full}$",
    
    # 生日+姓名+数字后缀
    "{birth_full}{name_full}123",
    "{birth_short}{name_full}123",
    "{birth_year}{name_full}123",
    "{birth_full}{name_full}1234",
    "{birth_short}{name_full}1234",
    "{birth_year}{name_full}1234",
    
    # 生日+姓名首字母+符号后缀
    "{birth_full}{name_initials}!",
    "{birth_short}{name_initials}!",
    "{birth_year}{name_initials}!",
    "{birth_full}{name_initials}@",
    "{birth_short}{name_initials}@",
    "{birth_year}{name_initials}@",
    "{birth_full}{name_initials}#",
    "{birth_short}{name_initials}#",
    "{birth_year}{name_initials}#",
    "{birth_full}{name_initials}$",
    "{birth_short}{name_initials}$",
    "{birth_year}{name_initials}$",
    
    # 生日+姓名首字母+数字后缀
    "{birth_full}{name_initials}123",
    "{birth_short}{name_initials}123",
    "{birth_year}{name_initials}123",
    
    # 身份证后6位+符号后缀
    "{idcard_last6}!",
    "{idcard_last6}@",
    "{idcard_last6}#",
    "{idcard_last6}$",
    
    # 身份证后6位+数字后缀
    "{idcard_last6}123",
    "{idcard_last6}1234",
    
    # 姓名+身份证后6位+符号后缀
    "{name_full}{idcard_last6}!",
    "{name_full}{idcard_last6}@",
    "{name_full}{idcard_last6}#",
    "{name_full}{idcard_last6}$",
    "{name_initials}{idcard_last6}!",
    "{name_initials}{idcard_last6}@",
    "{name_initials}{idcard_last6}#",
    "{name_initials}{idcard_last6}$",
    
    # 姓名+身份证后6位+数字后缀
    "{name_full}{idcard_last6}123",
    "{name_initials}{idcard_last6}123",
    
    # 手机号+符号后缀
    "{phone}!",
    "{phone}@",
    "{phone}#",
    "{phone}$",
    
    # 手机号+数字后缀
    "{phone}123",
    "{phone}1234",
    
    # 姓名+手机号+符号后缀
    "{name_full}{phone}!",
    "{name_full}{phone}@",
    "{name_full}{phone}#",
    "{name_full}{phone}$",
    "{name_initials}{phone}!",
    "{name_initials}{phone}@",
    "{name_initials}{phone}#",
    "{name_initials}{phone}$",
    
    # 姓名+手机号+数字后缀
    "{name_full}{phone}123",
    "{name_initials}{phone}123",
])

PATTERN_GROUPS: list[PatternGroup] = [
    PatternGroup(
        id="name_birth",
        label="姓名拼音 + 生日",
        description="全拼/首字母 + 完整生日或四位年份（最常见）",
        patterns=_NAME_BIRTH,
        default_enabled=True,
    ),
    PatternGroup(
        id="birth_name",
        label="生日 + 姓名拼音",
        description="完整生日/年份在前，姓名在后",
        patterns=_BIRTH_NAME,
        default_enabled=False,
    ),
    PatternGroup(
        id="birth_only",
        label="纯生日 / 年份",
        description="完整生日、六位或四位年份",
        patterns=_BIRTH_ONLY,
        default_enabled=False,
    ),
    PatternGroup(
        id="student_id",
        label="学号相关",
        description="学号单独或与生日/姓名组合",
        patterns=_STUDENT_ID + _SID_BIRTH + _SID_NAME,
        default_enabled=True,
    ),
    PatternGroup(
        id="phone",
        label="手机号相关",
        description="完整手机号或姓名+手机号",
        patterns=_PHONE,
        default_enabled=False,
    ),
    PatternGroup(
        id="idcard_email",
        label="身份证 / 邮箱",
        description="身份证后六位、邮箱前缀",
        patterns=_IDCARD_EMAIL,
        default_enabled=False,
    ),
    PatternGroup(
        id="separators",
        label="带分隔符组合",
        description="下划线、点号等少量常见分隔",
        patterns=_SEPARATORS,
        default_enabled=False,
    ),
    PatternGroup(
        id="suffix_variants",
        label="常见后缀变体",
        description="! @ 123 等后缀",
        patterns=_SUFFIX,
        default_enabled=False,
    ),
]


def get_all_group_ids() -> list[str]:
    return [g.id for g in PATTERN_GROUPS]


def get_default_enabled_ids() -> set[str]:
    return {g.id for g in PATTERN_GROUPS if g.default_enabled}


def get_default_group_id() -> str:
    defaults = get_default_enabled_ids()
    if defaults:
        return next(iter(defaults))
    return PATTERN_GROUPS[0].id
