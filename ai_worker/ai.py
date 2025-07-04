import os
import openai
import subprocess
import time
import threading
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(prompt: str, model="gpt-4", temperature=0.7) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты — AI-помощник по тендерам. Отвечай кратко и по делу."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Ошибка GPT: {str(e)}"

def vpn_connect(config_path):
    while True:
        print(f"Запускаем VPN с конфигом: {config_path}")
        proc = subprocess.Popen(['openvpn', '--config', config_path])
        time.sleep(10)  # даём VPN подняться
        print("[✓] Проверка IP через VPN:")
        os.system("curl ifconfig.me")  # покажет IP прямо в консоли
        proc.wait()
        print("VPN-соединение прервано, переподключаемся через 15 секунд...")
        time.sleep(15)


if __name__ == "__main__":
    vpn_config = os.path.join(os.path.dirname(__file__), "vpn_configs", "vpngate_vpn185479259.opengw.net_udp_1888.ovpn")
    print("📁 Используем конфиг:", vpn_config)

    vpn_thread = threading.Thread(target=vpn_connect, args=(vpn_config,), daemon=True)
    vpn_thread.start()

    time.sleep(15)  # Дай VPN нормально подняться

    print("💬 Отправляем запрос к GPT...")
    response = ask_gpt("Привет! Ты работаешь?")
    print("🧠 Ответ GPT:", response)


