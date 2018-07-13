import tkinter
from tkinter import filedialog
from tkinter import simpledialog


def open_file(filename, path=None, title=None):
    """
    Open choose file dialog

    :param filename - name of file
    :param path - path to file
    :param title - title of dialog
    :return: path to file
    """

    if title is None:
        title = "Select map file to open"

    if path is None:
        path = ""

    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        initialfile=filename,
        initialdir=path,
        title=title,
        filetypes=(("Robot map files", "*.map"),))

    root.destroy()
    return file_path


def save_file(filename):
    """
    Open save file dialog
    :param filename - name of file
    :return: path to file
    """

    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        initialfile=filename,
        title="Save map file",
        filetypes=(("Robot map files", "*.map"),))

    root.destroy()
    return file_path


def input_integer(val):
    """
    Open input integer dialog
    :param val - initial value
    :return: path to file
    """

    root = tkinter.Tk()
    root.withdraw()
    answer = simpledialog.askinteger("Input", "Enter temperature from interval [-10,10]",
                                     initialvalue=val,
                                     minvalue=-10,
                                     maxvalue=10)

    root.destroy()
    return answer
