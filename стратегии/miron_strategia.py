from bot_controller import MinecraftBot
import time
import random
import math
from collections import deque


class SmartStrategy:
    """
    🧠 УМНАЯ СТРАТЕГИЯ
    ==================
    - Автоматическое исследование местности
    - Поиск безопасных мест
    - Патрулирование территории
    - Реакция на игроков
    - Интеллектуальное перемещение
    """

    def __init__(self, bot):
        self.bot = bot
        self.memory = {
            'visited': [],  # Посещенные места
            'safe_spots': [],  # Безопасные места
            'players_seen': {},  # Замеченные игроки
            'start_time': time.time()  # Время запуска
        }
        self.state = "exploring"  # exploring, patrolling, returning, hiding
        self.last_action = time.time()
        self.action_cooldown = 2.0
        self.path_history = deque(maxlen=20)  # История перемещений

    def run(self):
        """Основной цикл умной стратегии"""

        # Приветствие
        self.bot.chat("🧠 Запущена УМНАЯ стратегия!")
        time.sleep(1)
        self.bot.chat("Я буду исследовать мир и искать безопасные места")

        # Получаем стартовую позицию
        start_pos = self.bot.get_position()
        self.memory['base'] = start_pos
        print(f"🏠 База установлена: x={start_pos['x']:.1f}, y={start_pos['y']:.1f}, z={start_pos['z']:.1f}")

        # Основной цикл (20 итераций)
        for cycle in range(20):
            print(f"\n🔄 Цикл {cycle + 1}/20 | Состояние: {self.state}")

            # Обновляем состояние
            self.update_state()

            # Действуем по состоянию
            if self.state == "exploring":
                self.explore()
            elif self.state == "patrolling":
                self.patrol()
            elif self.state == "returning":
                self.return_to_base()
            elif self.state == "hiding":
                self.hide()

            # Сохраняем позицию в память
            current_pos = self.bot.get_position()
            self.memory['visited'].append({
                'x': current_pos['x'],
                'z': current_pos['z'],
                'time': time.time()
            })

            # Короткая пауза между циклами
            time.sleep(1)

        # Завершение
        self.bot.chat("✅ Умная стратегия завершена!")
        self.bot.chat(
            f"Я исследовал {len(self.memory['visited'])} мест и нашел {len(self.memory['safe_spots'])} безопасных точек")
        time.sleep(2)

    def update_state(self):
        """Обновляет состояние на основе окружения"""
        current_pos = self.bot.get_position()
        time_running = time.time() - self.memory['start_time']

        # Меняем состояние в зависимости от условий

        # Если нашел опасность - прячемся
        if self.detect_danger(current_pos):
            self.state = "hiding"
            return

        # Если долго исследуем (больше 2 минут) - возвращаемся на базу
        if time_running > 120 and self.state == "exploring":
            self.state = "returning"
            self.bot.chat("⏰ Долго исследую, пора возвращаться")
            return

        # Если уже много где был - начинаем патрулировать
        if len(self.memory['visited']) > 15 and self.state == "exploring":
            self.state = "patrolling"
            self.bot.chat("👮 Теперь буду патрулировать территорию")
            return

        # Случайно меняем состояние для разнообразия (10% шанс)
        if random.random() < 0.1 and self.state != "hiding":
            states = ["exploring", "patrolling", "returning"]
            new_state = random.choice(states)
            if new_state != self.state:
                self.state = new_state
                self.bot.chat(f"🔄 Решил переключиться на {new_state}")

    def explore(self):
        """Режим исследования - ищем новые места"""
        if not self.can_act():
            return

        # Выбираем случайное направление
        directions = ['forward', 'back', 'left', 'right']
        direction = random.choice(directions)

        # Случайное количество шагов (3-8)
        steps = random.randint(3, 8)

        print(f"🔍 Исследую: {direction} на {steps} шагов")

        # Идем и осматриваемся
        for step in range(steps):
            self.bot.move(direction, 1)
            time.sleep(0.8)

            # Каждый шаг осматриваемся
            self.look_around()

            # Запоминаем интересные места
            if self.is_interesting_spot():
                self.mark_safe_spot()

        self.last_action = time.time()

    def patrol(self):
        """Режим патрулирования - ходим по кругу"""
        if not self.can_act():
            return

        # Патрульный маршрут: круг
        print("👮 Патрулирую периметр")

        # Идем по квадрату
        for direction in ['forward', 'right', 'back', 'left']:
            self.bot.chat(f"🚶 Патруль: {direction}")

            for step in range(5):
                self.bot.move(direction, 1)
                time.sleep(0.6)

                # Проверяем, все ли спокойно
                if random.random() < 0.3:
                    self.check_surroundings()

            time.sleep(0.5)

        self.last_action = time.time()

    def return_to_base(self):
        """Возвращение на базу"""
        if not self.can_act():
            return

        print("🏠 Возвращаюсь на базу")
        self.bot.chat("🏠 Возвращаюсь домой")

        # Получаем текущую позицию и базу
        current = self.bot.get_position()
        base = self.memory.get('base', {'x': 0, 'y': 0, 'z': 0})

        # Вычисляем направление к базе
        dx = base['x'] - current['x']
        dz = base['z'] - current['z']

        # Идем по оси X
        steps_x = abs(int(dx))
        direction_x = 'right' if dx > 0 else 'left'

        for _ in range(min(steps_x, 10)):  # Не больше 10 шагов за раз
            self.bot.move(direction_x, 1)
            time.sleep(0.5)

        # Идем по оси Z
        steps_z = abs(int(dz))
        direction_z = 'back' if dz > 0 else 'forward'

        for _ in range(min(steps_z, 10)):
            self.bot.move(direction_z, 1)
            time.sleep(0.5)

        # Проверяем, дошли ли
        new_pos = self.bot.get_position()
        distance = math.sqrt(
            (new_pos['x'] - base['x']) ** 2 +
            (new_pos['z'] - base['z']) ** 2
        )

        if distance < 5:
            self.bot.chat("✅ Я на базе!")
            self.state = "exploring"  # После возвращения снова исследуем
        else:
            print(f"📏 До базы еще {distance:.1f} блоков")

        self.last_action = time.time()

    def hide(self):
        """Прячемся от опасности"""
        print("⚠️ Прячусь!")
        self.bot.chat("⚠️ Опасность! Прячусь!")

        # Несколько раз прыгаем (имитация паники)
        for _ in range(3):
            self.bot.jump()
            time.sleep(0.5)

        # Убегаем в случайном направлении
        direction = random.choice(['left', 'right'])
        for _ in range(4):
            self.bot.move(direction, 1)
            time.sleep(0.4)

        # Ждем
        time.sleep(2)

        # Возвращаемся к исследованию
        self.state = "exploring"
        self.bot.chat("😅 Вроде безопасно, продолжаю")
        self.last_action = time.time()

    def look_around(self):
        """Осматривается по сторонам"""
        pos = self.bot.get_position()
        print(f"  👀 Осмотр: x={pos['x']:.1f}, z={pos['z']:.1f}")

        # Смотрим влево-вправо
        for side in ['left', 'right']:
            self.bot.move(side, 1)
            time.sleep(0.3)
            self.bot.move(side, 1)  # Возвращаемся
            time.sleep(0.3)

    def check_surroundings(self):
        """Проверка окружения"""
        pos = self.bot.get_position()

        # Проверяем высоту
        if pos['y'] > 100:
            print("  ⛰️ Высоко!")
        elif pos['y'] < 20:
            print("  🕳️ Низко!")

        # Ищем игроков (в реальном боте нужно слушать события)
        if random.random() < 0.2:
            print("  👤 Кажется, кто-то рядом...")

    def detect_danger(self, pos):
        """Определяет опасность"""
        # Опасно если:
        # - Очень низко (может быть яма/лава)
        # - Очень высоко (может упасть)
        # - Рядом игрок (симуляция)

        if pos['y'] < 5:
            return True

        if pos['y'] > 200:
            return True

        # Случайная опасность (10% шанс)
        if random.random() < 0.05:
            return True

        return False

    def is_interesting_spot(self):
        """Определяет, интересное ли место"""
        # 20% шанс, что место интересное
        return random.random() < 0.2

    def mark_safe_spot(self):
        """Отмечает безопасное место"""
        pos = self.bot.get_position()

        spot = {
            'x': pos['x'],
            'y': pos['y'],
            'z': pos['z'],
            'time': time.time()
        }

        self.memory['safe_spots'].append(spot)
        print(f"⭐ Найдено безопасное место: x={spot['x']:.1f}, z={spot['z']:.1f}")
        self.bot.chat(f"⭐ Нашел хорошее место! Координаты сохранены")

    def can_act(self):
        """Проверяет, можно ли действовать"""
        if time.time() - self.last_action < self.action_cooldown:
            return False
        return True


def main():
    """Запуск умной стратегии"""
    print("🧠 ЗАПУСК УМНОЙ СТРАТЕГИИ")
    print("=" * 50)

    # Создаем бота
    bot = MinecraftBot()

    # Подключаемся к серверу
    server_ip = input("Введите IP сервера (188.120.254.248): ") or "188.120.254.248"
    bot_name = input("Введите имя бота (SmartBot): ") or "SmartBot"

    print(f"\n🚀 Подключаюсь к {server_ip}...")
    bot.connect(
        host=server_ip,
        port=25565,
        username=bot_name
    )

    # Ждем подключения
    print("⏳ Ожидание подключения...")
    time.sleep(5)

    # Запускаем стратегию
    strategy = SmartStrategy(bot)
    strategy.run()

    # Отключаемся
    bot.disconnect()
    print("✅ Умная стратегия завершена")


if __name__ == "__main__":
    # Проверяем наличие необходимых модулей
    try:
        from bot_controller import MinecraftBot
    except ImportError:
        print("❌ Ошибка: не найден модуль bot_controller.py")
        print("Сначала создайте bot_controller.py с классом MinecraftBot")
        exit(1)

    main()