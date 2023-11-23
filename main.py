from enum import Enum
import flet as ft
import pyautogui
from pynput import mouse, keyboard

is_execute = False
task_index = 0


class TaskType(Enum):
    Move = 0
    Click = 1
    Write = 2


def main(page: ft.Page):
    pyautogui.FAILSAFE = True
    page.window_width = 640
    page.window_height = 480
    page.window_resizable = False
    page.window_maximizable = False
    page.title = "Rokuma"
    page.scroll = "always"
    task_list = list()
    page.padding = 10
    global is_execute

    def add_clicked(e):
        global task_index
        page.add(ft.Checkbox(label=f"id: {task_index}, task: ({input_x.value}, {input_y.value})"))
        task_list.append({'id': task_index, 'type': TaskType.Move, 'op': (input_x.value, input_y.value)})
        task_index += 1
        view.update()

    def add_textfield(e):
        global task_index
        page.add(ft.Checkbox(label=f"id: {task_index}, task: {input_field.value}"))
        task_list.append({'id': task_index, 'type': TaskType.Write, 'op': input_field.value})
        task_index += 1
        view.update()

    def play(e):
        exec_button.bgcolor = ft.colors.CYAN
        pause_button.bgcolor = ft.colors.GREY
        view.update()
        global is_execute
        is_execute = True
        while is_execute:
            for task in task_list:
                if is_execute is False:
                    break
                if task['type'] == TaskType.Move:
                    pyautogui.moveTo(task['op'][0], task['op'][1], 0.9)
                elif task['type'] == TaskType.Write:
                    pyautogui.click()
                    pyautogui.write(task['op'], 0.1)
                print(task['op'])
            page.update()

    def pause(e):
        exec_button.bgcolor = ft.colors.GREY
        pause_button.bgcolor = ft.colors.CYAN
        view.update()
        global is_execute
        is_execute = False

    # 中クリックで位置保存
    def on_click(x, y, button, pressed):
        if not pressed and str(button) == "Button.middle":
            input_x.value = x
            input_y.value = y
            view.update()

    def on_press(key):
        global is_execute
        try:
            if key == keyboard.Key.esc:
                exec_button.bgcolor = ft.colors.GREY
                pause_button.bgcolor = ft.colors.CYAN
                view.update()
                is_execute = False
                print('excute paused')
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    add_position_button = ft.FloatingActionButton(icon=ft.icons.ADD_ROUNDED, on_click=add_clicked)
    add_keyboard_button = ft.FloatingActionButton(icon=ft.icons.ADD_ROUNDED, on_click=add_textfield)
    exec_button = ft.FloatingActionButton(icon=ft.icons.PLAY_ARROW, on_click=play, bgcolor=ft.colors.GREY)
    pause_button = ft.FloatingActionButton(icon=ft.icons.PAUSE, on_click=pause, bgcolor=ft.colors.CYAN)

    input_x = ft.TextField(hint_text="Position X", expand=True)
    input_y = ft.TextField(hint_text="Position Y", expand=True)
    input_field = ft.TextField(hint_text="Input words", expand=True)
    task_view = ft.Column()
    view = ft.Column(
        width=600,
        controls=[
            ft.Row(
                controls=[
                    pause_button,
                    exec_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    input_field,
                    add_keyboard_button,
                ]
            ),
            ft.Row(
                controls=[
                    input_x,
                    input_y,
                    add_position_button
                ]
            ),
            task_view,
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)

    key_listener = keyboard.Listener(
        on_press=on_press,
    )
    key_listener.start()

    mouse_listener = mouse.Listener(
        on_click=on_click,
    )
    mouse_listener.start()


ft.app(target=main)
