import curses


class Input:

    @staticmethod
    def get_component(input_label, area):
        curses.curs_set(2)
        curses.echo(True)
        username_input = curses.newwin(area['height'],area['width'],area['y'],area['x'])
        username_input.addstr(0, 0, input_label)
        username_input.refresh()
        username = username_input.getstr(0+1, 0, 20)
        curses.curs_set(0)
        curses.echo(False)
        return username
