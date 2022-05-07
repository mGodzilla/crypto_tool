#! /usr/env/bin python3
#! -*- coding:utf-8 -*-

import sys, time
from crypto import CryptoLevel, CryptoPhrase, Logger
from clipboard import Clipboard


def main():

	try:
		# 钱包助记词组字符串
		print("1. Please input your wallet recovery phrase")
		wallet_recovery_phrase = input("1. 请输入钱包助记词组字符串: ")
		# 加密密钥
		print("2. Please input your crypto key")
		crypto_key = input("2. 请输入加密密钥: ")
	except Exception as e:
		wallet_recovery_phrase = ""
		crypto_key = ""

	Logger.info("加密等级: 【0】默认 【1】简单 【2】困难 ")
	Logger.info("Crypto Level: [0]DEFAULT [1]EASY [2]HARD ")
	try:
		# 加密等级
		print("3. Please input the crypto level")
		crypto_level = int(input("3. 请选择加密等级: "))
	except Exception as e:
		crypto_level = 0
	crypto_level = CryptoLevel.value_of(crypto_level)

	try:
		# 加密次数
		print("4. Please input the crypto times")
		crypto_times = int(input("4. 请输入加密次数: "))
	except Exception as e:
		crypto_times = 100

	print("")
	if wallet_recovery_phrase == "" or crypto_key == "":
		Logger.warn("Please input valid wallet recovery phrase and crypto key.")
		Logger.warn("请输入正确的钱包助记词组和加密密钥。")
		exit(0)

	cp = CryptoPhrase(crypto_key, crypto_level, crypto_times)
	Logger.info("After forward encrypt, please input [1] to copy to the clipboard")
	Logger.info("正向加密后，输入【1】复制到剪贴板")
	forward_text = cp.forward_encrypt(wallet_recovery_phrase)
	Logger.info(forward_text)
	
	Logger.info("After reverse encrypt, please input [2] to copy to the clipboard")
	Logger.info("反向加密后，输入【2】复制到剪贴板")
	reverse_text = cp.reverse_encrypt(wallet_recovery_phrase)
	Logger.info(reverse_text)

	try:
		print("")
		ret_number = int(input("5. Please choose: "))
	except Exception as e:
		ret_number = 1
	Clipboard.set_text(forward_text if ret_number == 1 else reverse_text)
	Logger.info("Copied to clipboard successfully")
	Logger.info("已成功复制到剪贴板")


if __name__ == "__main__":
	main()

