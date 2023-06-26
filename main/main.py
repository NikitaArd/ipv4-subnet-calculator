import sys

if __name__ == '__main__':
    if sys.argv[1] == 'ctk':
        import ctk_gui
    elif sys.argv[1] == 'flet':
        import flet_gui
    else:
        raise ValueError('Invalid GUI symbol')
