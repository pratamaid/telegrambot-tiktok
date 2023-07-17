import re
import requests
import array as arr
import colorama
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from colorama import Fore, Back, Style

API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
colorama.init(autoreset=True)

class Form(StatesGroup):
    name = State()

class download(StatesGroup):
    name = State()

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}

def fetch_video_id(url):
    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find('link', {'rel': 'canonical'}).attrs['href']
    video_id = link.split('/')[-1:][0]
    return video_id

def get_video_link(video_id):
    request_url = f'https://api2.musical.ly/aweme/v1/feed/?aweme_id={video_id}'
    response = requests.get(request_url, headers=headers)
    video_link = response.json()['aweme_list'][0]['video']['play_addr']['url_list'][2]
    unique_id = response.json()['aweme_list'][0]['author']['unique_id']
    love = response.json()['aweme_list'][0]['statistics']['digg_count']
    video_detail = [video_link, unique_id, love, video_id]
    return video_detail

def download_video(url):
    video_id = fetch_video_id(url)
    video_link = get_video_link(video_id)
    return video_link


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(f'Selamat datang, {message.chat.first_name}!\n\nAnda dapat memulai dengan klik /download atau /list \n'
                        f'Maka video anda akan saya Download!\n\nSaat ini, saya mendukung '
                        f'hanya video dari TikTok!')
    btn1 = InlineKeyboardButton('⬇️ Download', '/download')
    btn2 = InlineKeyboardButton('📚 List', '/list')
    markup4 = ReplyKeyboardMarkup(resize_keyboard=True).row(
        btn1, btn2
    )
    await message.answer('Pilih',reply_markup=markup4)

@dp.message_handler(commands=['list', 'List', '📚 List'])
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
    while counter <= len(video_list):
        video_detail = download_video(video_list[counter])
        await message.reply_video(video_detail[0], caption=f'📹Username: <a href="https://www.tiktok.com/@{video_detail[1]}">@{video_detail[1]}</a>\n❤️Like: {video_detail[2]}\n🔗Link: <a href="{video_detail[0]}">Link</a>\nSaya senang bisa membantu! @unduhtiktokbot',parse_mode=ParseMode.HTML)
        print(Fore.GREEN + '[+] Finish Downloading '+ str(video_detail[3]))
        counter = counter + 1
    else:
        await message.answer('⛔️ Anda mengirim tautan yang tidak didukung oleh bot!\nKetik /help untuk bantuan')
        print(Fore.RED + '[-] Downloading Error '+ str(video_detail[3]))

@dp.message_handler(commands=['download', 'Download', '⬇️ Download'])
async def send_video(message: types.Message):
    await download.name.set()
    await message.reply(f'🔗 Kirim Link Video Tiktok :')

@dp.message_handler(state=download.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        video_detail = download_video(message.text)
        await message.reply_video(video_detail[0], caption=f'📹Username: <a href="https://www.tiktok.com/@{video_detail[1]}">@{video_detail[1]}</a>\n❤️Like: {video_detail[2]}\n🔗Link: <a href="{video_detail[0]}">Link</a>\nSaya senang bisa membantu! @unduhtiktokbot',parse_mode=ParseMode.HTML)
        print(Fore.GREEN + '[+] Finish Downloading '+ str(video_detail[3]))
    else:
        await message.answer('⛔️ Anda mengirim tautan yang tidak didukung oleh bot!\nKetik /help untuk bantuan')
        print(Fore.RED + '[-] Downloading Error '+ str(video_detail[3]))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)