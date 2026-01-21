from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, RoundedRectangle


class MainApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = False
        self.last_button = None

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=5)

        with main_layout.canvas.before:
            Color(0.5, 0.5, 0.5, 1) # cor do fundo
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)

        main_layout.bind(pos=self._update_bg, size=self._update_bg)

        self.solution = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=60,
            padding_y=(10),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            
        )

        main_layout.add_widget(self.solution)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(
            text="=",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if self.solution.text == "Erro" and button_text.isdigit():
            self.solution.text = ""
            return

        if button_text == "C":
            self.solution.text = ""
            return
        
        if current == "0" and button_text.isdigit():
            self.solution.text = button_text
            return

        if current and (self.last_was_operator and button_text in self.operators):
            return

        if button_text == "." and "." in current:
            return

        self.solution.text += button_text
        self.last_was_operator = button_text in self.operators
        self.last_button = button_text

    def on_solution(self, instance):
        try:
            self.solution.text = str(eval(self.solution.text))
        except Exception:
            self.solution.text = "Erro"

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

if __name__ == "__main__":
    MainApp().run()
