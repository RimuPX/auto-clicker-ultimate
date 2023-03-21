from keyboard import (_queue, _Event, _time,
                      hook, unhook,
                      add_hotkey, remove_hotkey,
                      press, release,
                      KEY_UP, KEY_DOWN)
from threading import Thread
import keyboard as kb
import pyautogui
from dataclasses import dataclass
from pynput.mouse._win32 import Listener
from pynput.mouse._win32 import Controller
# speed steps mouse



class KeyBoardIO(object):

    @dataclass
    class _StructRecordTarget:
        _time: float = 0
        _posMouse: tuple = (0, 0)
        _keyEvents: list[object] = None
        _mouseEvents: list[object] = None
        _scrollParameters: list[float] = None

    event_end_work_record: bool = False
    event_end_work_Loop: bool = False

    mouse: Controller = None
    debug: bool = False

    def __init__(self):
        self.mouse = Controller()

    @staticmethod
    def __prepareProcessKeyEvent(
            triggerFn, finalizeFn, until: str,
            suppress: bool = False, trigger_on_release: bool = False) -> bool:
        # args:
        #   triggerFn - функция, в которую передают событие об нажатии на кнопку клавиатуры
        #   finalizeFn - функция, в которую передают весь список ивентов и сообщает о конце работы __prepareProcessKeyEvent (т.к. была нажата кнопка until)
        #   until - название кнопки, после нажатие которой будет вызван finalizeFn и функция __prepareProcessKeyEvent вернет True
        #   suppress - ...
        #   trigger_on_release - ...
        # return:
        #   bool - успешно окончилась ли функция __prepareProcessKeyEvent или нет
        try:
            # ---  initialize ---
            target = _queue.Queue()

            def trigger(*args, **kwargs):
                triggerFn(*args, **kwargs)
                target.put(*args, **kwargs)
            # --- start listening press events ---
            hookTarget = hook(trigger)
            lock = _Event()

            def end():
                finalizeFn(list(target.queue))
                lock.set()
            # --- start waiting press end key ---
            remove = add_hotkey(until, end, suppress=suppress, trigger_on_release=trigger_on_release)
            lock.wait()
            remove_hotkey(remove)
            # --- finalize ---
            unhook(hookTarget)
            return True
        except Exception as e:
            print("file PyKey: KeyBoardIO.prepareProcessKeyEvent(): ", e)
            return False

    @staticmethod
    def __prepareProcessMouseEvent(stopper, moveFn, clickFn, scrollFn) -> bool:
        # args:
        #   stopper - функция, в которую передают Thread объект Listener, с целью, чтобы остановить процесс сбора ивентов с мыши
        #   moveFn - функция, в которую передают положение мышки
        #   clickFn - функция, в которую передают параметры нажатой кнопки мыши
        #   scrollFn - функция, в которую передают параметры скролла мыши
        # return:
        #   bool - успешно ли окончилась функция __prepareProcessMouseEvent или нет
        try:
            with Listener(on_move=moveFn, on_click=clickFn, on_scroll=scrollFn) \
                    as listener:
                stopper(listener)
                listener.join()
                print("mouse record thread end work")
            return True
        except Exception as e:
            print("file PyKey: KeyBoardIO.__prepareProcessMouseEvent(): ")
            return False

    def record(self, buttonPressToEnd: str = 'esc', framesPosPerSecond=2):
        list_keyboard: list = []
        list_mouse: list = []
        list_scroll: list = []
        self.event_end_work_record = False

        # -- functions for keyboard --
        def add_list_KeyBoardEvents(*args, **kwargs):
            list_keyboard.append(args[0])

        # -- functions for mouse --
        def add_list_mouseClick(*args, **kwargs):
            btn = args[2]
            btnState = args[3]
            list_mouse.append((btn, btnState))

        def add_list_mouseScroll(*args, **kwargs):
            list_scroll.append(args[3])


        stopWorkBool: list = [] # служит чтобы принять с ThreadKeyBoard об окончании работы
        listenerObj: list = [] # служит чтобы принять с ThreadMouse инстанс класса Listener

        # -- for get pynput.mouse._win32.Listener and end process --
        def get_listener(listener):
            listenerObj.append(listener)

        # -- for end loop and mouse process --
        def edit_state_work(res):
            stopWorkBool.append(True)
            listenerObj[0].stop()
            print("key board record thread end work")

        mouse_thread = Thread(
            target=self.__prepareProcessMouseEvent,
            args=(
                get_listener,
                lambda *args:None, add_list_mouseClick, add_list_mouseScroll
            )
        )
        mouse_thread.start()


        kb_thread = Thread(
            target=self.__prepareProcessKeyEvent,
            args=(
                add_list_KeyBoardEvents,
                edit_state_work,
                buttonPressToEnd,
                False,
                False
            )
        )
        kb_thread.start()

        result: list[KeyBoardIO._StructRecordTarget] = []
        frame = 1/framesPosPerSecond
        while not stopWorkBool:
            # print("recording....")
            obj = self._StructRecordTarget(
                _time.time(),
                pyautogui.position(),
                list_keyboard.copy(),
                list_mouse.copy(),
                list_scroll.copy()
            )
            list_keyboard.clear()
            list_mouse.clear()
            list_scroll.clear()
            result.append(obj)
            _time.sleep(frame)

        return result

    def play(self, inputData: list[_StructRecordTarget], buttonPressToStart: str = 'esc', speed_factors: tuple[float] = (1, 0.001, 0.001)):

        state = kb.stash_state()
        pyautogui.PAUSE = inputData[1]._time - inputData[0]._time

        speed_factor = speed_factors[0]
        wait_mouse = speed_factors[1]
        wait_scroll = speed_factors[2]

        for obj in inputData:
            # -- move mouse --
            pos = obj._posMouse
            eventsKB = obj._keyEvents
            eventsMouse = obj._mouseEvents
            eventsScroll = obj._scrollParameters
            # print(f"move {pos[0]}:{pos[1]}, events {eventsKB}, {eventsMouse}, {eventsScroll}")
            pyautogui.moveTo(pos[0], pos[1], duration=0)

            last_time = None
            if eventsKB:
                # -- press keys, if have (eventsKB) --
                for event in eventsKB:
                    if speed_factor > 0 and last_time is not None:
                        _time.sleep((event.time - last_time) / speed_factor)
                    last_time = event.time

                    key = event.scan_code or event.name
                    print(key)
                    press(key) if event.event_type == KEY_DOWN else release(key)

            if eventsMouse:
                # -- press mouse keys, if have (eventsMouse) --
                for event in eventsMouse:
                    objBtn = event[0]
                    stateBtn = event[1]
                    if stateBtn:
                        self.mouse.press(objBtn)
                    else:
                        self.mouse.release(objBtn)
                    _time.sleep(wait_mouse)

            if eventsScroll:
                for event in eventsScroll:
                    self.mouse.scroll(0, event)
                    _time.sleep(wait_scroll)

        kb.restore_modifiers(state)


if __name__ == "__main__":

    temp = KeyBoardIO()
    data = temp.record("esc", framesPosPerSecond=60)
    temp.play(
        data,
        speed_factors=(
            1, 0.001, 0.001
        )
    )

#
# keyboard.press_and_release('shift+s, space')
#
# keyboard.write('The quick brown fox jumps over the lazy dog.')
#
# keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))
#
# # Press PAGE UP then PAGE DOWN to type "foobar".
# keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))
#
# # Blocks until you press esc.
# keyboard.wait('esc')
#
# # Record events until 'esc' is pressed.
# recorded = keyboard.record(until='esc')
# # Then replay back at three times the speed.
# keyboard.play(recorded, speed_factor=3)
#
# # Type @@ then press space to replace with abbreviation.
# keyboard.add_abbreviation('@@', 'my.long.email@example.com')
#
# # Block forever, like `while True`.
# keyboard.wait()
