import curses
from modules.components.Component import Component


class Text(Component):

    @staticmethod
    def get_component(text, size):
        title_size_x = 60
        middle_screen = int(size[1]/2)-int(title_size_x/2)-1
        text_window = curses.newwin(7,title_size_x,4,middle_screen)
        text_window.addstr(text)
        return text_window