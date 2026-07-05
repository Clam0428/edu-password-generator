"""教育 SRC 密码字典生成器 GUI。"""

from __future__ import annotations

import threading
from tkinter import filedialog, messagebox

import customtkinter as ctk

from .generator import GenerateOptions, PasswordGenerator, UserInfo
from .patterns import PATTERN_GROUPS, get_default_enabled_ids


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class EduPasswordGeneratorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("教育 SRC 密码字典生成器")
        self.geometry("1100x720")
        self.minsize(960, 640)

        self._group_vars: dict[str, ctk.BooleanVar] = {}
        self._passwords: list[str] = []
        self._generating = False

        self._build_layout()

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=0, minsize=380)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_input_panel()
        self._build_right_panel()

    def _build_input_panel(self) -> None:
        panel = ctk.CTkScrollableFrame(self, label_text="已知信息", width=360)
        panel.grid(row=0, column=0, padx=(12, 6), pady=12, sticky="nsew")
        panel.grid_columnconfigure(1, weight=1)

        fields = [
            ("name", "姓名", "如：张三"),
            ("student_id", "学号", "如：2021012345"),
            ("phone", "手机号", "如：13812345678"),
            ("birth", "生日信息", "完整生日(YYYY-MM-DD)或仅年份"),
            ("idcard", "身份证号", "完整18位身份证号"),
            ("email", "邮箱", "如：zhangsan@edu.cn"),
        ]

        self._entries: dict[str, ctk.CTkEntry] = {}
        for row, (key, label, placeholder) in enumerate(fields):
            ctk.CTkLabel(panel, text=label, anchor="w").grid(
                row=row, column=0, padx=(8, 6), pady=6, sticky="w"
            )
            entry = ctk.CTkEntry(panel, placeholder_text=placeholder)
            entry.grid(row=row, column=1, padx=(0, 8), pady=6, sticky="ew")
            self._entries[key] = entry

        hint = ctk.CTkLabel(
            panel,
            text="提示：字段均为可选，按实际掌握的信息填写。\n"
            "仅知年份时可勾选「爆破日期」遍历全年。",
            text_color="gray60",
            justify="left",
            wraplength=320,
        )
        hint.grid(row=len(fields), column=0, columnspan=2, padx=8, pady=(12, 4), sticky="w")

        self._brute_force_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            panel,
            text="爆破日期（仅知年份/月份时遍历所有可能日期）",
            variable=self._brute_force_var,
        ).grid(row=len(fields) + 1, column=0, columnspan=2, padx=8, pady=(4, 8), sticky="w")

    def _build_right_panel(self) -> None:
        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, padx=(6, 12), pady=12, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self._build_pattern_section(right)
        self._build_options_section(right)
        self._build_output_section(right)

    def _build_pattern_section(self, parent: ctk.CTkFrame) -> None:
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        ctk.CTkLabel(
            header,
            text="组合模式（可多选，仅生成已勾选类型）",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(side="left")
        ctk.CTkButton(header, text="全选", width=60, command=self._select_all_patterns).pack(side="right", padx=4)
        ctk.CTkButton(header, text="默认", width=60, command=self._reset_default_patterns).pack(side="right", padx=4)

        scroll = ctk.CTkScrollableFrame(frame, height=220, label_text="")
        scroll.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        scroll.grid_columnconfigure(0, weight=1)

        for group in PATTERN_GROUPS:
            var = ctk.BooleanVar(value=group.default_enabled)
            self._group_vars[group.id] = var
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.grid(sticky="ew", pady=2)
            row.grid_columnconfigure(1, weight=1)
            ctk.CTkCheckBox(row, text=group.label, variable=var, width=160).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(row, text=group.description, text_color="gray60", anchor="w").grid(
                row=0, column=1, padx=(8, 0), sticky="ew"
            )

    def _build_options_section(self, parent: ctk.CTkFrame) -> None:
        frame = ctk.CTkFrame(parent)
        frame.grid(row=1, column=0, sticky="new", pady=(0, 8))
        frame.grid_columnconfigure((1, 3, 5), weight=1)

        ctk.CTkLabel(frame, text="选项", font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, columnspan=6, padx=8, pady=(8, 4), sticky="w"
        )

        ctk.CTkLabel(frame, text="最小长度").grid(row=1, column=0, padx=(8, 4), pady=6)
        self._min_len = ctk.CTkEntry(frame, width=60)
        self._min_len.insert(0, "4")
        self._min_len.grid(row=1, column=1, padx=4, pady=6, sticky="w")

        ctk.CTkLabel(frame, text="最大长度").grid(row=1, column=2, padx=(12, 4), pady=6)
        self._max_len = ctk.CTkEntry(frame, width=60)
        self._max_len.insert(0, "32")
        self._max_len.grid(row=1, column=3, padx=4, pady=6, sticky="w")

        self._reverse_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(frame, text="包含反转组合", variable=self._reverse_var).grid(
            row=1, column=4, columnspan=2, padx=8, pady=6, sticky="w"
        )

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.grid(row=2, column=0, columnspan=6, padx=8, pady=(4, 8), sticky="ew")

        self._gen_btn = ctk.CTkButton(
            btn_row, text="生成字典", width=120, height=36, command=self._on_generate
        )
        self._gen_btn.pack(side="left", padx=(0, 8))

        self._export_btn = ctk.CTkButton(
            btn_row, text="导出 TXT", width=120, height=36, command=self._on_export, state="disabled"
        )
        self._export_btn.pack(side="left", padx=(0, 8))

        self._copy_btn = ctk.CTkButton(
            btn_row, text="复制全部", width=120, height=36, command=self._on_copy, state="disabled"
        )
        self._copy_btn.pack(side="left")

        self._status_label = ctk.CTkLabel(btn_row, text="就绪", text_color="gray60")
        self._status_label.pack(side="right", padx=8)

    def _build_output_section(self, parent: ctk.CTkFrame) -> None:
        frame = ctk.CTkFrame(parent)
        frame.grid(row=2, column=0, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="预览", font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, padx=8, pady=(8, 4), sticky="w"
        )

        self._preview = ctk.CTkTextbox(frame, font=ctk.CTkFont(family="Consolas", size=13))
        self._preview.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")
        self._preview.insert("1.0", "填写已知信息后点击「生成字典」…")
        self._preview.configure(state="disabled")

    def _select_all_patterns(self) -> None:
        for var in self._group_vars.values():
            var.set(True)

    def _reset_default_patterns(self) -> None:
        defaults = get_default_enabled_ids()
        for gid, var in self._group_vars.items():
            var.set(gid in defaults)

    def _collect_user_info(self) -> UserInfo:
        return UserInfo(**{k: e.get().strip() for k, e in self._entries.items()})

    def _collect_options(self) -> GenerateOptions:
        try:
            min_len = max(1, int(self._min_len.get()))
            max_len = max(min_len, int(self._max_len.get()))
        except ValueError:
            min_len, max_len = 4, 32

        enabled = {gid for gid, var in self._group_vars.items() if var.get()}
        return GenerateOptions(
            min_length=min_len,
            max_length=max_len,
            enabled_groups=enabled,
            include_reversed=self._reverse_var.get(),
            brute_force_date=self._brute_force_var.get(),
        )

    def _on_generate(self) -> None:
        if self._generating:
            return

        options = self._collect_options()
        if not options.enabled_groups:
            messagebox.showwarning("提示", "请至少勾选一种组合模式。")
            return

        info = self._collect_user_info()
        needs_info = options.enabled_groups

        if needs_info and not any([
            info.name, info.student_id, info.phone, info.birth,
            info.idcard, info.email,
        ]):
            messagebox.showwarning("提示", "请至少填写一项已知信息。")
            return

        birth_groups = {
            "name_birth", "birth_name", "birth_only",
            "separators", "suffix_variants", "idcard_email",
        }
        if options.brute_force_date and options.enabled_groups & birth_groups:
            gen_preview = PasswordGenerator(info, options)
            bf_info = gen_preview.get_bruteforce_info()
            if bf_info:
                count = gen_preview.estimate_count()
                if count > 50000 and not messagebox.askyesno(
                    "确认",
                    f"{bf_info}\n预计生成约 {count} 条密码，数量较大。\n是否继续？",
                ):
                        return

        self._generating = True
        self._gen_btn.configure(state="disabled", text="生成中…")
        self._status_label.configure(text="正在生成…")

        def task() -> None:
            gen = PasswordGenerator(info, options)
            hints = gen.get_missing_fields_hint()
            bf_info = gen.get_bruteforce_info()
            passwords = gen.generate()
            self.after(0, lambda: self._on_generate_done(passwords, hints, bf_info))

        threading.Thread(target=task, daemon=True).start()

    def _on_generate_done(self, passwords: list[str], hints: list[str], bf_info: str | None) -> None:
        self._passwords = passwords
        self._generating = False
        self._gen_btn.configure(state="normal", text="生成字典")

        self._preview.configure(state="normal")
        self._preview.delete("1.0", "end")

        selected_labels = [
            g.label for g in PATTERN_GROUPS if g.id in self._group_vars and self._group_vars[g.id].get()
        ]
        self._preview.insert("end", f"[模式] {', '.join(selected_labels)}\n")

        if bf_info:
            self._preview.insert("end", f"[爆破] {bf_info}\n")

        if hints:
            self._preview.insert("end", f"[提示] {', '.join(hints)}\n")

        if hints or bf_info:
            self._preview.insert("end", "\n")

        if not passwords:
            self._preview.insert("end", "未生成任何密码，请检查已填信息与已选模式是否匹配。")
            self._status_label.configure(text="生成 0 条")
            self._export_btn.configure(state="disabled")
            self._copy_btn.configure(state="disabled")
        else:
            self._preview.insert("end", "\n".join(passwords) + "\n")
            self._status_label.configure(text=f"共 {len(passwords)} 条")
            self._export_btn.configure(state="normal")
            self._copy_btn.configure(state="normal")

        self._preview.configure(state="disabled")

    def _on_export(self) -> None:
        if not self._passwords:
            return

        info = self._collect_user_info()
        default_name = "password_dict.txt"
        if info.student_id:
            default_name = f"dict_{info.student_id}.txt"
        elif info.name:
            default_name = f"dict_{info.name}.txt"

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfile=default_name,
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self._passwords))
            messagebox.showinfo("导出成功", f"已保存 {len(self._passwords)} 条密码至：\n{path}")
        except OSError as exc:
            messagebox.showerror("导出失败", str(exc))

    def _on_copy(self) -> None:
        if not self._passwords:
            return
        self.clipboard_clear()
        self.clipboard_append("\n".join(self._passwords))
        self._status_label.configure(text=f"已复制 {len(self._passwords)} 条")


def run_app() -> None:
    app = EduPasswordGeneratorApp()
    app.mainloop()
