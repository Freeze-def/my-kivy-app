[app]
title = My Kivy App
package.name = mykivyapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.11,kivy
orientation = portrait
fullscreen = 0

# Android configuration
android.api = 33
android.minapi = 21
android.ndk = 25c
android.sdk = 33

# Use develop branch (stable and maintained)
p4a.branch = develop
p4a.requirements = python3==3.11,kivy,android

# Architecture
android.archs = arm64-v8a

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Build configuration
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
