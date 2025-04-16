from flask import Flask, request, jsonify, render_template_string
import os
from threading import Thread
from datetime import datetime
import logging
import telebot


app = Flask(__name__)

TELEGRAM_TOKEN = '7455126495:AAFDHI1u5myCbspaRjydZutxno0xejfU0AU4'
TELEGRAM_CHAT_ID = 'ВАШ_CHAT_ID'
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['chat_id'])
def send_id(message):
    idisnik = message.chat.id
    bot.reply_to(message, f"id чата: {idisnik}")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def send_telegram_alert(message_text, photo_path=None):
    try:
        url = f'https://api.telegram.org/bot{7455126495:AAFDHI1u5myCbspaRjydZutxno0xejfU0AU}/'

        if photo_path:
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': TELEGRAM_CHAT_ID,
                    'caption': message_text,
                    'parse_mode': 'HTML'
                }
                response = requests.post(url + 'sendPhoto', files=files, data=data, timeout=10)
        else:
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message_text,
                'parse_mode': 'HTML'
            }
            response = requests.post(url + 'sendMessage', data=data, timeout=10)

        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки в Telegram: {str(e)}")
        return False


def notify_startup():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"<b>🚀 Сервер мониторинга запущен</b>\n\n" \
              f"🕒 <i>{current_time}</i>\n" \
              f"📡 Готов к приему аварийных сигналов"
    send_telegram_alert(message)


@app.route('/emergency', methods=['GET', 'POST'])
def handle_emergency():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return jsonify({'error': 'Фото не найдено в запросе'}), 400

        file = request.files['photo']
        if file.filename == '':
            return jsonify({'error': 'Не выбран файл'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Недопустимый формат файла'}), 400
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"emergency_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"<b>🚨 АВАРИЙНЫЙ СИГНАЛ!</b>\n\n" \
                  f"🕒 <i>{current_time}</i>\n" \
                  f"📷 Фото зафиксировано системой"
        if send_telegram_alert(message, filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logger.error(f"Ошибка удаления файла: {str(e)}")

            return jsonify({'status': 'success', 'message': 'Фото отправлено'})
        else:
            return jsonify({'error': 'Ошибка отправки уведомления'}), 500
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Отправка аварийного фото</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; }
                h1 { color: #d9534f; }
                .form-group { margin-bottom: 15px; }
                button { background-color: #d9534f; color: white; border: none; padding: 10px 15px; cursor: pointer; }
                button:hover { background-color: #c9302c; }
            </style>
        </head>
        <body>
            <h1>Отправка аварийного фото</h1>
            <form action="/emergency" method="post" enctype="multipart/form-data">
                <div class="form-group">
                    <input type="file" name="photo" accept="image/*" required>
                </div>
                <button type="submit">Отправить сигнал</button>
            </form>
        </body>
        </html>
    ''')


@app.route('/status')
def status_check():
    return jsonify({
        'status': 'active',
        'timestamp': datetime.now().isoformat(),
        'service': 'Smart Home Emergency Server'
    })


if __name__ == '__main__':
    Thread(target=notify_startup).start()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )