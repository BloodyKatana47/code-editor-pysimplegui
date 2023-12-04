import PySimpleGUI as sg
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
element_size = (screensize[0] // 2, screensize[1] // 2)


# print(sg.theme_list())

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        return f'Error: {str(e)}'


def edit_file(content, path):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            new_content = file.write(content)
            return new_content
    except Exception as e:
        return f'Error: {str(e)}'


class MainWindow:
    def __init__(self):
        layout = [
            [sg.FileBrowse(button_text='Выбрать файл', key='-FILE-', enable_events=True, size=(10, 2))],
        ]

        self.window = sg.Window(
            title='Главное окно',
            layout=layout,
            resizable=True,
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
                content = read_file(file_path=file_path)
                self.content = content
                self.file_path = file_path

                self.window.close()
                file_view = FileViewWindow(content=self.content, file_path=self.file_path)
                file_view.run()

        self.window.close()


class FileViewWindow:
    def __init__(self, content, file_path):
        self.content = content
        self.file_path = file_path
        layout = [
            [sg.Multiline(self.content, auto_size_text=True, expand_x=True, expand_y=True, key='-MULTI-')],
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

        self.window.close()


main_window = MainWindow()
main_window.run()
