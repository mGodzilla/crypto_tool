#! /usr/env/bin python3
#! -*- coding:utf-8 -*-

from functools import reduce
from enum import Enum


class Logger:
	__debug = False

	def __init__(self, is_debug):
		self.__debug = is_debug

	@classmethod
	def debug(cls, obj):
		if cls.__debug:
			print(str.format("[DEBUG] %s" % obj))

	@staticmethod
	def warn(obj):
		print(str.format("[WARN] %s" % obj))

	@staticmethod
	def info(obj):
		print(str.format("[INFO] %s" % obj))


class CryptoLevel(Enum):
	EASY = 1
	HARD = 2

	@classmethod
	def value_of(cls, value):
		for k, v in cls.__members__.items():
			if v.value == value:
				return v


class CryptoPhrase:
	__char_start = ord('a')
	__char_end = ord('z')

	def __init__(self, ckey, clevel=CryptoLevel.EASY, ctimes=1):
		self.crypto_key = str(ckey) # 加密密钥
		self.crypto_level = clevel if clevel in [v for v in CryptoLevel] else CryptoLevel.EASY # 加密等级
		self.crypto_times = int(ctimes) if str(ctimes).isdigit() else 1 # 加密次数
		self.__offset = self.__get_offset_list_by_crypto_key() # 加密偏移集合
		self.__offset_len = len(self.__offset) # 加密偏移集合长度

	def __get_offset_list_by_crypto_key(self):
		offsets = list()
		### 计算密钥每个字符的ASCII值并输出日志
		crypto_keys = [ord(v) for v in self.crypto_key]
		Logger.debug(crypto_keys)
		if self.crypto_level == CryptoLevel.HARD:
			### 困难模式，密钥每个字符ASCII数值分别和26取余
			offsets = [int(v % 26) for v in crypto_keys]
		elif self.crypto_level == CryptoLevel.EASY:
			### 简单模式，密钥每个字符ASCII数值之和和26取余
			offsets.append(reduce(lambda a, b : int(a) + int(b), crypto_keys) % 26)
		else:
			### FXIME 目前暂时和简单模式一致
			offsets.append(reduce(lambda a, b : int(a) + int(b), crypto_keys) % 26)
		### 输出加密信息日志
		Logger.info("The crypto level is {0}, and the crypto times is {1}. ".format(self.crypto_level.name, self.crypto_times))
		Logger.info("当前加密级别为{0}，加密次数为{1}。".format(self.crypto_level.name, self.crypto_times))
		### 输出偏移数组日志
		Logger.debug(offsets)
		return offsets

	def __get_offset_value(self, idx):
		return self.__offset[idx % self.__offset_len]

	def forward_encrypt(self, phrase):
		crypto_times = self.crypto_times
		while crypto_times > 0:
			Logger.debug("Crypto index: {0}".format(crypto_times))
			crypto_times -= 1
			phrase_cache = ""
			for idx, i in enumerate(str(phrase)):
				char_idx = ord(i)
				if char_idx != 32:
					char_idx += self.__get_offset_value(idx)
					char_idx = char_idx if char_idx <= self.__char_end else self.__char_start + (char_idx - self.__char_end - 1)
				phrase_cache += chr(char_idx)
			phrase = phrase_cache
		return phrase

	def reverse_encrypt(self, phrase):
		crypto_times = self.crypto_times
		while crypto_times > 0:
			Logger.debug("Crypto index: {0}".format(crypto_times))
			crypto_times -= 1
			phrase_cache = ""
			for idx, i in enumerate(str(phrase)):
				char_idx = ord(i)
				if char_idx != 32:
					char_idx -= self.__get_offset_value(idx)
					char_idx = char_idx if char_idx >= self.__char_start else self.__char_end - (self.__char_start - char_idx - 1)
				phrase_cache += chr(char_idx)
			phrase = phrase_cache
		return phrase

