"""密码字典生成核心引擎。"""

from __future__ import annotations

import calendar
import re
from dataclasses import dataclass, field
from datetime import date

from .patterns import PATTERN_GROUPS
from .pinyin_utils import name_to_variants


@dataclass
class UserInfo:
    """用户已知信息，字段均为可选。"""

    name: str = ""
    student_id: str = ""
    phone: str = ""
    birth: str = ""  # 完整生日(YYYY-MM-DD)/仅年份
    idcard: str = ""  # 完整18位身份证号
    email: str = ""


@dataclass
class GenerateOptions:
    min_length: int = 4
    max_length: int = 32
    enabled_groups: set[str] = field(default_factory=set)
    include_reversed: bool = False
    deduplicate: bool = True
    brute_force_date: bool = False


class PasswordGenerator:
    PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")

    def __init__(self, info: UserInfo, options: GenerateOptions):
        self.info = info
        self.options = options
        self._tokens = self._build_tokens()

    def _normalize_digits(self, value: str) -> str:
        return re.sub(r"\D", "", value.strip())

    def _resolve_birth_parts(self) -> tuple[int | None, int | None, int | None]:
        """解析已知的年/月/日分量，支持完整生日、仅年份等多种格式。"""
        y = m = d = None
        
        # 优先从身份证解析（如果填写了身份证）
        idcard_raw = self._normalize_digits(self.info.idcard.strip())
        if len(idcard_raw) == 18:
            # 身份证第7-14位是生日
            y = int(idcard_raw[6:10])
            m = int(idcard_raw[10:12])
            d = int(idcard_raw[12:14])
        else:
            # 否则从birth字段解析
            birth_raw = self._normalize_digits(self.info.birth.strip())
            if birth_raw:
                # 检查是否是完整生日（8位）
                if len(birth_raw) == 8:
                    y, m, d = int(birth_raw[:4]), int(birth_raw[4:6]), int(birth_raw[6:8])
                # 检查是否是6位生日
                elif len(birth_raw) == 6:
                    y, m, d = 1900 + int(birth_raw[:2]), int(birth_raw[2:4]), int(birth_raw[4:6])
                    if y > date.today().year:
                        y -= 100
                # 仅年份（4位）
                elif len(birth_raw) == 4:
                    y = int(birth_raw)
                # 仅年份（2位）
                elif len(birth_raw) == 2:
                    y = 1900 + int(birth_raw)
                    if y > date.today().year:
                        y -= 100

        return y, m, d

    def _iter_candidate_dates(self) -> list[tuple[int, int, int]]:
        """根据已知信息返回待展开的具体日期列表。"""
        y, m, d = self._resolve_birth_parts()
        if y is None:
            return []

        if m is not None and d is not None:
            return [(y, m, d)]

        if not self.options.brute_force_date:
            return []

        if m is not None:
            last_day = calendar.monthrange(y, m)[1]
            return [(y, m, day) for day in range(1, last_day + 1)]

        dates: list[tuple[int, int, int]] = []
        for month in range(1, 13):
            last_day = calendar.monthrange(y, month)[1]
            for day in range(1, last_day + 1):
                dates.append((y, month, day))
        return dates

    def _parse_birth(self) -> dict[str, list[str]]:
        """解析生日相关 token，支持完整日期、分段填写与日期爆破。"""
        tokens: dict[str, list[str]] = {
            "birth_full": [],
            "birth_short": [],
            "birth_year": [],
            "birth_year2": [],
            "birth_md": [],
            "birth_md_short": [],
            "birth_ym": [],
            "birth_ym_short": [],
            "birth_month": [],
            "birth_month_short": [],
            "birth_day": [],
            "birth_day_short": [],
        }

        y, m, d = self._resolve_birth_parts()
        if y is None:
            return tokens

        tokens["birth_year"].append(f"{y:04d}")
        tokens["birth_year2"].append(f"{y % 100:02d}")

        dates = self._iter_candidate_dates()
        if dates:
            full_set: set[str] = set()
            short_set: set[str] = set()
            md_set: set[str] = set()
            md_short_set: set[str] = set()
            ym_set: set[str] = set()
            ym_short_set: set[str] = set()
            month_set: set[str] = set()
            month_short_set: set[str] = set()
            day_set: set[str] = set()
            day_short_set: set[str] = set()

            for dy, dm, dd in dates:
                full_set.add(f"{dy:04d}{dm:02d}{dd:02d}")
                short_set.add(f"{dy % 100:02d}{dm:02d}{dd:02d}")
                md_set.add(f"{dm:02d}{dd:02d}")
                md_short_set.add(f"{dm}{dd}")
                ym_set.add(f"{dy:04d}{dm:02d}")
                ym_short_set.add(f"{dy % 100:02d}{dm:02d}")
                month_set.add(f"{dm:02d}")
                month_short_set.add(f"{dm}")
                day_set.add(f"{dd:02d}")
                day_short_set.add(f"{dd}")

            tokens["birth_full"] = sorted(full_set)
            tokens["birth_short"] = sorted(short_set)
            tokens["birth_md"] = sorted(md_set)
            tokens["birth_md_short"] = sorted(md_short_set)
            tokens["birth_ym"] = sorted(ym_set)
            tokens["birth_ym_short"] = sorted(ym_short_set)
            tokens["birth_month"] = sorted(month_set)
            tokens["birth_month_short"] = sorted(month_short_set)
            tokens["birth_day"] = sorted(day_set)
            tokens["birth_day_short"] = sorted(day_short_set)
        elif m is not None and d is not None:
            tokens["birth_full"].append(f"{y:04d}{m:02d}{d:02d}")
            tokens["birth_short"].append(f"{y % 100:02d}{m:02d}{d:02d}")
            tokens["birth_md"].append(f"{m:02d}{d:02d}")
            tokens["birth_md_short"].append(f"{m}{d}")
            tokens["birth_ym"].append(f"{y:04d}{m:02d}")
            tokens["birth_ym_short"].append(f"{y % 100:02d}{m:02d}")
            tokens["birth_month"].append(f"{m:02d}")
            tokens["birth_month_short"].append(f"{m}")
            tokens["birth_day"].append(f"{d:02d}")
            tokens["birth_day_short"].append(f"{d}")
        elif m is not None:
            tokens["birth_month"].append(f"{m:02d}")
            tokens["birth_month_short"].append(f"{m}")
            tokens["birth_ym"].append(f"{y:04d}{m:02d}")
            tokens["birth_ym_short"].append(f"{y % 100:02d}{m:02d}")
        elif d is not None:
            tokens["birth_day"].append(f"{d:02d}")
            tokens["birth_day_short"].append(f"{d}")

        return tokens

    def _build_tokens(self) -> dict[str, list[str]]:
        tokens: dict[str, list[str]] = {}

        name_vars = name_to_variants(self.info.name)
        for key, values in name_vars.items():
            if values:
                tokens[key] = values

        sid = self._normalize_digits(self.info.student_id)
        if sid:
            tokens["sid"] = [sid]
            if len(sid) >= 4:
                tokens["sid_last4"] = [sid[-4:]]
            if len(sid) >= 6:
                tokens["sid_last6"] = [sid[-6:]]
            if len(sid) >= 8:
                tokens["sid_last8"] = [sid[-8:]]
            if len(sid) >= 4:
                tokens["sid_year"] = [sid[:4]]

        phone = self._normalize_digits(self.info.phone)
        if phone:
            tokens["phone"] = [phone]

        for k, v in self._parse_birth().items():
            if v:
                tokens[k] = v

        # 从完整身份证提取后6位
        idcard_raw = self._normalize_digits(self.info.idcard.strip())
        if len(idcard_raw) == 18:
            tokens["idcard_last6"] = [idcard_raw[-6:]]

        email = self.info.email.strip()
        if email and "@" in email:
            tokens["email_prefix"] = [email.split("@", 1)[0]]

        return tokens

    def _expand_pattern(self, pattern: str) -> list[str]:
        if "{" not in pattern:
            return [pattern]

        parts: list[list[str]] = []
        last = 0
        for match in self.PLACEHOLDER_RE.finditer(pattern):
            parts.append([pattern[last : match.start()]])
            key = match.group(1)
            values = self._tokens.get(key, [])
            if not values:
                return []
            parts.append(values)
            last = match.end()
        parts.append([pattern[last:]])

        results = [""]
        for segment_options in parts:
            results = [r + opt for r in results for opt in segment_options]
        return results

    def _collect_patterns(self) -> list[str]:
        patterns: list[str] = []
        enabled = self.options.enabled_groups
        for group in PATTERN_GROUPS:
            if group.id in enabled:
                patterns.extend(group.patterns)
        return patterns

    def generate(self) -> list[str]:
        passwords: list[str] = []
        seen: set[str] = set()

        for pattern in self._collect_patterns():
            for pwd in self._expand_pattern(pattern):
                candidates = [pwd]
                if self.options.include_reversed and len(pwd) >= 4:
                    candidates.append(pwd[::-1])

                for candidate in candidates:
                    if not candidate:
                        continue
                    if len(candidate) < self.options.min_length:
                        continue
                    if len(candidate) > self.options.max_length:
                        continue
                    if self.options.deduplicate:
                        if candidate in seen:
                            continue
                        seen.add(candidate)
                    passwords.append(candidate)

        return passwords

    def estimate_count(self) -> int:
        return len(self.generate())

    def get_bruteforce_info(self) -> str | None:
        """返回日期爆破说明，供界面展示。"""
        y, m, d = self._resolve_birth_parts()
        if not self.options.brute_force_date or y is None:
            return None
        if m is not None and d is not None:
            return None

        dates = self._iter_candidate_dates()
        if not dates:
            return None

        if m is not None:
            return f"已启用日期爆破：{y}年{m:02d}月共 {len(dates)} 天"
        return f"已启用日期爆破：{y}年共 {len(dates)} 天"

    def get_missing_fields_hint(self) -> list[str]:
        hints: list[str] = []
        enabled = self.options.enabled_groups

        needs_name = {"name_birth", "birth_name", "separators", "suffix_variants", "phone", "idcard_email"}
        needs_birth = {"name_birth", "birth_name", "birth_only", "separators", "suffix_variants", "idcard_email"}
        needs_phone = {"phone"}

        if enabled & needs_name and not self.info.name.strip():
            hints.append("姓名（用于拼音组合）")
        if enabled & needs_birth and not self.info.birth.strip() and not self.info.idcard.strip():
            hints.append("生日信息或身份证号")
        if enabled & needs_phone and not self.info.phone.strip():
            hints.append("手机号")

        y, m, d = self._resolve_birth_parts()
        if (
            self.options.brute_force_date
            and enabled & needs_birth
            and y is not None
            and m is None
            and d is None
        ):
            hints.append(f"将爆破 {y} 年全年日期（约 {366 if calendar.isleap(y) else 365} 天）")

        return hints
