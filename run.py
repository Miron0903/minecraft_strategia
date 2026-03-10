#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Мастер-скрипт для запуска Minecraft стратегии с bridge.js
Запускает bridge и стратегию в одном окне
"""

import subprocess
import time
import os
import sys
import signal
import atexit


class MinecraftStarter:
    def __init__(self):
        self.bridge_process = None
        self.strategy_process = None

    def start_bridge(self):
        """Запускает bridge.js"""
        print("=" * 50)
        print("🚀 ЗАПУСК MINECRAFT СТРАТЕГИИ")
        print("=" * 50)
        print("[1/3] Запуск bridge.js...")

        # Проверяем, не занят ли порт
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 3000))
        if result == 0:
            print("⚠️  Порт 3000 уже занят. bridge.js вероятно уже запущен.")
            sock.close()
            return True

        sock.close()

        try:
            # Запускаем bridge в фоновом режиме
            self.bridge_process = subprocess.Popen(
                ["node", "bridge.js"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Ждем запуска
            for i in range(10):
                time.sleep(1)
                print(f"⏳ Ожидание... {i + 1}/10")

                # Проверяем, что процесс жив
                if self.bridge_process.poll() is not None:
                    print("❌ bridge.js завершился с ошибкой:")
                    stdout, stderr = self.bridge_process.communicate()
                    if stderr:
                        print(stderr)
                    return False

                # Проверяем, что порт открыт
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', 3000))
                sock.close()

                if result == 0:
                    print("✅ bridge.js запущен и готов к работе")
                    return True

            print("❌ Таймаут: bridge.js не отвечает")
            return False

        except Exception as e:
            print(f"❌ Ошибка запуска bridge.js: {e}")
            return False

    def run_strategy(self, strategy_file="miron_strategia.py"):
        """Запускает стратегию"""
        print(f"[2/3] Запуск стратегии {strategy_file}...")

        try:
            self.strategy_process = subprocess.run(
                [sys.executable, strategy_file],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка выполнения стратегии: {e}")
            return False
        except KeyboardInterrupt:
            print("\n⚠️  Стратегия прервана пользователем")
            return False

    def cleanup(self):
        """Очистка ресурсов"""
        print("[3/3] Очистка ресурсов...")

        if self.bridge_process:
            print("🛑 Останавливаю bridge.js...")
            if sys.platform == "win32":
                self.bridge_process.terminate()
            else:
                self.bridge_process.send_signal(signal.SIGTERM)

            try:
                self.bridge_process.wait(timeout=5)
                print("✅ bridge.js остановлен")
            except subprocess.TimeoutExpired:
                print("⚠️  Принудительное завершение bridge.js")
                self.bridge_process.kill()

    def run(self, strategy_file="miron_strategia.py"):
        """Основной метод запуска"""
        try:
            if self.start_bridge():
                self.run_strategy(strategy_file)
        finally:
            self.cleanup()
            print("=" * 50)
            print("✅ Работа завершена")
            print("=" * 50)


if __name__ == "__main__":
    # Можно выбрать стратегию через аргумент командной строки
    import argparse

    parser = argparse.ArgumentParser(description='Запуск Minecraft стратегии с bridge.js')
    parser.add_argument('--strategy', default='miron_strategia.py',
                        help='Имя файла стратегии (по умолчанию: miron_strategia.py)')
    args = parser.parse_args()

    starter = MinecraftStarter()

    # Регистрируем очистку при любом завершении
    atexit.register(starter.cleanup)

    try:
        starter.run(args.strategy)
    except KeyboardInterrupt:
        print("\n⚠️  Получен сигнал прерывания")
        starter.cleanup()