import tkinter as tk


root = tk.Tk()
root.title("Main Window")
root.geometry("640x480")

sub = tk.Toplevel(root)
sub.transient(root) #Keeps sub window on top of root
sub.title('Sub Window')
sub.minsize(320, 240)
sub.maxsize(320, 240)

pos = []

def main_move(event):
    #When the main window moves, adjust the sub window to move with it
    if pos:
        sub.geometry("+{0}+{1}".format(pos[0], pos[1]))
        # Change pos[0] and pos[1] to defined values (eg 50) for fixed position from main

def sub_move(event):
    # Set the min values
    min_w = root.winfo_rootx()
    min_h = root.winfo_rooty()
    # Set the max values minus the buffer for window border
    max_w = root.winfo_rootx() + root.winfo_width() - 15
    max_h = root.winfo_rooty() + root.winfo_height() - 35

    # Conditional statements to keep sub window inside main
    if event.x < min_w:
        sub.geometry("+{0}+{1}".format(min_w, event.y))

    elif event.y < min_h:
        sub.geometry("+{0}+{1}".format(event.x, min_h))

    elif event.x + event.width > max_w:
        sub.geometry("+{0}+{1}".format(max_w - event.width, event.y))

    elif event.y + event.height > max_h:
        sub.geometry("+{0}+{1}".format(event.x, max_h - event.height))

    global pos
    # Set the current sub window position
    pos = [event.x, event.y]  

root.bind('<Configure>', main_move)
sub.bind('<Configure>', sub_move)


root.mainloop()