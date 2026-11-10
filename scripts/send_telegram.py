import os
import glob
import re
import sys
import requests

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '').strip()
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '').strip()

if not bot_token or not chat_id:
    print('[WARN] Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID.')
    sys.exit(0)

key_files = glob.glob('*KEYS.txt') + glob.glob('etkg_run/*KEYS.txt')
if not key_files:
    print('[WARN] No KEYS.txt file found.')
    sys.exit(0)

with open(key_files[0], 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

name_m = re.search(r'License Name:\s*(.*)', content)
key_m = re.search(r'License Key:\s*([A-Z0-9-]+)', content)
date_m = re.search(r'License Out Date:\s*(.*)', content)

lic_name = name_m.group(1).strip() if name_m else 'ESET HOME Security Premium'
lic_key = key_m.group(1).strip() if key_m else 'N/A'
lic_date = date_m.group(1).strip() if date_m else 'N/A'

msg = (
    '<b>🔑 ESET License Key định kỳ (Ngày 03 hàng tháng)</b>\n\n'
    f'🛡 <b>Gói bản quyền:</b> {lic_name}\n'
    f'🔑 <b>License Key:</b> <code>{lic_key}</code>\n'
    f'📅 <b>Hạn dùng:</b> {lic_date}\n\n'
    '<i>(Nhấp vào mã key để copy nhanh)</i>'
)

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
res = requests.post(url, json={'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'}, timeout=15)
print('[INFO] Telegram response:', res.text)
