import requests
import time
import json

# Настройки
BRIDGE_URL = "http://localhost:3000"

class MinecraftBot:
    def __init__(self):
        self.connected = False
    
    def connect(self, host, port=25565, username="ExplorerBot"):
        """Подключение к серверу"""
        data = {
            "host": host,
            "port": port,
            "username": username
        }
        response = requests.post(f"{BRIDGE_URL}/connect", json=data)
        self.connected = True
        print(f"✅ Подключаюсь к {host}:{port} как {username}...")
        return response.json()
    
    def move(self, direction, steps=1):
        """Движение"""
        data = {"direction": direction, "steps": steps}
        response = requests.post(f"{BRIDGE_URL}/move", json=data)
        return response.json()
    
    def jump(self):
        """Прыжок"""
        response = requests.post(f"{BRIDGE_URL}/jump", json={})
        return response.json()
    
    def chat(self, message):
        """Отправить сообщение"""
        data = {"message": message}
        response = requests.post(f"{BRIDGE_URL}/chat", json=data)
        return response.json()
    
    def get_position(self):
        """Получить координаты"""
        response = requests.get(f"{BRIDGE_URL}/position")
        return response.json()
    
    def disconnect(self):
        """Отключиться"""
        response = requests.post(f"{BRIDGE_URL}/disconnect", json={})
        self.connected = False
        return response.json()

# ===== БОТ-ИССЛЕДОВАТЕЛЬ =====
def explorer_bot():
    """Бот который исследует мир"""
    bot = MinecraftBot()
    
    # 1. ПОДКЛЮЧЕНИЕ К СЕРВЕРУ
    server_ip = input("Введите IP сервера (например 188.120.254.248): ")
    bot_name = input("Введите имя для бота (например Explorer): ")
    
    bot.connect(
        host=server_ip,
        port=25565,
        username=bot_name
    )
    
    print("⏳ Ждем подключения...")
    time.sleep(5)  # Ждем подключения
    
    # 2. ПРИВЕТСТВИЕ
    bot.chat("Привет! Я бот-исследователь!")
    time.sleep(2)
    
    # 3. ИССЛЕДОВАНИЕ
    print("🔍 Начинаем исследование...")
    
    # Идем вперед 20 шагов, осматриваясь
    for step in range(1, 6):  # 5 раз по 4 шага
        # Идем немного вперед
        bot.chat(f"Исследую... шаг {step*4}")
        bot.move("forward", 4)
        time.sleep(2)
        
        # Осматриваемся по сторонам
        bot.move("left", 1)
        time.sleep(1)
        bot.move("right", 2)
        time.sleep(1)
        bot.move("left", 1)
        time.sleep(1)
        
        # Проверяем где мы
        pos = bot.get_position()
        print(f"📍 Сейчас я на x={pos['x']}, y={pos['y']}, z={pos['z']}")
        bot.chat(f"Я на высоте {int(pos['y'])} блоков")
        
        # Иногда прыгаем, чтобы посмотреть вокруг
        if step % 2 == 0:
            bot.jump()
            time.sleep(1)
    
    # 4. ВОЗВРАЩЕНИЕ
    bot.chat("Возвращаюсь обратно!")
    bot.move("back", 20)
    time.sleep(4)
    
    # 5. ФИНАЛ
    bot.chat("Исследование завершено!")
    pos = bot.get_position()
    print(f"🏁 Финальная позиция: {pos}")
    
    time.sleep(2)
    bot.disconnect()
    print("✅ Бот отключился")

# ЗАПУСК
if __name__ == "__main__":
    print("="*50)
    print("🤖 БОТ-ИССЛЕДОВАТЕЛЬ MINECRAFT")
    print("="*50)
    print("ВАЖНО: Сначала должен быть запущен bridge.js!")
    print("="*50)
    
    explorer_bot()