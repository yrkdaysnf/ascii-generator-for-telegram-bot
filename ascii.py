from sys import argv
from html import escape
from time import time

from asyncio import run, sleep
from aiogram import Bot
from aiogram.types import Message
from aiogram.enums import ParseMode
import cv2

# A workaround to stop the execution of the cycle
async def stop(message: Message):
    global is_running
    is_running = False

async def ascii(message: Message, bot: Bot):
    global is_running
    is_running = True

    www = 50 # Max lenght fit

    inv = False
    if message is not None:
        if 'inv' in message.text:inv = True
    if len(argv)>1:
        if argv[1] == '-inv':inv = True

    video = 'BadApple(10fps).mp4' # Put name ur video here
    path = f'video//{video}'

    string = " `.,-':<>;+!*/?%&98#"
    coef = 255 / (len(string) - 1)
    
    cap = cv2.VideoCapture(path)

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    delay = float(1 / cap.get(cv2.CAP_PROP_FPS))
   
    for i in range(0,length):
        start_time = time()
        _, frame = cap.read()
        if frame is None:break

        frame = cv2.resize(frame, (www, int(frame.shape[0] / (frame.shape[1] / www) / 2)))
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if inv:gray_image = 255 - gray_image

        s = f'{video[:25]} [frame: {i+1}/{length}]\n.{"_"*(www-1)}.\n'
        for y in range(0, gray_image.shape[0] - 1):
            s += '|'
            for x in range(0, gray_image.shape[1] - 1):
                s += string[len(string) - int(gray_image[y, x] / coef) - 1]
            s += '|\n'
        s += f'˙{"‾"*(www-1)}˙\n'

        if __name__ != '__main__':
            if i == 0:
                msg = await bot.send_message(message.chat.id, 
                                             text=f'<code>\n{escape(s)}\n</code>', 
                                             parse_mode=ParseMode.HTML)
            else:
                await msg.edit_text(f'<code>\n{escape(s)}\n</code>', 
                                    parse_mode=ParseMode.HTML)
            # I recommend not to put less than three seconds, telegram are perceived as a flood.
            await sleep(3)
        else:
            print(s,end='\r')
            # I tried to compensate for the time spent processing the frame, but it didn't help. 
            await sleep(delay - ((time() - start_time)))

        if is_running == False: 
            is_running = False
            break

if __name__ == '__main__':
    run(ascii(None, None))