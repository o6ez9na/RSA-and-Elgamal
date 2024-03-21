from textual.binding import \
    Binding  # Импорт класса Binding из модуля textual.binding для определения привязок клавиш к действиям
from rsa import *  # Импорт всех имен из модуля rsa для доступа к функциям RSA
from gamal import *  # Импорт всех имен из модуля gamal для доступа к функциям El'Gamal
from textual.app import App, ComposeResult, \
    on  # Импорт класса App, ComposeResult и декоратора on из модуля textual.app для создания приложения
from textual.widgets import Footer, Button, Input, Label, Rule, TabbedContent, TabPane, Log, \
    Switch  # Импорт виджетов из модуля textual.widgets для построения пользовательского интерфейса
from textual.containers import Horizontal, VerticalScroll, \
    Vertical  # Импорт контейнеров из модуля textual.containers для организации расположения виджетов
import time  # Импорт модуля времени для измерения времени выполнения программы


class RSA(App):  # Определение класса приложения RSA, который является подклассом класса App из библиотеки textual
    CSS_PATH = 'style.tcss'  # Путь к файлу CSS для стилизации приложения

    # Определение привязок клавиш к действиям
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),  # Привязка клавиши 'q' для выхода из приложения
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",  # Привязка клавиши '?' для отображения экрана помощи
        ),
        Binding(key="j", action="down", description="Scroll down", show=False),
        # Привязка клавиши 'j' для прокрутки вниз, но она не отображается в описании привязок
    ]

    # Метод для построения пользовательского интерфейса
    def compose(self) -> ComposeResult:
        with TabbedContent():  # Создание TabbedContent для организации вкладок в интерфейсе
            with TabPane("RSA"):  # Создание вкладки "RSA"
                yield Horizontal(  # Горизонтальное размещение виджетов
                    VerticalScroll(  # Вертикальная прокрутка для содержимого
                        Label("Сообщение, которе мы будем шифровать"),  # Текстовая метка
                        Input(placeholder="сообщение", id='message-input-field-rsa'),
                        # Поле ввода сообщения с идентификатором
                        Label('Перемешаем?'),  # Текстовая метка
                        Switch(id='radio-rsa'),  # Переключатель с идентификатором
                        Rule(line_style='double'),  # Горизонтальная линия-разделитель
                        Label("Галя, стартуем!"),  # Текстовая метка
                        Button.success("старт", id='btn-rsa'),  # Кнопка "старт" с идентификатором
                        Rule(line_style='double'),  # Горизонтальная линия-разделитель
                        Label('Лог:', id='label-log'),  # Текстовая метка с идентификатором
                        Log(id='right-side-label'),  # Журнал с идентификатором
                    ),
                )

            with TabPane("El'Gamal"):  # Создание вкладки "El'Gamal"
                yield Horizontal(  # Горизонтальное размещение виджетов
                    VerticalScroll(  # Вертикальная прокрутка для содержимого
                        Label("Сообщение, которе мы будем шифровать"),  # Текстовая метка
                        Input(placeholder="сообщение", id='message-input-field-gamal'),
                        # Поле ввода сообщения с идентификатором
                        Label('Перемешаем?'),  # Текстовая метка
                        Switch(id='radio-gamal'),  # Переключатель с идентификатором
                        Rule(line_style='double'),  # Горизонтальная линия-разделитель
                        Label('Галя, стартуем!'),  # Текстовая метка
                        Button.success("старт", id='btn-gamal'),  # Кнопка "старт" с идентификатором
                        Rule(line_style='double'),  # Горизонтальная линия-разделитель
                        Label('Лог:'),  # Текстовая метка
                        Log(id='left-side-label'),  # Журнал с идентификатором
                    )
                )
            with TabPane("О программе"):  # Создание вкладки "О программе"
                yield Log(id='about-program')  # Журнал с идентификатором для отображения информации о программе
        yield Footer()  # Отображение подвала

    # Метод, вызываемый при готовности приложения
    def on_ready(self) -> None:
        console = self.query_one('#about-program',
                                 Log)  # Получение доступа к журналу с идентификатором '#about-program'
        console.write(
            'Наша программа представляет собой инструмент для шифрования '
            'и дешифрования сообщений с использованием двух распространенных'
            ' криптогра-\nфических алгоритмов:\n\nRSA и ElGamal.'
            'RSA (Rivest-Shamir-Adleman) - это асимметричный криптографический'
            ' алгоритм, который использует пары ключей для шифрования\nи расшифрования'
            ' данных. Он основан на сложности факторизации больших простых '
            'чисел. Программа позволяет пользователю ввести сообщение,\nвыбрать'
            ' опцию перемешивания (если желает) и запустить процесс шифрования.'
            ' Затем она предоставляет результат шифрования вместе с сгене-\nрированными'
            ' ключами и временем выполнения.\n\nElGamal - еще один асимметричный алгоритм'
            ' шифрования, основанный на сложности задачи дискретного логарифмирования. '
            'Этот алгоритм также\nработает с парой ключей: открытым и закрытым. Пользователь '
            'может ввести сообщение, выбрать опцию перемешивания (если нужно) и запустить'
            '\nпроцесс шифрования. Программа выводит результат шифрования, сгенерированные '
            'ключи и время выполнения.\n\nНаша программа предоставляет простой и удобный'
            ' интерфейс для работы с этими двумя криптографическими алгоритмами, а также'
            ' демонстрирует\nих применение в практических сценариях.')

    @on(Button.Pressed, '#btn-rsa')
    def take_rsa(self, event: Button.Pressed):
        # Получаем доступ к виджету журнала для вывода результатов операции и к переключателю для опции перемешивания.
        log = self.query_one('#right-side-label', Log)
        radio_btn = self.query_one('#radio-rsa', Switch)

        # Очищаем журнал для вывода новых результатов.
        log.clear()

        # Получаем введенное пользователем сообщение и проверяем, что оно не пустое.
        input_message = self.query_one('#message-input-field-rsa', Input)
        send_input_message = input_message.value

        if send_input_message != '':

            # Выводим в журнал информацию о состоянии опции перемешивания.
            if radio_btn.value:
                log.write('ПЕРЕМЕШИВАНИЕ ВКЛЮЧЕНО')
            else:
                log.write('ПЕРЕМЕШИВАНИЕ ВЫКЛЮЧЕНО')

            # Выводим в журнал введенное пользователем сообщение.
            log.write(f'\nвведенное сообщение: {send_input_message}\n\n')
            time_start = time.time()
            # Запускаем функцию rsa_run, которая шифрует сообщение и возвращает результат.
            result = rsa_run(send_input_message, radio_btn.value)
            time_end = time.time()
            # Выводим в журнал сгенерированные ключи и временем выполнения операции.
            log.write(
                f'p => {result[4]}\n'
                f'q => {result[5]}\n\n'
                f'пары:\n\tпубличный ключ: {result[2][0]}\n'
                f'\tприватный ключ: {result[3][0]}\n\n'
                f'результат декодирования: {result[1]}\n'
                f'время работы программы: {time_end - time_start}')
            # Очищаем поле ввода и сбрасываем состояние переключателя.
            input_message.clear()
            radio_btn.value = False
        else:
            log.write_line('введите сообщение')

    @on(Button.Pressed, '#btn-gamal')
    def take_gamal(self, event: Button.Pressed):
        # Получаем доступ к виджету журнала для вывода результатов операции и к переключателю для опции перемешивания.
        log = self.query_one('#left-side-label', Log)
        log.clear()

        radio_btn = self.query_one('#radio-gamal', Switch)

        # Получаем введенное пользователем сообщение и проверяем, что оно не пустое.
        input_message = self.query_one('#message-input-field-gamal', Input)
        send_input_message = input_message.value

        if send_input_message != '':

            # Выводим в журнал информацию о состоянии опции перемешивания.
            if radio_btn.value:
                log.write('ПЕРЕМЕШИВАНИЕ ВКЛЮЧЕНО')
            else:
                log.write('ПЕРЕМЕШИВАНИЕ ВЫКЛЮЧЕНО')

            # Выводим в журнал введенное пользователем сообщение.
            log.write(f'\nвведенное сообщение: {send_input_message}\n\n')
            time_start = time.time()

            # Запускаем функцию gamal_run, которая шифрует сообщение и возвращает результат.
            result = gamal_run(send_input_message, radio_btn.value)

            time_end = time.time()
            # Выводим в журнал сгенерированные ключи и временем выполнения операции.
            log.write(f'\tоткрытый ключ:'
                      f'g => {result[1]}\n'
                      f'p => {result[2]}\n\n'
                      f'y => {result[0]}\n\n'
                      f'\tприватный ключ (x): {result[3]}\n\n'
                      f'\tшифротекст: {result[4], result[5]}\n\n'
                      f'результат декодирования: {result[6]}\n'
                      f'время работы программы: {time_end - time_start}')
            # Очищаем поле ввода и сбрасываем состояние переключателя.
            input_message.clear()
            radio_btn.value = False
        else:
            log.write('введите сообщение')


if __name__ == '__main__':
    # Создаем объект класса RSA и вызываем его метод run() для запуска приложения.
    app = RSA()
    app.run()
