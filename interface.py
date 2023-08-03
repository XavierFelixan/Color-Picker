import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import pyperclip

FONT = ("Times New Roman", 13, "normal")

class Interface:
    def __init__(self) -> None:
        # Creating the User Interface
        self.window = tkinter.Tk()
        self.window.config(padx=50, pady=50)
        self.window.title("Color Picker")

        # Creating a Canvas for the image and making it detects left-click
        self.canvas = tkinter.Canvas(self.window)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.pick_color)

        # Creating a Frame to ease the positioning of several elements
        self.frame = tkinter.Frame()
        self.frame.grid(row=0, column=1)
      
        self.rgb = tkinter.Entry(self.frame, font=FONT, relief="solid", width=15)
        self.rgb.grid(row=0, column=1, padx=10, pady=5)
        self.hex = tkinter.Entry(self.frame, font=FONT, relief="solid", width=15)
        self.hex.grid(row=1, column=1, padx=10, pady=5)

        self.color = tkinter.Button(self.frame, width=2, state='disabled')
        self.color.grid(row=0, column=0, padx=5, rowspan=2)
        self.default_bg = self.color['bg']
        self.copy_rgb = tkinter.Button(self.frame, text="📑", relief="groove", command=self.copying_rgb)
        self.copy_rgb.grid(row=0, column=2, pady=4)
        self.copy_hex = tkinter.Button(self.frame, text="📑", relief="groove", command=self.copying_hex)
        self.copy_hex.grid(row=1, column=2, pady=4)
        self.browse = tkinter.Button(self.frame, text="Browse", command=self.browse_file)
        self.browse.grid(row=0, column=3, padx=5, rowspan=2)
      
        self.window.mainloop()

    # Browse the file explorer to obtain and open the image file
    def browse_file(self):
        # Setting up the elements for new image
        self.color.config(bg=self.default_bg)
        self.rgb.delete(0, tkinter.END)
        self.hex.delete(0, tkinter.END)

        # Browse and prepare the image
        filename = filedialog.askopenfilename(initialdir='/', title="Select an Image", filetypes=(("png files","*.png"),("jpg files","*.jpg"),("jpeg files","*.jpeg")))
        image = Image.open(filename)
        ori_width, ori_height = image.size
        now_width, now_height = self.adjust_image(ori_width, ori_height)
        self.img = image.resize((now_width, now_height), Image.Resampling.LANCZOS)
        self.img_array = np.array(self.img)

        # Displaying the new image in the Canvas
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.canvas.config(width=now_width, height=now_height)
        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.img_tk)

    # Resize the image for better viewing
    def adjust_image(self, ori_width, ori_height):
        while ori_width > 900 or ori_height > 600:
            ori_width, ori_height = int(ori_width/1.1), int(ori_height/1.1)
        return (ori_width, ori_height)

    # Pick the Color
    def pick_color(self, cursor):
        # Setting up the elements for picking new color
        self.rgb.delete(0, tkinter.END)
        self.hex.delete(0, tkinter.END)

        # Get the RGB code of the color
        self.rgb_code = tuple(px for px in self.img_array[cursor.y][cursor.x][0:3])

        #Get the hex code of the color
        self.hex_code = '#%02x%02x%02x' % self.rgb_code

        # Displaying the color and its color codes
        self.color.config(bg=self.hex_code)
        self.rgb.insert(0, str(self.rgb_code))
        self.hex.insert(0, self.hex_code)

    # Copy the RGB code into the clipboard
    def copying_rgb(self):
        pyperclip.copy(str(self.rgb_code))

    # Copy the hex code into the clipboard
    def copying_hex(self):
        pyperclip.copy(self.hex_code)        
