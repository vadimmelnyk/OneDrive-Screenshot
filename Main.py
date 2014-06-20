__author__ = 'Vadim Melnyk'
import OneDriveConnect
import OneDriveSend as onedrvSend
import Yourls
import Screenshot
import WindowsBalloonTip
import pythoncom
import pyHook

from Tkinter import Tk

import thread


def show_notification(title, text):
    notification = WindowsBalloonTip.WindowsBalloonTip(title, text)
    del notification

def copy_to_clipboard(short_link):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(short_link)
    r.destroy()

client_id = ''
client_secret = ''
scope = 'wl.signin wl.basic wl.offline_access'
response_type = 'code'
redirect_uri = 'https://login.live.com/oauth20_desktop.srf'


onedriveConnection = OneDriveConnect.OneDriveConnect(client_id,client_secret,scope,response_type,redirect_uri)
onedriveConnection.init_saved_values()
try:
    thread.start_new_thread(show_notification, ('OneDrive Screenshot', 'Application is running'))
except Exception, e:
    print "Error: unable to start thread: " + e
    exit(1)



def OnKeyboardEvent(event):
    if event.KeyID == 123:
        shot = Screenshot.Screenshot.make_full_screen()
        print "Screenshot is made..."
        onedriveConnection.refresh_token()
        access_token = onedriveConnection.access_token_value
        link = onedrvSend.OneDriveSend.upload_file(shot, access_token)
        print "Successfully uploaded to OneDrive. Getting short link..."
        yourls = Yourls.Yourls('domain_name', 'access_code')
        short_link = yourls.shorten_link(link, "test")
        ### Copy link to a clipboard
        copy_to_clipboard(short_link)
        ###

        ### Create a notification
        try:
            thread.start_new_thread(show_notification, ('OneDrive Screenshot', short_link + " has been copied to clipboard"))
        except Exception, e:
            print "Error: unable to start thread: " + e
            exit(1)
        ###

        print(short_link + ' has been copied to the clipboard')
    return True
while True:
            hm = pyHook.HookManager()
            hm.KeyDown = OnKeyboardEvent
            hm.HookKeyboard()
            pythoncom.PumpMessages()


