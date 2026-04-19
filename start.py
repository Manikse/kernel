import subprocess
import os
import sys

def main():
    print("🚀 Ініціалізація EXARCHON Cloud Terminal...")

    # Шлях до Python у твоєму віртуальному середовищі (щоб працював rich та requests)
    python_exe = os.path.join("core", ".venv", "Scripts", "python.exe")
    
    if not os.path.exists(python_exe):
        print(f"❌ Помилка: Не знайдено віртуальне середовище за шляхом: {python_exe}")
        sys.exit(1)

    print("🌐 Підключення до Хмарного Нексуса (Railway)...")

    # Запускаємо ТІЛЬКИ клієнт
    try:
        subprocess.run(
            [python_exe, "client.py"],
            cwd=os.path.join("clients", "python-node")
        )
    except KeyboardInterrupt:
        pass 
    finally:
        print("\n🛑 Відключення терміналу. Хмарний Нексус продовжує роботу.")

if __name__ == "__main__":
    main()