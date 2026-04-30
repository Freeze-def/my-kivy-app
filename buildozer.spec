[app]
# === Basic Info ===
title = My Kivy App
package.name = mykivyapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# === Requirements (FIXED: совместимые версии) ===
# Убрали фиксацию ==3.11, чтобы p4a сама подобрала совместимую версию
# Если критично именно 3.11 — используйте p4a.branch = 2023.10.24 или новее из stable
requirements = python3,kivy

# === Display ===
orientation = portrait
fullscreen = 0

# === Android Configuration ===
android.api = 33
android.minapi = 21
# NDK версия указывается без "r", buildozer сам найдёт или скачает
android.ndk = 25c
# android.sdk лучше не фиксировать, если не требуется конкретно — раскомментируйте при необходимости
# android.sdk = 33
android.accept_sdk_license = True

# === python-for-android (FIXED: стабильная ветка) ===
# develop — экспериментальная, часто ломается. Используем стабильный релиз.
p4a.branch = master
# p4a.source можно указать для полной воспроизводимости (опционально):
# p4a.source = https://github.com/kivy/python-for-android
# p4a.branch = 2024.01.21

# === УДАЛЕНО: p4a.requirements ===
# Эта строка дублирует requirements и вызывает конфликты. Не нужна!

# === Architecture ===
android.archs = arm64-v8a

# === Permissions ===
android.permissions = INTERNET,ACCESS_NETWORK_STATE

[buildozer]
# === Build Settings ===
log_level = 2
warn_on_root = 1
# Автоматически принимать лицензии (важно для CI/CD)
android.accept_sdk_license = True
# Включить кэш для ускорения повторных сборок в GitHub Actions
build_dir = .buildozer