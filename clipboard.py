#! /usr/env/bin python3
#! -*- coding:utf-8 -*-

import win32con
import win32clipboard as w3cb


class Clipboard:
	@staticmethod
	def set_text(info):
		w3cb.OpenClipboard()
		w3cb.EmptyClipboard()
		w3cb.SetClipboardData(win32con.CF_UNICODETEXT, info)
		w3cb.CloseClipboard()

	@staticmethod
	def get_text():
		w3cb.OpenClipboard()
		text = w3cb.GetClipboardData(win32con.CF_UNICODETEXT)
		w3cb.CloseClipboard()
		return text

