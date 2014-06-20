__author__ = 'Vadim Melnyk'
import pyscreenshot as ImageGrab
import re
import datetime

class Screenshot():
    @staticmethod
    def make_full_screen():

        now = re.sub(r'[^\d]', '', str(datetime.datetime.now()))

        # print now
        im = ImageGrab.grab_to_file(now+'.png')
        return str(now)+'.png'

    def make_part_of_the_screen(self):
        pass