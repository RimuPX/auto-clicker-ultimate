from keyboard import _queue, _Event, _time, hook, unhook, add_hotkey, remove_hotkey
import threading
import keyboard as kb
import pyautogui
from dataclasses import dataclass

# speed steps mouse



class KeyBoardIO(object):

    @dataclass
    class _StructRecordTarget:
        _time: float = 0
        _posMouse: tuple = (0, 0)
        _keyEvents: list[object] = None


    event_end_work_record: bool = False
    def __init__(self):
        pass

    def __prepareProcessKeyEvent(self, triggerFn, finalizeFn, until: str, suppress: bool = False, trigger_on_release: bool = False):
        try:
            # ---  initialize ---
            target = _queue.Queue()

            def trigger(*args, **kwargs):
                triggerFn(*args, **kwargs)
                target.put(*args, **kwargs)
            # --- start listening press events ---
            hookTarget = hook(trigger)
            lock = _Event()

            def end(self):
                finalizeFn(self, list(target.queue))
                lock.set()
            # --- start waiting press end key ---
            remove = add_hotkey(until, lambda: end(self), suppress=suppress, trigger_on_release=trigger_on_release)
            lock.wait()
            remove_hotkey(remove)
            # --- finalize ---
            unhook(hookTarget)
            return True
        except Exception as e:
            print("file PyKey: SaveStateDoing.prepareProcessKeyEvent(): ", e)
            return False

    def record(self, buttonPressToEnd: str = 'esc', framesPosPerSecond=2):
        list_args: list = []
        self.event_end_work_record = False

        def edit_state_work(self, res):
            self.event_end_work_record = True
            print("key board record thread end work")

        def add_list(*args, **kwargs):
            list_args.append(args)

        thread = threading.Thread(
            target=self.__prepareProcessKeyEvent,
            args=(
                add_list,
                edit_state_work,
                buttonPressToEnd,
                False,
                False
            )
        )
        thread.start()

        result: list[SaveStateDoing._StructRecordTarget] = []
        frame = 1/framesPosPerSecond
        while not self.event_end_work_record:
            print("wait, do")
            obj = self._StructRecordTarget(
                _time.time(),
                pyautogui.position(),
                list_args.copy()
            )
            list_args.clear()
            result.append(obj)
            _time.sleep(frame)

        return result

    def play(self, inputData: list[_StructRecordTarget], buttonPressToStart: str = 'esc'):

        state = kb.stash_state()
        pyautogui.PAUSE = inputData[1]._time - inputData[0]._time
        for object in inputData:
            pos = object._posMouse
            print(f"move {pos[0]}:{pos[1]}")
            pyautogui.moveTo(pos[0], pos[1], duration=0)
            #print("press",key) if event.event_type == kb.KEY_DOWN else print("realese", key)

        kb.restore_modifiers(state)


temp = SaveStateDoing()

data = temp.record("esc", framesPosPerSecond=60)

temp.play(data)

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
