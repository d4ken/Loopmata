import uuid
from enum import Enum
import flet as ft
import pyautogui
from pynput import mouse, keyboard
import pretty_errors
from rich import print

pretty_errors.activate()
is_execute = False


class TaskType(Enum):
    Click = 1
    Write = 2
    Drag = 3


def main(page: ft.Page):
    pyautogui.FAILSAFE = True
    page.window_width = 640
    page.window_height = 840
    page.window_resizable = False
    page.window_maximizable = False
    page.title = "Loopmata"
    page.scroll = "always"
    page.padding = 10
    task_dict = dict()
    global is_execute

    def add_task(e, task_type):
        if delta_x.value == "":
            delta_x.value = 0
        if delta_y.value == "":
            delta_y.value = 0
        if mouse_duration.value == "":
            mouse_duration.value = 30
        if key_input_duration.value == "":
            key_input_duration.value = 10

        cbx = ft.Checkbox()
        operation_dict = dict()
        id = uuid.uuid4()
        if task_type == TaskType.Click:
            if delta_x != 0 or delta_y != 0:
                cbx = ft.Checkbox(
                    label=f"{task_type.name} : ({input_x.value}, {input_y.value}), delta : ({int(delta_x.value)}, {int(delta_y.value)}), duration: {mouse_duration.value}ms")
                operation_dict = {'id': id, 'type': task_type, 'op': (input_x.value, input_y.value),
                                  'delta': (int(delta_x.value), int(delta_y.value)),
                                  'duration': mouse_duration.value}
            else:
                cbx = ft.Checkbox(
                    label=f"CLICK : ({input_x.value}, {input_y.value}), duration: {mouse_duration.value}ms")
                operation_dict = {'id': id, 'type': task_type, 'op': (input_x.value, input_y.value),
                                  'duration': mouse_duration.value}

        elif task_type == TaskType.Write:
            cbx = ft.Checkbox(label=f"{task_type.name} : {input_field.value}, duration: {key_input_duration.value}ms")
            operation_dict = {'id': id, 'type': task_type, 'op': input_field.value,
                              'duration': key_input_duration.value}
        task = ft.Row(
            [
                cbx,
                ft.IconButton(icon=ft.icons.DELETE_SHARP, on_click=lambda e: delete_task(task)),
                ft.IconButton(icon=ft.icons.COPY_SHARP, on_click=lambda e: copy_task(task)),
            ])
        task.data = operation_dict
        task_dict.update({id: operation_dict})
        task_view.controls.append(task)
        view.update()

    def delete_task(e):
        id = e.data['id']
        task_view.controls.remove(e)
        task_dict.pop(id)
        view.update()

    # 選択タスクをコピーして追加
    def copy_task(e):
        print(e.data)
        if e.data['type'] == TaskType.Click:
            input_x.value = e.data['op'][0]
            input_y.value = e.data['op'][1]
            delta_x.value = e.data['delta'][0]
            delta_y.value = e.data['delta'][1]
        add_task(e, TaskType.Click)
        view.update()

    def clear_all_task(e):
        task_dict.clear()
        task_view.controls.clear()
        view.update()

    def add_clicked(e):
        if input_x.value == "" or input_y.value == "":
            return
        add_task(e, TaskType.Click)

    def add_drag(e):
        if input_x.value == "" or input_y.value == "":
            return
        add_task(e, TaskType.Drag)

    def add_textfield(e):
        if input_field.value == "":
            return
        add_task(e, TaskType.Write)

    def play(e):
        if len(task_dict) == 0:
            return
        exec_button.bgcolor = ft.colors.CYAN
        pause_button.bgcolor = ft.colors.GREY
        view.update()
        global is_execute
        is_execute = True
        counter = 0
        while is_execute and counter < int(loop_count.value):
            print(counter)
            for task in task_dict.values():
                if is_execute is False:
                    break
                if task['type'] == TaskType.Click:
                    pyautogui.moveTo(int(task['op'][0]) + counter * int(task['delta'][0]),
                                     int(task['op'][1]) + counter * int(task['delta'][1]), int(task['duration']) / 1000,
                                     pyautogui.easeOutQuad)
                    pyautogui.click()

                elif task['type'] == TaskType.Drag:
                    pyautogui.mouseDown()
                    pyautogui.dragTo(int(task['op'][0]) + counter * int(task['delta'][0]),
                                     int(task['op'][1]) + counter * int(task['delta'][1]), int(task['duration']) / 1000,
                                     button='left')
                    pyautogui.mouseUp()

                elif task['type'] == TaskType.Write:
                    pyautogui.write(task['op'], int(task['duration']) / 1000)

                print(f"{task['type']}: {task['op']}")
            counter += 1
            if counter == int(loop_count.value):
                exec_button.bgcolor = ft.colors.GREY
                pause_button.bgcolor = ft.colors.CYAN
                print("End Loop")
            page.update()

    def pause(e):
        exec_button.bgcolor = ft.colors.GREY
        pause_button.bgcolor = ft.colors.CYAN
        view.update()
        global is_execute
        is_execute = False

    def on_click(x, y, button, pressed):
        # 中クリックの場合
        if not pressed and str(button) == "Button.middle":
            input_x.value = int(x)
            input_y.value = int(y)
            # 増分初期化
            delta_x.value = 0
            delta_y.value = 0
            view.update()

    def update_position(x, y):
        current_x_text.value = int(x)
        current_y_text.value = int(y)
        if input_x.value != "" and input_y.value != "":
            delta_x_text.value = int(x - input_x.value)
            delta_y_text.value = int(y - input_y.value)
        view.update()

    def on_press(key):
        global is_execute
        try:
            if key == keyboard.Key.f9:
                exec_button.bgcolor = ft.colors.GREY
                pause_button.bgcolor = ft.colors.CYAN
                view.update()
                is_execute = False
                print('excute paused')

        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    add_click_pos_button = ft.FloatingActionButton(icon=ft.icons.ADD_ROUNDED, on_click=add_clicked)
    add_drag_pos_button = ft.FloatingActionButton(icon=ft.icons.ADD_ROUNDED, on_click=add_drag)
    add_keyboard_button = ft.FloatingActionButton(icon=ft.icons.ADD_ROUNDED, on_click=add_textfield)
    clear_all_task_button = ft.IconButton(icon=ft.icons.CLEAR_ALL, on_click=clear_all_task, tooltip="Clear Operation")

    exec_button = ft.FloatingActionButton(icon=ft.icons.PLAY_ARROW, on_click=play, bgcolor=ft.colors.GREY,
                                          tooltip="Play")
    pause_button = ft.FloatingActionButton(icon=ft.icons.PAUSE, on_click=pause, bgcolor=ft.colors.CYAN,
                                           tooltip="Pause (F9)")
    loop_count = ft.TextField(expand=False, width=80, input_filter=ft.NumbersOnlyInputFilter(),
                              value="3")
    input_x = ft.TextField(hint_text="Pos X", expand=False, width=80, input_filter=ft.NumbersOnlyInputFilter())
    input_y = ft.TextField(hint_text="Pos Y", expand=False, width=80, input_filter=ft.NumbersOnlyInputFilter())
    delta_x = ft.TextField(hint_text="Delta X", expand=False, width=80, input_filter=ft.NumbersOnlyInputFilter())
    delta_y = ft.TextField(hint_text="Delta Y", expand=False, width=80,
                           input_filter=ft.NumbersOnlyInputFilter())

    # リアルタイム表示テキスト
    current_x_text = ft.Text(value="0")
    current_y_text = ft.Text(value="0")
    delta_x_text = ft.Text(value="0")
    delta_y_text = ft.Text(value="0")

    mouse_duration = ft.TextField(hint_text="Duration(ms)", expand=False, value="150",
                                  input_filter=ft.NumbersOnlyInputFilter(), width=100)
    input_field = ft.TextField(hint_text="Input words here...", expand=True)
    key_input_duration = ft.TextField(hint_text="Duration(ms)", expand=False, width=70, value="100",
                                      input_filter=ft.NumbersOnlyInputFilter(), tooltip="Type Per ms")

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
            ft.Text(value="⌨ KEY INPUT", size=20, weight=ft.FontWeight.W_700),
            ft.Row(
                controls=[
                    ft.Text(value="Typing : ", size=16, weight=ft.FontWeight.W_600),
                    input_field,
                    key_input_duration,
                    add_keyboard_button,
                ]
            ),
            ft.Container(
                # bgcolor=ft.colors.GREY,
                padding=5,
            ),
            ft.Text(value="🖱 MOUSE INPUT", size=20, weight=ft.FontWeight.W_700,
                    tooltip="Add mouse position with middle click"),
            ft.Row(
                controls=[
                    ft.Column(
                        [
                            ft.Row(
                                controls=[
                                    ft.Text(value="Position : ", size=16, weight=ft.FontWeight.W_600),
                                    input_x,
                                    input_y,
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(value="Loop Delta : ", size=16, weight=ft.FontWeight.W_600),
                                    delta_x,
                                    delta_y,
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(value="Mouse Duration (ms): ", size=16, weight=ft.FontWeight.W_600),
                                    mouse_duration,
                                ]
                            ),
                        ]
                    ),
                    ft.Container(
                        padding=10,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(value="⏳ Realtime Info", size=20, weight=ft.FontWeight.W_600),
                            ft.Row(
                                controls=[
                                    ft.Text(value=f"Current Position: ( x:"),
                                    current_x_text,
                                    ft.Text(value=", y:"),
                                    current_y_text,
                                    ft.Text(value=")")
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(value=f"Previous Delta: ( x:"),
                                    delta_x_text,
                                    ft.Text(value=", y:"),
                                    delta_y_text,
                                    ft.Text(value=")")
                                ]
                            ),
                            ft.Container(
                                padding=10
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(value="Click : ", size=16, weight=ft.FontWeight.W_600),
                                    add_click_pos_button,
                                    ft.Container(
                                        padding=5,
                                    ),
                                    ft.Text(value="Drag : ", size=16, weight=ft.FontWeight.W_600),
                                    add_drag_pos_button
                                ],
                            ),
                        ]
                    )
                ]
            ),
            ft.Container(
                padding=5,
            ),
            ft.Row(
                controls=[
                    ft.Text(value="🤖 OPERATION", size=20, weight=ft.FontWeight.W_700),
                    ft.Container(padding=5),
                    clear_all_task_button
                ]
            ),
            ft.Row(
                controls=[
                    ft.Text(value="🔁 Operation Loop Count : ", size=16, weight=ft.FontWeight.W_600),
                    loop_count,
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
        on_move=update_position,
    )
    mouse_listener.start()


ft.app(target=main)
