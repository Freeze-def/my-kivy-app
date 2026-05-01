"""
🔥 Power Dashboard — Kivy App 🔥
Анимации • Математика • Интерактив • Неон
Создано для: @Freeze-def
"""

import random
import math
from time import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Circle, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.core.window import Window


# =============================================================================
# 🌌 Анимированный фон с частицами
# =============================================================================
class ParticleSystem(Widget):
    """Неоновые частицы, летающие по экрану"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self.max_particles = 30
        self.bind(pos=self.update_particles, size=self.update_particles)
        Clock.schedule_interval(self.update, 1/60)
        
        # Создаём частицы
        for _ in range(self.max_particles):
            self.spawn_particle()
    
    def spawn_particle(self):
        """Создать новую частицу"""
        particle = {
            'x': random.uniform(0, self.width),
            'y': random.uniform(0, self.height),
            'vx': random.uniform(-0.5, 0.5),
            'vy': random.uniform(-0.5, 0.5),
            'radius': random.uniform(2, 6),
            'color': [random.uniform(0.3, 1), random.uniform(0.3, 1), 1, 0.7],            'life': random.uniform(3, 8)
        }
        self.particles.append(particle)
    
    def update(self, dt):
        """Обновление частиц"""
        with self.canvas:
            # Очищаем старые частицы
            self.canvas.clear()
            Color(0.05, 0.05, 0.15, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            for p in self.particles[:]:
                # Движение
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= dt
                
                # Отскок от краёв
                if p['x'] < 0 or p['x'] > self.width:
                    p['vx'] *= -1
                if p['y'] < 0 or p['y'] > self.height:
                    p['vy'] *= -1
                
                # Умирающие частицы заменяем
                if p['life'] <= 0:
                    self.particles.remove(p)
                    self.spawn_particle()
                    continue
                
                # Рисуем частицу
                Color(*p['color'])
                Circle(pos=(p['x'], p['y']), radius=p['radius'])
                
                # Связи между близкими частицами
                for other in self.particles:
                    if p is other:
                        continue
                    dist = math.hypot(p['x'] - other['x'], p['y'] - other['y'])
                    if dist < 80:
                        alpha = (80 - dist) / 80 * 0.3
                        Color(p['color'][0], p['color'][1], 1, alpha)
                        Line(points=[p['x'], p['y'], other['x'], other['y']], width=1)
    
    def update_particles(self, *args):
        """При изменении размера окна"""
        for p in self.particles:
            p['x'] = min(p['x'], self.width)
            p['y'] = min(p['y'], self.height)

# =============================================================================
# 🔘 Кнопка с неоновым свечением и анимацией
# =============================================================================
class NeonButton(Button):
    """Кнопка с эффектом свечения при нажатии"""
    
    glow_intensity = NumericProperty(0)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Анимация "нажатия"
            Animation(scale=0.95, duration=0.1).start(self)
            Animation(glow_intensity=1, duration=0.15).start(self)
            return super().on_touch_down(touch)
        return False
    
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            Animation(scale=1, duration=0.1).start(self)
            Animation(glow_intensity=0, duration=0.3).start(self)
            return super().on_touch_up(touch)
        return False
    
    def on_press(self):
        # Вибрация (если поддерживается)
        try:
            from android import mActivity
            from android.jnius import cast
            from android.context import Context
            vibrator = mActivity.getSystemService(Context.VIBRATOR_SERVICE)
            vibrator.vibrate(50)
        except:
            pass  # Не критично
    
    def on_release(self):
        # Эффект "волны"
        pass


# =============================================================================
# 🧮 Математический виджет: визуализация π
# =============================================================================
class PiVisualizer(Widget):
    """Показывает цифры π с анимацией появления"""
    
    pi_text = StringProperty("3.")
    index = NumericProperty(1)
    
    def __init__(self, **kwargs):        super().__init__(**kwargs)
        self.pi_digits = str(math.pi).replace('.', '')[1:]  # цифры после запятой
        Clock.schedule_interval(self.add_digit, 0.08)
    
    def add_digit(self, dt):
        if self.index < len(self.pi_digits):
            self.pi_text += self.pi_digits[self.index]
            self.index += 1
            return True
        return False  # остановить планировщик


# =============================================================================
# 🎲 Генератор случайных чисел с анимацией
# =============================================================================
class RandomGenerator(Widget):
    """Крутая анимация генерации случайного числа"""
    
    current_value = StringProperty("0")
    is_generating = False
    
    def generate(self, min_val=1, max_val=999, callback=None):
        if self.is_generating:
            return
        
        self.is_generating = True
        steps = 20
        step = 0
        
        def animate(dt):
            nonlocal step
            step += 1
            if step < steps:
                # Быстрая "прокрутка" чисел
                self.current_value = str(random.randint(min_val, max_val))
            else:
                # Финальное значение
                result = random.randint(min_val, max_val)
                self.current_value = str(result)
                self.is_generating = False
                if callback:
                    callback(result)
                return False  # остановить
        
        Clock.schedule_interval(animate, 0.03)


# =============================================================================
# 🎨 Главный экран приложения
# =============================================================================class MainScreen(FloatLayout):
    """Основной интерфейс с карточками и анимациями"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        self.animate entrance()
    
    def build_ui(self):
        # === Фон ===
        self.particles = ParticleSystem(size_hint=(1, 1))
        self.add_widget(self.particles)
        
        # === Заголовок ===
        title = Label(
            text="⚡ POWER DASHBOARD ⚡",
            font_size=dp(28),
            bold=True,
            color=(0.9, 0.95, 1, 1),
            size_hint=(1, None),
            height=dp(60),
            pos_hint={'top': 0.95}
        )
        # Анимация появления заголовка
        title.opacity = 0
        self.add_widget(title)
        Animation(opacity=1, duration=0.8).start(title)
        
        # === Карточка: π Визуализатор ===
        pi_card = self.create_card(
            title="🌀 Число π",
            content=PiVisualizer(),
            pos_hint={'center_x': 0.5, 'y': 0.55}
        )
        self.add_widget(pi_card)
        
        # === Карточка: Генератор ===
        self.random_gen = RandomGenerator()
        rand_card = self.create_card(
            title="🎲 Случайное число",
            content=Label(
                text="0",
                font_size=dp(48),
                bold=True,
                color=(0.2, 1, 0.8, 1),
                text_size=(dp(200), None),
                halign='center'
            ),
            pos_hint={'center_x': 0.5, 'y': 0.35}
        )        # Связываем виджет с карточкой
        self.rand_label = rand_card.children[0].children[0]  # получаем Label
        self.add_widget(rand_card)
        
        # === Кнопка генерации ===
        gen_btn = NeonButton(
            text="🔥 СГЕНЕРИРОВАТЬ 🔥",
            size_hint=(None, None),
            size=(dp(220), dp(50)),
            pos_hint={'center_x': 0.5, 'y': 0.22},
            background_normal='',
            background_color=(0.2, 0.1, 0.4, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16),
            bold=True
        )
        gen_btn.bind(on_press=self.on_generate)
        self.add_widget(gen_btn)
        
        # === Статус бар ===
        self.status = Label(
            text="✅ Готов к работе",
            font_size=dp(14),
            color=(0.7, 0.9, 1, 0.8),
            size_hint=(1, None),
            height=dp(30),
            pos_hint={'x': 0, 'y': 0.02}
        )
        self.add_widget(self.status)
    
    def create_card(self, title, content, pos_hint):
        """Создать стильную карточку с заголовком"""
        card = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(280), dp(140)),
            pos_hint=pos_hint,
            padding=dp(12),
            spacing=dp(8)
        )
        
        # Фон карточки с градиентом (эмуляция)
        with card.canvas.before:
            Color(0.1, 0.15, 0.3, 0.85)
            Rectangle(pos=card.pos, size=card.size, radius=[12])
            Color(0.3, 0.6, 1, 0.4)
            Line(round_rectangle=(card.x, card.y, card.width, card.height, 12), width=2)
        
        # Заголовок карточки
        card_label = Label(            text=title,
            font_size=dp(16),
            bold=True,
            color=(0.9, 1, 1, 1),
            size_hint=(1, None),
            height=dp(25)
        )
        card.add_widget(card_label)
        
        # Контент
        content.size_hint = (1, 1)
        card.add_widget(content)
        
        return card
    
    def animate_entrance(self):
        """Анимация появления элементов"""
        for child in self.children[:]:
            if isinstance(child, BoxLayout):  # карточки
                child.opacity = 0
                child.y -= 50
                Animation(opacity=1, y=child.y + 50, duration=0.5, t='out_back').start(child)
    
    def on_generate(self, instance):
        """Обработчик кнопки генерации"""
        self.status.text = "🔄 Генерация..."
        
        def on_complete(value):
            self.rand_label.text = str(value)
            self.status.text = f"✅ Получено: {value}"
            # Анимация "успеха"
            anim = Animation(color=(0.2, 1, 0.8, 1), duration=0.2) + Animation(color=(0.9, 0.95, 1, 1), duration=0.3)
            anim.start(self.rand_label)
        
        self.random_gen.generate(callback=on_complete)
    
    def on_kv_lang_updated(self):
        """Обновить canvas при изменении размера"""
        for child in self.children:
            if hasattr(child, 'canvas'):
                child.canvas.ask_update()


# =============================================================================
# 🚀 Основное приложение
# =============================================================================
class PowerDashboardApp(App):
    """🔥 Главное приложение 🔥"""
    
    def build(self):        # Настройки окна
        Window.clearcolor = (0.05, 0.05, 0.12, 1)
        Window.borderless = False
        
        # Для мобильных: фиксация ориентации
        try:
            from android import activity
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PythonActivity.mActivity.setRequestedOrientation(
                autoclass('android.content.pm.ActivityInfo').SCREEN_ORIENTATION_PORTRAIT
            )
        except:
            pass  # Работает и без этого на ПК
        
        return MainScreen()
    
    def on_pause(self):
        # Сохранение состояния при сворачивании
        return True
    
    def on_resume(self):
        # Восстановление при возврате
        pass


# =============================================================================
# 🎯 Запуск
# =============================================================================
if __name__ == '__main__':
    PowerDashboardApp().run()