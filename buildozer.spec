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
android.api = 31
android.minapi = 21
android.ndk = 25c
android.sdk = 33

# Required for AIDL compilation
android.accept_sdk_license = True
android.arch = armeabi-v7a
android.gradle_dependencies = 
android.add_src = 

# Python for Android
p4a.branch = develop
p4a.requirements = python3,kivy,android

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 1
