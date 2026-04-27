from kivy.app import App
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        # Создаем кнопку с текстом
        btn = Button(text='Hello from GitHub Actions!',
                     font_size=20,
                     background_color=(0, 1, 0, 1)) # Зеленая кнопка
        
        # Привязываем действие при нажатии
        btn.bind(on_press=self.on_button_press)
        return btn

    def on_button_press(self, instance):
        instance.text = 'Clicked!'
        instance.background_color = (1, 0, 0, 1) # Становится красной

if __name__ == '__main__':
    MyApp().run()
