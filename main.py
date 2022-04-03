#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

from kahoot import Kahoot
from kahoot.models import Message

bot = Kahoot()

@bot.on("message")
async def message(data: Message) -> None:
    pass

async def main() -> None:
    async with bot:
        await bot.join(6598272, nickname="aidnzz")
        await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
