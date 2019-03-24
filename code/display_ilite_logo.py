import tkinter as tk

# displays a picture fullscreen as determined by the "picture_name" variable

picture_name = "final.png"
picture_path = "../media/" + picture_name

# Creates the "window" object basically
root = tk.Tk()

# Make the tk fullscreen and the topmost window
root.attributes("-fullscreen", True)
root.wm_attributes("-topmost", True)

# Hide the mouse pointer
root.config(cursor='none')

# Allow for turning off the screen saver
# This happens only with a press of the ESCAPE key
# This will only happen if a keyboard is plugged in
root.bind("<Escape>", root.destroy)

# Setup the actual canvas to draw to
canvas = tk.Canvas(root)
canvas.pack(fill='both', expand=True)

# Grabbing the image and painting it to the canvas
img = tk.PhotoImage(file=picture_path)
canvas.create_image(0, 0, anchor='nw', image=img)

# Display the canvas to the screen
root.mainloop()
