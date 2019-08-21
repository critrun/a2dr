
Let's you display colour images inside of python terminal. (Windows 10)

___________________________________________________________________________________________

Tested for Windows 10

Library needed: Pillow  

___________________________________________________________________________________________

Copy paste this into cmd to install library needed:

**python -m pip install --upgrade pip --user**

**pip install pillow --user**

___________________________________________________________________________________________
   
If you have any ideas upon further improvement contact me via discord.

Discord tag:  **critcore#8395**

___________________________________________________________________________________________ 

Feel free to edit the library, but if you’re giving your edit away anywhere make sure to 

credit  my discord account and give link to my original post of this library and send link 

to your edit  to my discord.     

**Do not redistribute my library and claim it’s your own.**

**Do not redistribute my library and not credit like instructed.**  

**Do not remove the startup screen in the library if you edit and give it away.**   

**Do not edit the startup screen in any way**  

**Do not redistribute my library without editing, instead link the post.**

___________________________________________________________________________________________    

A2DR contains 19 neat commands, ~450 lines of code and all this for free, for your pleasure.    

However free comes with the cost that I can’t guarantee it will work for you. 

But I’m very willing to help you when I have the time. Contact my discord for help.    

 

Below are instructions on how to use every command. So you can get into the epic world of  

A2DR, the simple to use library for displaying colour images in python terminal.  

___________________________________________________________________________________________                 

**pixel_size(size)**   

Changes the font size in terminal.    



Example:    

pixel_size(5)  

___________________________________________________________________________________________    

**get_terminal_size()**  

Returns the size of terminal in columns and rows.    



Example:    

w, h = get_terminal_size() 

___________________________________________________________________________________________    

**resolution(size)**  

Changes the font size in terminal and returns terminal size.    



Example:    

w, h = resolution(2)  

___________________________________________________________________________________________    

**try_res(size)**  

Displays a test image with given font size    



Example:    

try_res(10)  

___________________________________________________________________________________________    

**test_image()**  

Displays a test image and changes the font size to 2. Recommended 1080p or more.    



Example:    

test_image() 

___________________________________________________________________________________________           

**merge(bottom image, top image, colour)**  

Merges two images where the given colour is invisible on the top image.    



Example:    

merged_img = merge(img1, img2, “255255255”)  

___________________________________________________________________________________________    

**draw_legacy(image, image width)**  

Displays given image in terminal. Works faster for larger images.    



Example:    

draw_legacy(img, 1920)  

___________________________________________________________________________________________    

**draw(image, image width)**  

Displays given image in terminal. Doesn’t flicker. Super fast with small images. Image must  

be same resolution as get_terminal_size().    



Example:    

draw(img, 400)  

___________________________________________________________________________________________    

**img_convert(image path, width, height)**  

Returns an image workable by A2DR in the given resolution. Also displays a loading screen  

while converting.    



Example:    

img = img_convert(“Image.jpg”, 1280, 720)  

___________________________________________________________________________________________    

**recommended_res(fps)**  

Changes to and returns the recommended font size for the desired fps.    



Example:    

font_size = recommended_res(60)  

___________________________________________________________________________________________       

**res2pix(width, height)**  

Changes to and returns the recommended font size for the given resolution.    

Example:    



font_size = res2pix(720, 1280)  

___________________________________________________________________________________________    

**compress(image)** 

Compresses and turns an A2DR workable images into a much smaller utf-8 friendly string.    



Example:    

compressed_image = compress(img)  

___________________________________________________________________________________________    

**uncompress(compressed image)**  

Uncompresses a compressed utf-8 friendly image and makes it A2DR workable.    



Example    

img = uncompress(compressed_image)  

___________________________________________________________________________________________    

**resize(image, image width, new width, new height)**  

Resizes given image into the new width and height.    



Example:    

img = resize(img, 1280, 1920, 1080)  

___________________________________________________________________________________________    

**str2img(string)**  

Returns image and image width. The image resembles the string and you can only input  

numbers, small letters, space and percent sign.    



Example:    

img_of_text, w = str2img(“Hello World”)  

___________________________________________________________________________________________         

**swap_col(image, colour1, colour2)**  

Swaps colour1 with colour2 in image.    



Example:    

img = swap_col(img, 255255255, 000255000)  

___________________________________________________________________________________________    

**load(percent, title)**  

Returns an image of a windows 95 styled loading screen. Title can only contains the same  

set of characters as the str2img() can take.    



Example:    

img = load(40, “this is a loading screen”)  

___________________________________________________________________________________________    

**logo()**  

Returns an image of the A2DR logo. Great for quickly trying out different features within 

the  library.    



Example:    

logo_img = logo()  

___________________________________________________________________________________________    

**startup()**  

Displays the startup screen of A2DR.    



Example:    

startup()  

___________________________________________________________________________________________    

Here’s a handy tip:  If you want to resize an image to current font size so you can use 

the non legacy draw do  this:    



w, h = get_terminal_size()  

img = resize(img, img_width, w, h)  

draw(img, w)  

___________________________________________________________________________________________
