from bot_controller import MinecraftBot
import time


def main():
    """Простая стратегия для Мирона"""
    print("🤖 Запуск стратегии Мирона")

    # Создаем бота
    bot = MinecraftBot()

    # Подключаемся к серверу
    bot.connect(
        host="188.120.254.248",
        port=25565,
        username="MironBot"
    )

    # Ждем подключения
    time.sleep(3)

    # Приветствие
    bot.chat("Привет! Я бот Мирона!")
    time.sleep(1)

    # Получаем позицию
    pos = bot.get_position()
    print(f"📍 Моя позиция: x={pos['x']:.1f}, y={pos['y']:.1f}, z={pos['z']:.1f}")

    # Идем вперед
    print("🚶 Иду вперед...")
    bot.move("forward", 5)
    time.sleep(2)

    # Прыгаем
    print("🦘 Прыгаю!")
    bot.jump()
    time.sleep(1)

    # Идем вправо
    print("🚶 Иду вправо...")
    bot.move("right", 3)
    time.sleep(2)

    # Проверяем позицию
    pos = bot.get_position()
    print(f"📍 Новая позиция: x={pos['x']:.1f}, y={pos['y']:.1f}, z={pos['z']:.1f}")
    bot.chat(f"Я на x={pos['x']:.0f}, z={pos['z']:.0f}")

    # Возвращаемся
    print("🚶 Возвращаюсь...")
    bot.move("back", 5)
    bot.move("left", 3)
    time.sleep(2)

    # Прощаемся
    bot.chat("Пока! Стратегия выполнена!")
    time.sleep(1)

    # Отключаемся
    bot.disconnect()
    print("✅ Стратегия завершена")


if __name__ == "__main__":
    main()