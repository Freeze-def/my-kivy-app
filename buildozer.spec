[app]
title = My Kivy App
package.name = mykivyapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Android configuration
android.api = 33
android.minapi = 21
android.ndk = 25c
android.sdk = 33

# Use release branch instead of master
p4a.branch = release-2024.12.1
p4a.requirements = python3,kivy,android

# Architecture
android.archs = armeabi-v7a,arm64-v8a

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Build configuration
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
