from json import dump, load
from typing import Union

import PySimpleGUI as sg

import ctypes

# user32 = ctypes.windll.user32
# width = user32.GetSystemMetrics(0)
# height = user32.GetSystemMetrics(1)

width = 1366
height = 768
element_size = (width // 2, height // 2)


# print(sg.theme_list())

def read_file(path: str) -> str:
    """Read a file and return its contents."""
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        return f'Error: {str(e)}'


def edit_file(content: str, path: str) -> Union[int, str]:
    """Edit a file and save it."""
    try:
        with open(path, 'w', encoding='utf-8') as file:
            new_content = file.write(content)
            return new_content
    except Exception as e:
        return f'Error: {str(e)}'


def set_config(theme: str) -> Union[None, str]:
    """Set the theme."""
    try:
        with open('config.json', 'w') as file:
            value = {'theme': theme}
            dump(value, file)
    except Exception as e:
        return f'Error: {str(e)}'


def get_config() -> Union[dict, str]:
    """Read config.json and return theme."""
    try:
        with open('config.json', 'r') as file:
            data = load(file)
            return data
    except Exception as e:
        return f'Error: {str(e)}'


class MainWindow:
    """Responsible for displaying main window content."""

    def __init__(self):
        # tab_layout = [
        #     [sg.Multiline(self.content, auto_size_text=True, expand_x=True, expand_y=True, key='-MULTI-')],
        # ]
        # layout = [
        #     [sg.TabGroup(layout=[
        #         [sg.Tab(title=f'{self.file_path.split("/")[-1]}', layout=tab_layout)],
        #     ], expand_y=True, expand_x=True)],
        #     [sg.Button(button_text='Назад', key='-BACK-', enable_events=True)],
        # ]

        config_theme = get_config()

        self.theme = config_theme.get('theme') if config_theme else 'BrightColors'

        sg.theme(self.theme)

        main_layout = [
            [sg.FileBrowse(button_text='Выбрать файл', key='-FILE-', enable_events=True, size=(10, 2))],
        ]

        settings_layout = [
            [sg.Text(text='Настройки темы')],
            [sg.Listbox(sg.theme_list(), size=(25, 16), enable_events=True, key='-THEME-')],
            # [sg.Checkbox(text='Автосохранение файла', default=False, key='-AUTOSAVE-')],
        ]

        layout = [
            [sg.TabGroup(layout=[
                [sg.Tab(title='Main', layout=main_layout)],
                [sg.Tab(title='Settings', layout=settings_layout)],
            ], expand_x=True, expand_y=True)],
            # [sg.Button(
            #     button_text='Настройки',
            #     key='-SETTINGS-',
            #     enable_events=True,
            #     size=(10, 2),
            #     pad=((1, 0), (280, 0)),
            # )],
        ]

        self.window = sg.Window(
            title='Главное окно',
            layout=layout,
            resizable=False,
            size=(element_size[0], element_size[1])
        )

        self.content = None
        self.file_path = None

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == '-FILE-':
                file_path = values['-FILE-']
                content = read_file(path=file_path)
                self.content = content
                self.file_path = file_path

                self.window.close()
                file_view = FileViewWindow(content=self.content, file_path=self.file_path)
                file_view.run()

            elif event == '-SETTINGS-':
                self.window.close()
                settings_window = SettingsWindow()
                settings_window.run()

            elif event == '-THEME-':
                set_config(values[event][0])

                self.window.close()

                main_window = MainWindow()
                main_window.run()

        self.window.close()


class FileViewWindow:
    """Responsible for displaying the content of a file."""

    def __init__(self, content: str, file_path: str):
        self.content = content
        self.file_path = file_path
        tab_layout = [
            [sg.Multiline(self.content, auto_size_text=True, expand_x=True, expand_y=True, key='-MULTI-')],
        ]
        layout = [
            [sg.TabGroup(layout=[
                [sg.Tab(title=f'{self.file_path.split("/")[-1]}', layout=tab_layout)],
            ], expand_y=True, expand_x=True)],
            [sg.Button(button_text='Назад', key='-BACK-', enable_events=True)],
        ]
        self.window = sg.Window(
            title='Просмотр файла',
            layout=layout,
            resizable=True,
        ).Finalize()
        self.window.Maximize()
        self.window.bind(bind_string="<Control_L><s>", key='-SAVE-')

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == '-BACK-':
                self.window.close()

                main_window = MainWindow()
                main_window.run()

            elif event == '-SAVE-':
                new_text = values['-MULTI-']
                new_content = edit_file(path=self.file_path, content=str(new_text))
                self.content = new_content
                sg.Popup('Сохранено!')

        self.window.close()


class SettingsWindow:
    def __init__(self):
        layout = [
            [sg.Listbox(sg.theme_list(), size=(15, 5), select_mode=True)],
            [sg.Button(button_text='Назад', key='-BACK-', enable_events=True)],
        ]

        self.window = sg.Window(
            title='Настройки',
            layout=layout,
            resizable=True,
            size=(element_size[0], element_size[1])
        )

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == '-BACK-':
                self.window.close()

                main_window = MainWindow()
                main_window.run()

            elif event == '-SAVE-SETTINGS-':
                print('Button')

        self.window.close()


main_window = MainWindow()
main_window.run()
