# This file contains the main function for the Catan Player project.

from board import CatanBoard

_greeting = r"""
 ________  ________  _________  ________  ________           ________  ___
|\   ____\|\   __  \|\___   ___\\   __  \|\   ___  \        |\   __  \|\  \
\ \  \___|\ \  \|\  \|___ \  \_\ \  \|\  \ \  \\ \  \       \ \  \|\  \ \  \
 \ \  \    \ \   __  \   \ \  \ \ \   __  \ \  \\ \  \       \ \   __  \ \  \
  \ \  \____\ \  \ \  \   \ \  \ \ \  \ \  \ \  \\ \  \       \ \  \ \  \ \  \
   \ \_______\ \__\ \__\   \ \__\ \ \__\ \__\ \__\\ \__\       \ \__\ \__\ \__\
    \|_______|\|__|\|__|    \|__|  \|__|\|__|\|__| \|__|        \|__|\|__|\|__|

"""


def main():
    print(_greeting)
    myboard = CatanBoard()
    myboard.play()


if __name__ == "__main__":
    main()
