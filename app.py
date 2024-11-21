from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio

app = Flask(__name__)

# Ganti dengan api_id dan api_hash Anda
API_ID = '25713591'
API_HASH = '0922a8867d12505f4609bca66aa1b9b1'

# Simpan sesi pengguna
sessions = {}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    # Buat client Telegram
    client = TelegramClient(phone_number, API_ID, API_HASH)

    async def main():
        await client.start()
        # Kirim kode verifikasi
        await client.send_code_request(phone_number)
        sessions[phone_number] = client

    asyncio.run(main())
    return jsonify({'message': 'Verification code sent'}), 200

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json
    phone_number = data.get('phone_number')
    verification_code = data.get('verification_code')

    if not phone_number or not verification_code:
        return jsonify({'error': 'Phone number and verification code are required'}), 400

    client = sessions.get(phone_number)

    if not client:
        return jsonify({'error': 'Session not found. Please request a new code.'}), 400

    async def main():
        await client.start()
        try:
            # Verifikasi kode
            await client.sign_in(phone_number, verification_code)
            return jsonify({'message': 'Login successful'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return asyncio.run(main())

if __name__ == '__main__':
    app.run(port=5000)
