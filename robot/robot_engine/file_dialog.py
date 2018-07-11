import tkinter
import tkinter.filedialog as tkFileDialog


def open_file(fName):
    """
    Open choose file dialog
    :return: path to file
    """

    root = tkinter.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename(initialfile=fName, filetypes=(("Robot map files", "*.map"),))

    root.destroy()
    return file_path


def save_file(fName):
    """
    Open save file dialog
    :return: path to file
    """

    root = tkinter.Tk()
    root.withdraw()
    file_path = tkFileDialog.asksaveasfilename(initialfile=fName, filetypes=(("Robot map files", "*.map"),))

    root.destroy()
    return file_path
