import flet as ft
import math
import ast

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text

class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE
        self.expand = 1 

class ActionButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE
        self.expand = 1

class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK
        self.expand = 1

class ScientificButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.colors.GREEN
        self.color = ft.colors.WHITE
        self.expand = 1

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=30)
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20

        scientific_buttons = ft.Column(
            controls=[
                ScientificButton(text="√", button_clicked=self.button_clicked),
                ScientificButton(text="^", button_clicked=self.button_clicked),
                ScientificButton(text="sin", button_clicked=self.button_clicked),
                ScientificButton(text="cos", button_clicked=self.button_clicked),
                ScientificButton(text="tan", button_clicked=self.button_clicked),
            ],
            alignment="start",
            spacing=5,
            expand=False,  
        )

 
        main_buttons = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                        ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ],
                    spacing=5,
                ),
            ],
            spacing=5,
            expand=1,  
        )

        self.content = ft.Row(
            controls=[
                scientific_buttons,
                main_buttons,
            ],
            alignment="stretch",  
            spacing=10,
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")

        if data == "AC":
            self.result.value = "0"
            self.reset()

        elif data == "=":
            try:
                num_open = self.expression.count('(')
                num_close = self.expression.count(')')
                if num_open > num_close:
                    self.expression += ')' * (num_open - num_close)
                result = self.safe_eval(self.expression)
                self.result.value = str(result)
                self.expression = str(result)
            except Exception as ex:
                self.result.value = "Error"
                print(f"Error: {ex}")
                self.expression = ""
        elif data == "+/-":
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.result.value = self.expression
        elif data == "%":
            self.expression += '*0.01'
            self.result.value = self.expression
        else:
            if data == "√":
                self.expression += 'math.sqrt('
            elif data in ("sin", "cos", "tan"):
                self.expression += f"math.{data}(math.radians("
            elif data == "^":
                self.expression += '**'
            else:
                self.expression += data
            self.result.value = self.expression

        self.update()

    def safe_eval(self, expr):
        allowed_nodes = {
            ast.Expression, ast.Call, ast.Name, ast.Load, ast.BinOp, ast.UnaryOp,
            ast.Num, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
            ast.Mod, ast.USub, ast.Attribute
        }

        node = ast.parse(expr, mode='eval')

        for subnode in ast.walk(node):
            if type(subnode) not in allowed_nodes:
                raise ValueError("不正な式です")

        code = compile(node, '<string>', 'eval')
        return eval(code, {'__builtins__': None, 'math': math}, {})

    def reset(self):
        self.expression = ""

def main(page: ft.Page):
    page.title = "Calc App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    page.spacing = 0

    calc = CalculatorApp()
    page.add(calc)

ft.app(target=main)
