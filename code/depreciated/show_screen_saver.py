import sys
import Tkinter as tk
# import pyscreenshot as sshot

# Parsing command line arguments
# The only one should be an double number of seconds to keep the screen on for
# The parsing isn't very safe but it gets the job done (it won't be called any
# other way anyways)


def get_delay():
    if len(sys.argv) > 1:
        return int(1000 * float(sys.argv[1]))
    else:
        return 3000


# Basically the second argument should be the image name
# or relative path from the python script
# AGAIN... parsing these arguments is unethically not safe
def get_img():
    out = ""

    if len(sys.argv) > 2:
        out = sys.argv[2]
    else:
        out = 'final.png'

    return '../' + out

# Method to turn off the screen saver


def on_escape(event=None):
    print("Escaped")
    root.destroy()

# -------------------------------------- #

# Take a screen shot and save it to a temp location
# screenshot = sshot.grab()
# screenshot.save('screenshot.png')


# Create the TK entity
root = tk.Tk()

# Make the tk fullscreen and the topmost window
root.attributes("-fullscreen", True)
root.wm_attributes("-topmost", True)

# Hide the mouse pointer
root.config(cursor='none')

# Allow for turning off the screen saver
root.bind("<Escape>", on_escape)

# Saftey for testing to turn off the screen saver after a given number of
# seconds This can be commented out later
# If the number is negative (probably just -1) then it will always display
if get_delay() > 0:
    root.after(get_delay(), root.destroy)

# Setup the actual canvas to draw to
canvas = tk.Canvas(root)
canvas.pack(fill='both', expand=True)

# Grabbing the image and painting it to the canvas
img = tk.PhotoImage(file=get_img())
# print( 'Got the ILITE img: ' + get_img() )
canvas.create_image(0, 0, anchor='nw', image=img)

# Display the canvas to the screen
root.mainloop()
