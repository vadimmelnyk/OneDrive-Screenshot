__author__ = 'Vadim Melnyk'
import pythoncom
import pyHook

key1 = -1

def OnKeyboardEvent(event):

    #print 'KeyID:', event.KeyID
    global key1
    key1 = event.KeyID

    return True


class KeyListener():
    @staticmethod
    def start_listening():
        while True:
            hm = pyHook.HookManager()
            hm.KeyDown = OnKeyboardEvent
            hm.HookKeyboard()
            pythoncom.PumpMessages()