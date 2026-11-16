"""Inline keyboards. Every button has a handler — no dead controls."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bots.common.i18n import LANGUAGES, t

REPORTS = {"dashboard": "📊", "consumption": "📈", "anomalies": "⚠️", "forecast": "🔮"}


def main_menu(language: str, *, is_demo: bool, is_admin: bool = False) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=t(language, "dashboard"), callback_data="menu:dashboard"),
         InlineKeyboardButton(text=t(language, "analysis"), callback_data="menu:analysis")],
        [InlineKeyboardButton(text=t(language, "anomalies"), callback_data="menu:anomalies"),
         InlineKeyboardButton(text=t(language, "forecast"), callback_data="menu:forecast")],
        [InlineKeyboardButton(text=t(language, "report"), callback_data="menu:report"),
         InlineKeyboardButton(text=t(language, "settings"), callback_data="menu:settings")],
    ]
    if not is_demo:
        rows.append([InlineKeyboardButton(text=t(language, "upload"), callback_data="menu:upload")])
    if is_admin:
        rows.append([InlineKeyboardButton(text="👑 Admin Panel", callback_data="menu:admin")])
    rows.append([InlineKeyboardButton(text=t(language, "help"), callback_data="menu:help")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Yangilash", callback_data="admin:refresh")],
        [InlineKeyboardButton(text=t(language, "back"), callback_data="menu:main")]
    ])


def back_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(language, "back"), callback_data="menu:main")]])


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=f"lang:{code}")]
        for code, label in LANGUAGES.items()])


def report_keyboard(language: str) -> InlineKeyboardMarkup:
    formats = [("pdf", "PDF"), ("xlsx", "Excel"), ("csv", "CSV")]
    rows = []
    for kind, icon in REPORTS.items():
        rows.append([InlineKeyboardButton(text=f"{icon} {kind}",
                                          callback_data=f"report:{kind}:pdf")])
    rows.append([InlineKeyboardButton(text=t(language, "back"), callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def settings_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 " + t(language, "choose_lang"),
                              callback_data="settings:lang")],
        [InlineKeyboardButton(text=t(language, "alerts"), callback_data="settings:alerts")],
        [InlineKeyboardButton(text="🔓 Unlink", callback_data="settings:unlink")],
        [InlineKeyboardButton(text=t(language, "back"), callback_data="menu:main")],
    ])
