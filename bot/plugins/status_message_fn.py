#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import asyncio
import os
import shutil
import time

from bot import (
    BOT_START_TIME,
    LOGGER,
    LOG_FILE_ZZGEVC,
    MAX_MESSAGE_LENGTH
)


from bot.helper_funcs.admin_check import AdminCheck
from bot.commands import Command
from bot.localisation import Localisation
from bot.helper_funcs.display_progress import (
    TimeFormatter,
    humanbytes
)


async def status_message_f(client, message):
    currentTime = time.strftime("%H:%M:%S", time.gmtime(time.time() - BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)

    ms_g = f"<b>Bot Uptime</b>: <code>{currentTime}</code>\n" \
        f"<b>Total disk space</b>: <code>{total}</code>\n" \
        f"<b>Used</b>: <code>{used}</code>\n" \
        f"<b>Free</b>: <code>{free}</code>\n"

    msg = ms_g
    await message.reply_text(msg, quote=True)

async def exec_message_f(client, message):
    #if await AdminCheck(client, message.chat.id, message.from_user.id):
    if True:
        DELAY_BETWEEN_EDITS = 0.3
        PROCESS_RUN_TIME = 100
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.message_id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.message_id

        start_time = time.time() + PROCESS_RUN_TIME
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "No Error"
        o = stdout.decode()
        if not o:
            o = "No Output"
        else:
            _o = o.split("\n")
            o = "`\n".join(_o)
        OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

        if len(OUTPUT) > MAX_MESSAGE_LENGTH:
            with open("exec.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(OUTPUT))
            await client.send_document(
                chat_id=message.chat.id,
                document="exec.text",
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id
            )
            os.remove("exec.text")
            await message.delete()
        else:
            await message.reply_text(OUTPUT)


async def upload_log_file(client, message):
    await message.reply_document(
        LOG_FILE_ZZGEVC
    )
