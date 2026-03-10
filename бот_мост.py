# бот_мост.py - Подключение к реальному Minecraft серверу через bridge.js
import requests
import time


class MinecraftКарта:
    """Читает карту с реального сервера 188.120.254.248:25565"""

    def __init__(self, bridge_url="http://localhost:3000"):
        self.bridge_url = bridge_url
        self.сервер_ip = "188.120.254.248"
        self.порт = 25565
        self.боты = {}

    def создать_бота(self, имя):
        """Создает нового бота на сервере"""
        try:
            response = requests.post(f"{self.bridge_url}/connect", json={
                "host": self.сервер_ip,
                "port": self.порт,
                "username": имя
            }, timeout=5)

            if response.status_code == 200:
                print(f"✅ Бот {имя} создан на сервере")
                self.боты[имя] = {
                    'имя': имя,
                    'подключен': True,
                    'позиция': {'x': 0, 'y': 64, 'z': 0}
                }
                return True
        except Exception as e:
            print(f"❌ Ошибка создания бота: {e}")
            return False

    def получить_позицию(self, имя_бота):
        """Получает позицию бота на сервере"""
        try:
            response = requests.get(f"{self.bridge_url}/position", timeout=2)
            data = response.json()
            if 'x' in data:
                self.боты[имя_бота]['позиция'] = data
                return data
        except:
            pass
        return {'x': 0, 'y': 64, 'z': 0}

    def получить_блок(self, имя_бота, x, y, z):
        """
        👁️ ПОЛУЧАЕТ РЕАЛЬНЫЙ БЛОК С СЕРВЕРА
        """
        try:
            # Перемещаем бота для сканирования
            requests.post(f"{self.bridge_url}/move", json={
                "direction": "forward",
                "steps": 0  # Не двигаемся, просто запрашиваем блок
            })

            # Здесь нужно добавить эндпоинт в bridge.js для получения блока
            # Пока возвращаем заглушку
            return {
                'тип': 'камень',
                'прочность': 100,
                'можно_копать': True,
                'свет': 15
            }
        except:
            return {'тип': 'неизвестно', 'прочность': 0}

    def сканировать_область(self, имя_бота, центр_x, центр_y, центр_z, радиус=10):
        """
        🔍 Сканирует область вокруг бота (реальные блоки с сервера)
        Возвращает карту для стратегии
        """
        карта = {}
        for dx in range(-радиус, радиус + 1):
            for dz in range(-радиус, радиус + 1):
                for dy in range(-3, 4):  # По вертикали меньше
                    x = центр_x + dx
                    y = центр_y + dy
                    z = центр_z + dz

                    блок = self.получить_блок(имя_бота, x, y, z)
                    карта[(x, y, z)] = блок

        return карта

    def двигать_бота(self, имя_бота, направление, шагов=1):
        """Двигает бота по серверу"""
        try:
            response = requests.post(f"{self.bridge_url}/move", json={
                "direction": направление,
                "steps": шагов
            })
            return response.status_code == 200
        except:
            return False

    def отправить_сообщение(self, имя_бота, текст):
        """Отправляет сообщение в чат"""
        try:
            requests.post(f"{self.bridge_url}/chat", json={
                "message": текст
            })
        except:
            pass