import time
import tkinter as tk

from tkinterdnd2 import TkinterDnD, DND_FILES
import os
from PIL import Image, ImageTk, ImageOps
from tkinter import ttk

root = TkinterDnD.Tk()
progress = tk.IntVar()
progress_bar = ttk.Progressbar(root, length=250, maximum=250, variable=progress)

# ____ON_DROP____
image_dropped = False
# ____ON_DROP____

def convert():
    global file_name, file_path, max_width
    max_width = max_ascii_width.get() or 1000
    max_width = int(max_width)
    working_with_picture(str(file_path), file_name)

# ____SETTINGS____
settings_frame = tk.Frame(root, bg="lightgray")
convert_button = tk.Button(settings_frame, text="Convert",
                               command=convert)
settings_label = tk.Label(settings_frame, text="settings", font=("Arial", 12), bg="lightgray", wraplength=250)
max_ascii_width = tk.StringVar(value="1000")   # max 1000 char on a line if using win11, 1024 if using win10 notepad
max_width_label = tk.Label(root, text="Max width:")
max_width = 0
# ____SETTINGS____

file_name = ""
ascii_characters_by_surface_10 = " .:-=+*#%@"
ascii_characters_by_surface_65 = '`^"' + r",:;Il!i~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
ascii_characters_by_surface = ascii_characters_by_surface_10

def color_inverter():  # if true, white viewer background is expected(e.g. windows notepad)
    global ascii_characters_by_surface, inverted_colors
    ascii_list = list(ascii_characters_by_surface)
    ascii_list.reverse()
    ascii_characters_by_surface = ""
    for char in ascii_list:
        ascii_characters_by_surface += char

color_inverter()  # run it once, so the default viewer background is white

def pixel_to_ascii(pixel, extension):
    if extension == ".png":
        if isinstance(pixel, int):  # Handle grayscale images where the pixel is an integer
            pixel_brightness = pixel
            max_brightness = 255
            brightness_weight = len(ascii_characters_by_surface) / max_brightness
            index = int(pixel_brightness * brightness_weight)
            index -= 1

        else:  # Extract color channels from the pixel tuple
            try:
                (R, G, B, A) = pixel
            except:
                (R, G, B) = pixel
                A = 1
            pixel_brightness = 0.299 * R + 0.587 * G + 0.114 * B
            max_brightness = 0.299 * 255 + 0.587 * 255 + 0.114 * 255
            brightness_weight = len(ascii_characters_by_surface) / max_brightness
            index = int(pixel_brightness * brightness_weight)
            if index == 0 and A > 0:  # is it black???
                pass
            else:
                index -= 1
        return ascii_characters_by_surface[index]
    elif extension in (".jpg", ".jpeg"):
        if isinstance(pixel, int):  # Handle grayscale images where the pixel is an integer
            pixel_brightness = pixel
            max_brightness = 255
            brightness_weight = len(ascii_characters_by_surface) / max_brightness
            index = int(pixel_brightness * brightness_weight)
            index -= 1

        else:  # Extract color channels from the pixel tuple
            (R, G, B) = pixel
            pixel_brightness = 0.299 * R + 0.587 * G + 0.114 * B
            max_brightness = 0.299 * 255 + 0.587 * 255 + 0.114 * 255
            brightness_weight = len(ascii_characters_by_surface) / max_brightness
            index = int(pixel_brightness * brightness_weight)
            if index == 0:  # is it black???
                pass
            else:
                index -= 1
        return ascii_characters_by_surface[index]
        # sadly, with this logic, the true white (255, 255, 255, 255) will never be " " (blank)
        # I know there is some clear solution to this, but I am just too dumb
    else:
        print("I don't support this extension, sry")
        time.sleep(1)

def working_with_picture(pic, pic_name):
    global image_dropped, max_width
    extension = os.path.splitext(pic)[-1].lower()
    if extension not in (".png", ".jpeg", ".jpg"):
        print("Bad file extension, need .jpg or .png")
        print(extension)
        exit()
    image = Image.open(pic)
    image = ImageOps.exif_transpose(image)  # Correct the orientation based on EXIF data

    # ____RESIZING_IMAGE_TO_BE_VIEWABLE____
    (width, height) = image.size
    if width > max_width:  # max 1000 char on a line if using win11, 1024 if using win10
        aspect_ratio = width / height
        width = max_width
        height = int(width/aspect_ratio)
    new_height = int(height*0.3676470588235294)  # cos character has greater height than width
    image = image.resize((width, new_height))
    # ____RESIZING_IMAGE_TO_BE_VIEWABLE____

    ascii_art = []
    one_step = 250 / new_height
    another_step = one_step
    for y in range(new_height):
        progress.set(another_step)
        root.update_idletasks()  # Update the GUI
        line = ""
        #print(another_step)
        #time.sleep(0.001)
        for x in range(width):
            px = image.getpixel((x, y))
            line += pixel_to_ascii(px, extension)
        another_step += one_step
        ascii_art.append(line)
    progress.set(0)
    root.update_idletasks()  # Update the GUI after the conversion is done
    saving_ascii_art(ascii_art, pic_name)  # Call the saving_ascii_art function to save the ASCII art
    toggle_settings(False)
    image_dropped = False

def saving_ascii_art(ascii_art, pic_name):
    with open(f"{pic_name}_ascii_image.txt", "w") as f:
        for line in ascii_art:
            f.write(line)
            f.write("\n")

def on_drop(event):
    global file_name, image_dropped, file_path, settings_label

    file_path = event.data.strip("{}")
    file_name = os.path.basename(file_path).split(".")[0]  # get only the name of the file and not the extension
    shortened_file_name = ""
    for char in file_name:
        if len(shortened_file_name) <= 15:
            shortened_file_name += char
    settings_label.config(text=shortened_file_name)

    if not image_dropped:
        image_dropped = True
        toggle_settings()

    root.update_idletasks()

def toggle_settings(settings_visible = True):
    global settings_label, inverted_color_checkbox, width_entry

    if not settings_visible:
        # Hide the settings
        settings_frame.pack_forget()
        convert_button.pack_forget()
        settings_label.pack_forget()
        inverted_color_checkbox.pack_forget()
        max_width_label.pack_forget()
        width_entry.pack_forget()
        root.geometry("250x150")  # Adjust the base window size
    else:
        # Show the settings
        convert_button.pack(side="top", fill="both", expand=False)
        settings_frame.pack(fill="both", expand=True)# fill="both", expand=True
        settings_label.pack(pady=10)
        inverted_color_checkbox.pack()
        max_width_label.pack()
        width_entry.pack()
        root.geometry("250x304")  # Expand the window size to fit settings
    root.update_idletasks()  # Update the GUI after the conversion is done


    #settings_visible = not settings_visible

def main():
    global inverted_color_checkbox, width_entry

    root.title("Ascii_art")
    root.geometry("250x150")

    #main_frame = tk.Frame(root)
    #main_frame.pack(fill="both", expand=True)

    try:
        img_more = Image.open(r"more.png")
        img_more = ImageTk.PhotoImage(img_more)
    except:
        img_more = None
        # img_settings = None

    label = tk.Label(root, text="↓ Drag and drop images here ↓")
    label.pack(padx=10, pady=10)

    img_label = tk.Label(root, image=img_more)
    img_label.pack(padx=10, pady=10)

    progress_bar.pack()

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    inverted_color_checkbox = tk.Checkbutton(settings_frame, text='Inverted colors', command=color_inverter,
                                             background="lightgray")
    width_entry = tk.Entry(root, textvariable=max_ascii_width)
    root.mainloop()


if __name__ == '__main__':
    main()