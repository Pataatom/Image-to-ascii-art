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
settings_frame = tk.Frame(root, bg="lightgray")
convert_button = tk.Button(settings_frame, text="Convert",
                               command=lambda: working_with_picture(str(file_path), file_name))
settings_label = tk.Label(settings_frame, text="Settings Area", font=("Arial", 12), bg="lightgray")
# ____ON_DROP____

file_name = ""
ascii_characters_by_surface_10 = " .:-=+*#%@"
ascii_characters_by_surface_65 = '`^"' + r",:;Il!i~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
ascii_characters_by_surface = ascii_characters_by_surface_10

# stupid reversing string
ascii_list = list(ascii_characters_by_surface)
ascii_list.reverse()
ascii_characters_by_surface = ""
for char in ascii_list:
    ascii_characters_by_surface += char
# stupid reversing string


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


def working_with_picture(pic, file_name):
    global image_dropped
    extension = os.path.splitext(pic)[-1].lower()
    if extension not in (".png", ".jpeg", ".jpg"):
        print("Bad file extension, need .jpg or .png")
        print(extension)
        exit()
    image = Image.open(pic)
    image = ImageOps.exif_transpose(image)  # Correct the orientation based on EXIF data

    # ____RESIZING_IMAGE_TO_BE_VIEWABLE____
    (width, height) = image.size
    if width > 1024:  # notepad max characters on a line
        aspect_ratio = width / height
        width = 1024
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
        print(another_step)
        for x in range(width):
            px = image.getpixel((x, y))
            line += pixel_to_ascii(px, extension)
        another_step += one_step
        ascii_art.append(line)
    progress.set(0)
    root.update_idletasks()  # Update the GUI after the conversion is done
    saving_ascii_art(ascii_art, file_name)  # Call the saving_ascii_art function to save the ASCII art
    toggle_settings(False)
    image_dropped = False


def saving_ascii_art(ascii_art, file_name):
    with open(f"{file_name}_ascii_image.txt", "w") as f:
        for line in ascii_art:
            f.write(line)
            f.write("\n")


def on_drop(event):
    global file_name, image_dropped, file_path
    if not image_dropped:
        image_dropped = True
        file_path = event.data.strip("{}")
        file_name = os.path.basename(file_path).split(".")[0]  # get only the name of the file and not the extension


        toggle_settings(True)
    else:
        file_path = event.data.strip("{}")
        file_name = os.path.basename(file_path).split(".")[0]  # get only the name of the file and not the extension
        #working_with_picture(str(file_path), file_name)


def toggle_settings(settings_visible = True):


    if not settings_visible:
        # Hide the settings
        settings_frame.pack_forget()
        convert_button.pack_forget()
        settings_label.pack_forget()
        root.geometry("250x150")  # Adjust the base window size
    else:
        # Show the settings
        convert_button.pack(side="top", fill="both", expand=False)
        settings_frame.pack(fill="both", expand=True)# fill="both", expand=True
        settings_label.pack(pady=10)
        root.geometry("250x300")  # Expand the window size to fit settings

    #settings_visible = not settings_visible



def main():

    root.title("Ascii_art")
    root.geometry("250x150")

    #main_frame = tk.Frame(root)
    #main_frame.pack(fill="both", expand=True)

    try:
        img_more = Image.open(r"more.png")
        img_more = ImageTk.PhotoImage(img_more)
        # img_settings = Image.open(r"settings.png")
        # img_settings = ImageTk.PhotoImage(img_settings)
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
    root.mainloop()


if __name__ == '__main__':
    main()