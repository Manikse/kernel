import subprocess
import time
import os
import sys

def main():
    print("🚀 Ініціалізація EXARCHON Cognitive Engine...")

    # Шлях до Python у твоєму віртуальному середовищі
    python_exe = os.path.join("core", ".venv", "Scripts", "python.exe")
    
    if not os.path.exists(python_exe):
        print(f"❌ Помилка: Не знайдено віртуальне середовище за шляхом: {python_exe}")
        sys.exit(1)

    # 1. Запускаємо Ядро (Мозок) у фоновому режимі
    print("🧠 Підняття Нексуса у фоні (Decoupled Mode)...")
    core_process = subprocess.Popen(
        [python_exe, "main.py"],
        cwd="core", # Запускаємо з папки core
        stdout=subprocess.DEVNULL, # Ховаємо сухі серверні логи
        stderr=subprocess.DEVNULL
    )

    # Даємо серверу 4 секунди на запуск та підключення до API
    print("⏳ Встановлення нейронного зв'язку...")
    time.sleep(4) 

    # 2. Запускаємо Термінал (Руки) прямо в цьому вікні
    try:
        subprocess.run(
            [python_exe, "client.py"],
            cwd=os.path.join("clients", "python-node")
        )
    except KeyboardInterrupt:
        pass # Перехоплюємо Ctrl+C, щоб не було страшних помилок
    finally:
        # 3. Автоматичне прибирання
        print("\n🛑 Відключення терміналу. Згортання Нексуса...")
        core_process.terminate()
        core_process.wait()
        print("✅ Система EXARCHON успішно приспана.")

if __name__ == "__main__":
    main()