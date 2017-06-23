#!/usr/bin/env python3
import time
from thirdparty.colorama import init, Fore, Style, Back


class Output:
    def __init__(self):
        init()
        self.ORIG = Style.NORMAL + Fore.RESET
        self.HEADER = Back.CYAN + Style.BRIGHT + Fore.WHITE
        self.BR_GREEN = Style.BRIGHT + Fore.GREEN
        self.BR_CYAN = Style.BRIGHT + Fore.CYAN
        self.BR_YELLOW = Style.BRIGHT + Fore.YELLOW
        self.BR_RED = Style.BRIGHT + Fore.RED
        self.BR_MAGENTA = Style.BRIGHT + Fore.MAGENTA

    def page_found(self, message, indent):
        output = "[{0}200 - OK{1}] {2}".format(self.BR_GREEN, self.ORIG, message)

        if indent:
            print("\t", output)
        else:
            print(output)

    def progress(self, message, indent = False):
        output = "[{0}+{1}] {2}".format(self.BR_YELLOW, self.ORIG, message)

        if indent:
            print("\t", output)
        else:
            print(output)

    def negative(self, message):
        print("[{0}-{1}] {2}".format(self.BR_RED, self.ORIG, message))

    def status(self, message):
        print("[{0}*{1}] {2}".format(self.BR_CYAN, self.ORIG, message))

    def error(self, message):
        print("[{0}ERROR{1}] {2}".format(self.BR_RED, self.ORIG, message))

    def show_header(self, pause_time):
        print("{0}  / _ \\{1}\t\t|\t{2}BAKSpider - Backup File Spider:{1}".format(
            self.BR_MAGENTA, self.ORIG + Back.RESET, self.HEADER))
        print("{0}\_\(_)/_/{1}\t|\t-> Spider a website for leftover backup files.".format(self.BR_MAGENTA, self.ORIG))
        print("{0} _//\"\\\\_{1}\t|".format(self.BR_MAGENTA, self.ORIG))
        print("{0}  /   \\{1}\t\t|\thttps://github.com/mc-soft".format(self.BR_MAGENTA, self.ORIG))
        print("--------------------------------------------------------------")
        time.sleep(pause_time)
