#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/3/30 下午5:26 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : edgeTTS.py
# @desc : README.md

import asyncio

import edge_tts

TEXT = "早上好，今天遇到你很高心"
VOICE = "zh-CN-XiaoxiaoNeural"
OUTPUT_FILE = "test.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.run(amain())