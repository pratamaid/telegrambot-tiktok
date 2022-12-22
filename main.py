import re
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    name = State()

class download(StatesGroup):
    name = State()

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}

def download_video(url):
    request_url = f'https://api.douyin.wtf/api?url={url}'
    response = requests.get(request_url, headers=headers)
    video_link = response.json()['video_data']['nwm_video_url_HQ']
    return video_link


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(f'Selamat datang, {message.chat.first_name}!\n\nAnda dapat memulai dengan klik /download atau /list \n'
                        f'Maka video anda akan saya Download!\n\nSaat ini, saya mendukung '
                        f'hanya video dari TikTok!')
    btn1 = InlineKeyboardButton('/download', '/download')
    btn2 = InlineKeyboardButton('/list', '/list')
    markup4 = ReplyKeyboardMarkup(resize_keyboard=True).row(
        btn1, btn2
    )
    await message.answer('Pilih',reply_markup=markup4)

@dp.message_handler(commands=['list', 'List'])
async def send_list(message: types.Message, state: FSMContext):
    await Form.name.set()
    await message.reply(f'📚 Kirim List Video Tiktok :\n'
                        f'Pisahkan setiap link video dengan ↩')

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f"Hello, {message.chat.first_name}!\nMohon tunggu sebentar 😊")
    video_list = message.text.split('\n')
    counter = 0
    while counter < len(video_list):
        video_link = download_video(video_list[counter])
        await message.reply_video(video_link, caption='Saya senang bisa membantu! Salam, @unduhtiktokbot')
        counter = counter + 1
    else:
        print('Done')

@dp.message_handler(commands=['download', 'Download'])
async def send_video(message: types.Message):
    await download.name.set()
    await message.reply(f'🔗 Kirim Link Video Tiktok :')

@dp.message_handler(state=download.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        video_link = download_video(message.text)
        await message.reply_video(video_link, caption='Saya senang bisa membantu! Salam, @unduhtiktokbot')
    else:
        await message.answer('⛔️ Anda mengirim tautan yang tidak didukung oleh bot!\nKetik /help untuk bantuan')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)