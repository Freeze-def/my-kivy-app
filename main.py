"""
🔥 Power Dashboard — Kivy App 🔥
Анимации • Математика • Интерактив • Неон
"""

import random
import math
from time import time

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Circle, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window


class ParticleSystem(Widget):
    """Неоновые частицы"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self.max_particles = 30
        self.bind(pos=self.update_particles, size=self.update_particles)
        Clock.schedule_interval(self.update, 1/60)
        for _ in range(self.max_particles):
            self.spawn_particle()
    
    def spawn_particle(self):
        particle = {
            'x': random.uniform(0, self.width),
            'y': random.uniform(0, self.height),
            'vx': random.uniform(-0.5, 0.5),
            'vy': random.uniform(-0.5, 0.5),
            'radius': random.uniform(2, 6),
            'color': [random.uniform(0.3, 1), random.uniform(0.3, 1), 1, 0.7],
            'life': random.uniform(3, 8)
        }
        self.particles.append(particle)
    
    def update(self, dt):
        with self.canvas:
            self.canvas.clear()            Color(0.05, 0.05, 0.15, 1)
            Rectangle(pos=self.pos, size=self.size)
            for p in self.particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= dt
                if p['x'] < 0 or p['x'] > self.width:
                    p['vx'] *= -1
                if p['y'] < 0 or p['y'] > self.height:
                    p['vy'] *= -1
                if p['life'] <= 0:
                    self.particles.remove(p)
                    self.spawn_particle()
                    continue
                Color(*p['color'])
                Circle(pos=(p['x'], p['y']), radius=p['radius'])
                for other in self.particles:
                    if p is other:
                        continue
                    dist = math.hypot(p['x'] - other['x'], p['y'] - other['y'])
                    if dist < 80:
                        alpha = (80 - dist) / 80 * 0.3
                        Color(p['color'][0], p['color'][1], 1, alpha)
                        Line(points=[p['x'], p['y'], other['x'], other['y']], width=1)
    
    def update_particles(self, *args):
        for p in self.particles:
            p['x'] = min(p['x'], self.width)
            p['y'] = min(p['y'], self.height)


class NeonButton(Button):
    """Кнопка с неоновым эффектом"""
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Animation(scale=0.95, duration=0.1).start(self)
            return super().on_touch_down(touch)
        return False
    
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            Animation(scale=1, duration=0.1).start(self)
            return super().on_touch_up(touch)
        return False


class PiVisualizer(Widget):
    """Визуализация числа π"""
        pi_text = StringProperty("3.")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pi_digits = str(math.pi).replace('.', '')[1:]
        self.index = 0
        Clock.schedule_interval(self.add_digit, 0.08)
    
    def add_digit(self, dt):
        if self.index < len(self.pi_digits):
            self.pi_text += self.pi_digits[self.index]
            self.index += 1
            return True
        return False


class RandomGenerator:
    """Генератор случайных чисел"""
    
    def __init__(self, callback=None):
        self.callback = callback
        self.is_generating = False
    
    def generate(self, min_val=1, max_val=999):
        if self.is_generating:
            return
        self.is_generating = True
        steps = 20
        step = [0]
        
        def animate(dt):
            step[0] += 1
            if step[0] < steps:
                return str(random.randint(min_val, max_val))
            else:
                result = random.randint(min_val, max_val)
                self.is_generating = False
                if self.callback:
                    self.callback(result)
                return False
        Clock.schedule_interval(animate, 0.03)


class MainScreen(FloatLayout):
    """Главный экран"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        def build_ui(self):
        # Фон с частицами
        self.particles = ParticleSystem(size_hint=(1, 1))
        self.add_widget(self.particles)
        
        # Заголовок
        title = Label(
            text="⚡ POWER DASHBOARD ⚡",
            font_size=dp(28),
            bold=True,
            color=(0.9, 0.95, 1, 1),
            size_hint=(1, None),
            height=dp(60),
            pos_hint={'top': 0.95}
        )
        title.opacity = 0
        self.add_widget(title)
        Animation(opacity=1, duration=0.8).start(title)
        
        # Карточка π
        pi_card = self.create_card(
            title="🌀 Число π",
            content=PiVisualizer(),
            pos_hint={'center_x': 0.5, 'y': 0.55}
        )
        self.add_widget(pi_card)
        
        # Карточка генератора
        self.rand_label = Label(
            text="0",
            font_size=dp(48),
            bold=True,
            color=(0.2, 1, 0.8, 1),
            halign='center'
        )
        rand_card = self.create_card(
            title="🎲 Случайное число",
            content=self.rand_label,
            pos_hint={'center_x': 0.5, 'y': 0.35}
        )
        self.add_widget(rand_card)
        
        # Кнопка генерации
        gen_btn = NeonButton(
            text="🔥 СГЕНЕРИРОВАТЬ 🔥",
            size_hint=(None, None),
            size=(dp(220), dp(50)),
            pos_hint={'center_x': 0.5, 'y': 0.22},
            background_normal='',
            background_color=(0.2, 0.1, 0.4, 1),            color=(1, 1, 1, 1),
            font_size=dp(16),
            bold=True
        )
        gen_btn.bind(on_press=self.on_generate)
        self.add_widget(gen_btn)
        
        # Статус
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
        card = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(280), dp(140)),
            pos_hint=pos_hint,
            padding=dp(12),
            spacing=dp(8)
        )
        with card.canvas.before:
            Color(0.1, 0.15, 0.3, 0.85)
            Rectangle(pos=card.pos, size=card.size, radius=[12])
            Color(0.3, 0.6, 1, 0.4)
            Line(round_rectangle=(card.x, card.y, card.width, card.height, 12), width=2)
        card_label = Label(
            text=title,
            font_size=dp(16),
            bold=True,
            color=(0.9, 1, 1, 1),
            size_hint=(1, None),
            height=dp(25)
        )
        card.add_widget(card_label)
        content.size_hint = (1, 1)
        card.add_widget(content)
        return card
    
    def on_generate(self, instance):
        self.status.text = "🔄 Генерация..."
        
        def on_complete(value):
            self.rand_label.text = str(value)            self.status.text = f"✅ Получено: {value}"
            anim = Animation(color=(0.2, 1, 0.8, 1), duration=0.2) + Animation(color=(0.9, 0.95, 1, 1), duration=0.3)
            anim.start(self.rand_label)
        
        self.random_gen = RandomGenerator(callback=on_complete)
        self.random_gen.generate()


class PowerDashboardApp(App):
    """Главное приложение"""
    
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.12, 1)
        try:
            from android import activity
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            SCREEN_ORIENTATION_PORTRAIT = autoclass('android.content.pm.ActivityInfo').SCREEN_ORIENTATION_PORTRAIT
            PythonActivity.mActivity.setRequestedOrientation(SCREEN_ORIENTATION_PORTRAIT)
        except:
            pass
        return MainScreen()
    
    def on_pause(self):
        return True


if __name__ == '__main__':
    PowerDashboardApp().run()