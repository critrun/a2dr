#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ctypes
import os
import msvcrt
import subprocess
from ctypes import wintypes
import random
from PIL import Image
import time

###################################
###############A2DR################
##Anton's 2 Dimensional Rendering##
###################################
#This is a library made by critcore
#reddit username: bobafex (because reddit won't let me change name to critcore, oof)
#made with a lot of forum surfing.
#to see the people who made this library possible jsut scroll through the code
#and look at the comments.
#discord: critcore#8395
###################################

#incoming code made by Marfisa and light editing by me
def pixel_size(pix):
    "Changes the pixel size."

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = pix #default: 11
    font.dwFontSize.Y = pix #default: 18
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = "Lucida Console"

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
            handle, ctypes.c_long(False), ctypes.pointer(font))

    #incoming code by Eryk Sun

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    SW_MAXIMIZE = 3

    kernel32.GetConsoleWindow.restype = wintypes.HWND
    kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
    kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
    user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

    def maximize_console(lines=None):
        fd = os.open('CONOUT$', os.O_RDWR)
        try:
            hCon = msvcrt.get_osfhandle(fd)
            max_size = kernel32.GetLargestConsoleWindowSize(hCon)
            if max_size.X == 0 and max_size.Y == 0:
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            os.close(fd)
        cols = max_size.X
        hWnd = kernel32.GetConsoleWindow()
        if cols and hWnd:
            if lines is None:
                lines = max_size.Y
            else:
                lines = max(min(lines, 9999), max_size.Y)
            subprocess.check_call('mode.com con cols={} lines={}'.format(
                                    cols, lines))
            user32.ShowWindow(hWnd, SW_MAXIMIZE)
    maximize_console()

#this enables vt100 somehow
os.system('')

#incoming code made by Indian Pythonista and light editing by me
def not_to_be_used_externally(r, g, b):
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
def convert(r, g, b):
    return "\x1b[48;5;"+str(not_to_be_used_externally(r, g, b))+"m  \x1b[0m"

#incoming code made by me
def mod(t1, t2):
    t=t1/t2
    return round((t-round(t-0.499))*t2)

def hi2lo(colour):
    r=int(colour[0:3])
    g=int(colour[3:6])
    b=int(colour[6:9])
    return str(not_to_be_used_externally(r, g, b)+1000)[1:]

def lo2hi(code):
    code=int(code)
    #return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
    #return (code-16)/36*255/5
    rm = mod((code-16), 36)
    gm = mod((rm), 6)

    g=round(rm/6-0.499)
    b=gm
    r=(code-16-g*6-b)/36

    r=round(r*255/5)
    g=round(g*255/5)
    b=round(b*255/5)
    return str(r+1000)[1:]+str(g+1000)[1:]+str(b+1000)[1:]

def clear():
    "The most inefficient way to clear the screen."
    os.system('cls')

#incoming code made by granitosaurus and light editing by me
def get_terminal_size(fallback=(80, 24)):
    "Returns resolution of interpreter."
    for i in range(0,3):
        try:
            columns, rows = os.get_terminal_size(i)
        except OSError:
            continue
        break
    else:  # set default if the loop completes which means all failed
        columns, rows = fallback
    return columns/2, rows-4

#incoming code made by me, critcore :)
def resolution(pix_size):
    "Changes pixel size and returns new resolution."
    pixel_size(pix_size)
    w, h = get_terminal_size()
    return int(w), int(h)

def try_res(pix_size):
    "Displays a noisy test image."
    clear()
    w, h=resolution(pix_size)
    x2=0
    x3=0
    image=""
    while(x3<h):
        while(x2<w):
            image+=convert(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x2+=1
        print(image)
        image=""
        x2=0
        x3+=1
    print(image)
    
def test_image():
    "Displays a test image."
    resolution(2)
    r=0
    g=0
    b=0
    second=0
    image=""
    clear()
    while(b<256):
        while(g<256):
            while(r<256):
                image+=convert(r, g, b)
                r+=1
            r=0
            second=second+1
            g+=1
            if(second==3):
                print(image)
                image=""
                second=0
        g=0
        b+=51

def merge(img_bottom, img_top, colour):
    "Merges two images where the colour is transparent."
    img_bottom=img_bottom[4:]
    img_top=img_top[4:]
    colour=str(colour)
    if(len(colour)!=9):
        return "Error"
    int(colour)
    img1=img_bottom
    img2=img_top
    x=0
    final=""
    while(x<len(img_top)):
        if(img2[x:x+9]==colour):
            final=final+img1[x:x+9]
        else:
            final=final+img2[x:x+9]
        x+=9
    return final

def clr(rows):
    "Best way to clear the screen."
    print("\033[F"*(rows+2))

def draw(img):
    "Draws img on screen."
    width=int(img[0:4])
    img=img[4:]
    w, h = get_terminal_size()
    he=len(img)/9/width
    we=round((w-width)/2)
    x=0
    img=img.replace("i", "0")
    temp=round((h-he)/2)
    #clear()
    clr(h)
    print("\n"*temp)
    x=0
    x1=0
    line="  "*we
    temp=len(img)
    while(x<temp):
        while(x1<width):
            try:
                line+=convert(int(img[x:x+3]), int(img[x+3:x+6]), int(img[x+6:x+9]))
                x+=9
                x1+=1
            except:
                x+=9
                x1+=1
        line+="\n"+"  "*we
        x1=0
    print(line)

def img_convert(img, width, height):
    "Returns resized image from file path"
    w=width
    h=height
    img = Image.open(img)
    img = img.resize((w, h), Image.ANTIALIAS)
    img=img.convert("RGB")
    y=0
    if(width>9999):
        print("error")
        print("picture size to big in img_convert()")
    else:
        if(len(str(w))==1):
            out="000"+str(width)
        else:
            if(len(str(w))==2):
                out="00"+str(width)
            else:
                if(len(str(w))==3):
                    out="0"+str(width)
                else:
                    out=str(width)
    while(y<h):
        x=0
        while(x<w):
            r, g, b = img.getpixel((x, y))
            r=str(int(r)+1000)[1:]
            g=str(int(g)+1000)[1:]
            b=str(int(b)+1000)[1:]
            out+=str(r)+str(g)+str(b)
            x+=1
        y+=1
    return out

def recommended_res(fps):
    "Returns and sets the recommended pixel size for the given fps."
    ft=0
    res=50
    while(ft<1/fps):
        w, h = resolution(res)
        line=""
        x=0
        clear()
        while(x<w):
            line=line+convert(000, 000, 000)
            x+=1
        start=time.time()
        x=0
        while(x<h):
            print(line)
            x+=1
        ft=time.time()-start
        res=res-1
    resolution(res+1)
    return res+1

def res2pix(width, height):
    "Changes and returns the pixel size for the given resolution."
    res=1
    pixel_size(res)
    x, y=get_terminal_size()
    while(width<=x and height<=y):
        res+=1
        pixel_size(res)
        x, y=get_terminal_size()
    pixel_size(res-1)
    return res-1
            
def compress(img):
    "Compress an image for a2dr."
    width=img[0:4]
    img=img[4:]
    x=0
    recent=img[0:9]
    times=0
    final=""
    book="""AIbwE/O1064()P2[].KR3–5q"%GN9jH7BMXLD;+':z“”€$¢−_QVY!#&*<=>?@Z^`{|}~•…Â£ï»¿∩╗┐§×ΚαλημέρκόσεüñРуский®"""
    while(x<len(img)+9*18):
        if(img[x:x+9]==recent):
            times+=1
        else:
            final+=str(times+1000)[1:]+hi2lo(recent) #here
            times=1
        if(times==999):
            final+=str(times+1000)[1:]+hi2lo(recent) #here
            recent=""
            times=0
        recent=img[x:x+9]
        x+=9
    x=0
    out=""
    final=width+final
    while(x<len(final)):
        out+=book[int(final[x:x+2]):int(final[x:x+2])+1]
        x+=2
    return out

def uncompress(img):
    "Uncompress an image for a2dr."
    temp=""
    x=0
    book="""AIbwE/O1064()P2[].KR3–5q"%GN9jH7BMXLD;+':z“”€$¢−_QVY!#&*<=>?@Z^`{|}~•…Â£ï»¿∩╗┐§×ΚαλημέρκόσεüñРуский®"""
    while(x<len(img)):
        temp+=str(book.index(img[x:x+1])+100)[1:]
        x+=1
    img=temp[4:]
    width=temp[0:4]
    x=0
    final=""
    while(x<len(img)):
        times=int(img[x:x+3])
        x2=0
        while(x2<times):
            final+=lo2hi(img[x+3:x+6]) #12 instead of 6
            x2+=1
        x+=6 #12 here
    return width+final

def resize(img, w, h):
    "Resizes the image to given size."
    img_w=int(img[0:4])
    img=img[4:]
    w=int(w)
    h=int(h)
    img_h=len(img)/9/img_w
    hr=img_h/h
    wr=img_w/w
    out=""
    x=0
    y=0
    while(y<h):
        while(x<w):
            out+=img[round(x*wr-0.5)*9+round(y*hr-0.5)*9*img_w:round(x*wr-0.5)*9+round(y*hr-0.5)*9*img_w+9]
            x+=1
        x=0
        y+=1
    return str(w+10000)[1:]+out

def swap_col(img, colour1, colour2):
    "Takes image and changes colour 1 to colour 2."
    width=img[0:4]
    img=img[4:]
    c1=str(colour1)
    c2=str(colour2)
    x=0
    out=""
    while(x<len(img)):
        if(img[x:x+9]==c1):
            out+=c2
        else:
            out+=img[x:x+9]
        x+=9
    return width+out

def logo():
    "Returns logo image."
    return uncompress("""IVA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–:A(:A(:A(:A(:A(:A–:A(:A(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA(EA–EA(EA(EA(EA–EA7EA(EA(EA(EA(EA(EA(/A–/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/AH…A4…A4…A(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA–XA(XA(XA–XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(XA–:A(:A–:A7:A(:A(:A(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA–EA(EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA(EA(EA–EA7EA(EA(EA–EA(EA–EA–EA(/A–/A(/A(/A(/A(/A(/A(/A–/A–/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A7/A(/A(/A(/A(/A(/A(/A(/A(/A3…A4…A4…A(XA(XA–XA(XA7XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA–XA–XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(:A(:A(:A–:A(:A(:A(:A(:A–:A–EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA–EA(EA(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/AH…A4…A–XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA–:A(:A(:A–:A(:A(:A(:A(:A(:A–EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA4йA(σA(σA4йA(EA–EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A–/A(/A4…A4…A(XA(XA(XA–XA(XA7XA(XA–XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(:A(:A(:A(:A(:A(:A–:A(:A(:A–:A(EA–EA(EA(EA–EA(EA–EA(EA(EA(EA4йA–σA4йA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(/A7/A(/A(/A7/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A–/A(/A(/A–/A(/A–/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA–XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA–:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(:A(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA4йA(σA(σA4йA(EA–EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA–/A(/A(/A(/A(/A–/A(/A(/A–/A–/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A7/A–/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A–/A(/A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A–:A(EA–EA–EA(EA(EA(EA(EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA–EA(/A(EA(/A(/A(/A(/A–/A(/A(/A–/A(/A(/A(/A(/A(/A7/A(/A(/A–/A(/A(/A(/A(/A(/A(/A–/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A–/A(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A–:A–:A(:A(:A–:A–:A(EA(EA(EA(EA(EA–EA(EA(EA(EA4йA–σA4йA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–XA(XA–XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA7XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A–:A(:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA(EA(EA(EA–EA(EA4йA(σA(σA4йA(EA(EA(EA–EA–EA(EA(EA(EA–EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(/A–/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A7/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA–XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA–EA(EA(EA(EA(EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA(EA–EA–EA(EA(EA–/A(/A–/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A–/A(/A(/A–/A–/A(/A(/A(/A(/A(/A–/A(/A(/A–/A(/A(/A(/A(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA–XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–:A(:A(:A(:A(:A(:A(:A–:A(:A–EA(EA(EA(EA(EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(/A–/A(/A(/A(/A–/A(/A–/A(/A(/A–/A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(EA–EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A–/A(/A(/A–/A(/A(/A(XA(XA(XA7XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(:A(:A(:A(:A–:A(:A–:A(:A–EA(EA(EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA–EA(EA(EA(EA(EA–EA7EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A–/A–/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A–/A–/A(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(:A(λA(λA–λA–λA(λA(λA(λA(λAzλA(λA(λA(:A(XA–XA–XA(XA–XA–XA(XA(:A(:A(:A(:A(:A7:A(:A(:A(:A(EA(EA(EA(EA(EA4йA(σA(σA4йA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(/A(−A(ηA(σA(σA)7A)7A57A)7A)7A(σA(σA(−A(−A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A–/A(/A–/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(XA7XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(λI^7A)7A(:A(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(:A(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(:A4йA(σA(σA4йA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA–EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(zA(−A(σA)7IB7A)7A(σA(−A(/A(/A(/A(/A(/A–/A–/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A–/A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA)%A)7A)7A!7Aï7A)7A)7A)7A(:A(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(:A(:A(:A–:A(:A(:A–:A(:A–:A(EA(EA(:A4йA(σA(σA4йA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(−A(σA)7AB7A)7A)7A)7Aλ7A57AB7A(σA(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(XA(XA(XA(XA(XA–XA–XA–XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(:A)7A)7A)7IB7A)7A)7A(ηA(XA(XA–XA(XA(XA(XA–XA(XA–XA(XA(:A(:A(:A(:A–:A(:A(:A–:A(EA(EA(:A4йA–σA4йA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(σAB7A57I!7A)7A)7A)7A)7A(−A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A–/A(/A(/A(/A(/A(/A(/A–/A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(λA)7A)7I“7A)7A)7A)7A(:A(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(:A–:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A4йA(σA(σA4йA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA–EA(EA(EA(EA(EA(σA)7A)7bb7A)7A)7A)7A(−A(/A(/A–/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA)%A)7A)7I!7A)7A)7A(:A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A7:A(:A(:A(:A4йA(σA(σA4йA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(σA)7A)7b)7A)7A)7A)7A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A)7Iï7A)7A)7A(ηA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–:A(XA(:A(:A(:A–:A(:A(:A(:A(:A4йA(σA(σA4йA(:A–EA(EA(EA(EA–EA(EA–EA(EA(EA(EA–EA(EA–EA(EA(EA(EA(EA(σA)7A)7b57A)7A)7A(σA(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(XA(XA(XA7XA(XA(XA(XA–XA–XA(XA–XA(XA–XA(XA–XA(XA(XA(XA(XA(λA)7A)7I^7A)7A)7A)%A(XA(XA–XA(XA–XA(XA(XA7XA(XA–XA(XA–:A(:A7:A(:A(:A(:A4йA(σA(σA4йA(:A(EA(EA(EA(EA(EA(EA–EA–EA(EA(EA(EA(EA(EA–EA–EA(EA(EA(EA(σA)7A)7b57A57A)7A((A(/A(/A(/A(/A(/A–/A(/A–/A(/A(/A(/A(/A(/A–/A(/A(/A–/A–XA(XA–XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA)%A)7A)7Aï7A)7Añ7A)7A)7A(:A(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A(:A(:A(:A–:A(:A4йA(σA(σA4йA(:A(EA(EA(EA(EA(EA(EA–EA(EA–EA(EA(EA(EA(EA(EA7EA(EA(EA(EA(σA)7A)7AB7A)7A)7A)7A)7A)7A)7A57I57A)7A)7A(−A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A–/A(/A(/A(/A(/A(/A(/A(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(╗A57Iλ7A)7A)7A(ηA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–:A(:A(:A(:A(:A(:A4йA(σA(σA4йA(:A(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(σA)7A)7A)7A)7Ib7A)7Ib7A)7A)7A(σA(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA7XA–XA(XA–XA–XA(XA(XA(λA)7A)7A^7A)7A)7A)%A)7Aλ7A)7A)7A)%A(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(:A(:A(:A(:A(:A(:A4йA(σA(σA4йA(:A–EA(EA(EA–EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(σA)7A)7AB7A)7A(σA(−A(−A(−A(−A(−A(σI57A)7A)7A)7A(/A(/A(/A(/A(/A–/A(/A(/A(/A–/A(/A–/A–/A(/A–/A(/A(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA)%A)7A)7A^7A)7A)7A(λA)%A)7A)7Aï7A)7A)7A(:A(XA(XA(XA–XA(XA(XA(XA(XA(XA7XA(XA(XA(XA(XA7:A(:A(:A(:A4йA(σA(σA4йA(:A(EA–EA(EA(EA(EA(EA(EA(EA–EA(EA–EA(EA(EA–EA–EA(EA(EA(σA)7A)7A)7A(σA(−A(EA(EA(EA(EA(EA(EA(EA(EA(−A)7A)7A)7Aλ7A)7A)7A)7A(/A(/A(/A(/A(/A(/A–/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(╗A)7A)7Aï7A)7A)7A(λA(σA)7A)7Aï7A)7A)7A(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(:A(:A(XA(:A(:A(:A4йA(σA(σA4йA(:A(:A(:A(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(σA)7A(σA(:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA4йA(−A)7A)7Ib7A)7A(−A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7Aλ7A)7A(:A(λA)7A)7Aï7A)7A)7A)%A(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA–XA(XA(:A(XA(:A(:A(:A4йA–σA4йA(:A(:A(:A(EA(EA(EA–EA(EA(EA(EA(EA–EA(EA–EA–EA(EA(EA(EA(EA(σA(ηA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(/A)7I57A(−A(/A(/A(/A(/A(/A(/A–/A(/A(/A–/A–/A(/A(/A(/A(/A(/A(/A(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA)7A)7A)7A^7A)7A)7A)%A(XA(╗A)7A)7Añ7A)7A(:A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA–:A(:A(:A4йA(σA(σA4йA(:A(:A–:A(EA–EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA)7A)7A)7Añ7A)7A(−A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A7/A(/A(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(╗A)7A)7Aï7A)7A)7A(ηA(XA(:A)7A)7A)7Aï7A)7A)7A(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(:A(:A(:A4йA(σA(σA4йA(:A(:A(:A–:A(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA7EA–EA(EA(EA(EA(EA(EA(EA7EA(EA–EA–EA(EA(EA(EA(EA)7A)7A)7Añ7A)7A(/A(/A(/A(/A7/A(/A(/A(/A(/A–/A(/A(/A(/A–/A(/A(/A(/A(XA(XA(XA–XA–XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7Aï7A)7A)7A(λA(XA(XA)%A)7A)7Aï7A)7A)7A)%A(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(:A4йA(σA(σA4йA(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA–EA(EA–EA–EA–EA(EA–EA(EA(EA(EA(EA(−A)7A)7Aλ7A)7A)7A)7A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA)7A)7A)7A^7A)7A)7A)7A(:A(XA(XA(λA)7A)7Añ7A)7A(:A(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(:A4йA–σA4йA(:A(:A(:A(:A(:A(:A(:A(EA7EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(σA)7A)7Aλ7A)7A)7A(σA(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A–/A(/A(/A(/A(/A(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(╗A)7A)7Aï7A)7A)7A)%A(XA(XA(XA(λA)7A)7Aλ7A)7A)7A(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(:A4йA(σA(σA4йA(:A(:A7:A–:A(:A(EA–EA(EA(EA–EA(EA(EA–EA(EA(EA(EA–EA(EA–EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(−A)7A)7Añ7A)7A)7A(−A(EA(/A–/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A7/A(/A–/A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(σA)7A)7Aï7A)7A)7A(λA(XA(XA(XA(:A)7A)7A)7Aï7A)7A)7A(σA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A4йA(σA(σA4йA(:A(:A(:A(:A(:A(:A–:A(:A(EA(EA(EA–EA(EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(−A)7A57Aλ7A)7A)7A)7A(zA(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A–/A–/A(/A(/A(XA(XA(XA–XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA)7A)7A)7Aï7A)7A)7A(λA(XA(XA(XA(XA)%A)7A)7Añ7A)7A(:A(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(:A4йA(σA(σA4йA(:A–:A–:A(:A(:A(:A–:A(EA–EA(EA(EA(EA(EA(EA7EA7EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(−A)7A)7A)7Añ7A)7A)7A(σA(EA(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A–/A(MA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(╗A)7A)7Aï7A)7A)7A)7A(:A(XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A(λA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A4йA(σA(σA4йA(:A–:A(:A(:A(:A(:A(:A–:A(:A(EA–EA(EA(EA(EA–EA–EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(−A)7A)7A)7Añ7A)7A)7A)7A(zA(EA(/A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(/A–MA(MA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(σA)7A)7Aï7A)7A)7A)%A(XA(XA(XA(XA(XA(╗A)7A)7Aλ7A)7A)7A(σA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(:A4йA(σA(σA4йA(:A(:A(:A(:A–:A(:A(:A(:A(:A(:A(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(ηA57A)7Ib7A)7A)7A(−A(EA(/A–EA(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A–/A(/A(/A(/A(MA(MA–MA–XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA)7A)7A)7Aï7A)7A)7A(λA(XA(XA(XA(XA(XA(:A)7A)7A)7Añ7A)7A(:A(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A4йA–σA4йA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA–EA(EA–EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(:A(σA)7A)7A)7Ib7A)7A)7A(σA(EA(EA(EA(EA(EA(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(MA(MA(MA(MA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A(╗A(XA(XA(XA(XA(XA(XA)%A)7A)7Aλ7A)7A)7A(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(:A4йA(σA(σA4йA(:A(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA4йA(:A)7A)7A)7Ib7A)7A)7A)7A(σA(EA(EA(EA(EA(EA(EA(EA(/A(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(/A–/A–/A(/A(…A–MA(MA(MA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(σA)7A)7Aï7A)7A)7A)7A(:A(XA(XA(XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A(σA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(:A4йA(σA(σA4йA(:A(XA(XA(:A–:A(:A(:A(:A–:A–:A(:A(:A(EA(EA7EA(EA(EA(EA(EA(EA(EA(EA(EA4йA(−A)7A)7A)7Ib7A)7A57A(−A(EA(EA(EA(EA(EA(EA(EA(EA(EA(/A(/A(/A–/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(…A(…A–MA–MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(╗A)7A)7A)7Aï7A)7A)7A)%A(XA(XA(XA(XA(XA(XA(XA(╗A)7A)7Aλ7A)7A)7A)7A(:A(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(:A4йA(σA(σA4йA(:A(XA(XA–XA(:A(:A(:A(:A(:A(:A(:A(:A(:A–:A(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(ηA57A)7Añ7A)7A)7A)7A)7A(−A(EA(EA(EA(EA(EA(EA(EA–EA–EA(/A(/A–/A(/A(/A(/A(/A(/A(/A–/A–/A(/A(/A(…A(…A–…A(MA(MA(MA(XA–XA–XA(XA–XA(XA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)%A(λA(λA(λA(λA(λA(λA(λA(λA)7Ib7A)7A)7A(λA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA–XA(:A4йA–σA4йA(:A–XA(XA–XA(:A(:A(:A(:A(:A–:A(:A(:A(:A–EA(EA(EA(EA(EA(EA(EA(EA(EA4йA(ηA)7A)7A)7Añ7A)7A57A(σA(:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(/A(/A(/A(/A–/A(/A(/A(/A(/A–/A(/A(/A(/A(/A(…A(…A(…A(…A(MA(MA(MA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA)%A)7A)7wb7A)7A)7A(σA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA–XA–XA(XA4йA–σA4йA(:A(XA–XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(σA)7A)7Añ7A)7A)7A)7A)7A(−A(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A(…A(…A–…A(…A–MA–MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(╗A)7I57A)7Aλ7I)7A)7A)7A)7A(:A(XA(XA(XA(XA–XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(ηA(σA4йA(:A(XA(XA(XA(XA(XA(XA(:A(:A–:A(:A(:A(:A(:A(:A(:A(:A(:A(EA–EA(EA(EA4йA(ηA)7A)7Añ7A)7A57A(σA(:A(EA(EA(EA–EA(EA(EA(EA(EA(EA–EA(EA–EA–EA(/A(/A(/A(/A(/A(/A(/A7/A(/A–/A(/A(…A(…A(…A(…A(…A(…A(…A(MA(MA(MA(MA(XA(XA(XA(XA(XA(XA(MA(λA)7A)7w57A)7A)7A(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA–σA4йA(:A(XA(XA–XA(XA(XA(:A(:A(:A–:A(:A(:A–:A(:A(:A(:A(:A(EA(EA(:A4йA(−A)7A)7Añ7A)7A)7A)7A(−A(EA(EA(EA(EA(EA–EA(EA(EA(EA7EA–EA(EA(EA(EA(EA–EA(/A(/A(/A(/A(/A(/A(/A(/A(/A7/A(…A(…A(…A(…A–…A(…A(MA(MA(MA(MA(XA(XA(XA(XA(XA(XA(XA)%A)7A)7w57A)7A)7A(σA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(σA(σA4йA(:A(XA(XA–XA(XA(XA–XA(:A–:A(:A(:A(:A(:A(:A–:A(:A(:A(:A4йA(:A)7A57Aλ7A)7A)7A)%A(:A(EA(EA(EA(EA(EA(EA(EA(EA–EA–EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(/A(/A(/A(/A(/A(/A(/A(/A(/A(/A–/A–…A(…A(…A–…A(…A(…A–MA(MA(MA–XA(XA(XA(MA(╗A)7w“7A)7A)7A)7A(:A(XA(XA–XA–XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(ηA(σA(XA(:A–XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A(:A–:A(:A(:A(:A(:A(:A4йA(σA)7A)7Aλ7A)7A)7A(σA(:A(EA(EA(EA–EA(EA7EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA–EA–EA(/A(/A(/A(/A(/A(/A–/A(/A(/A(/A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(MA–MA(XA(XA(XA(MA(λA)7A)7w“7A)7A)7A(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–σA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–:A(:A(:A(:A(:A–:A(:A(:A4йA(:A)7A)7Aλ7A)7A)7A(σA4йA4йA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA–/A(/A(/A(/A(/A–/A(/A–…A(…A(…A(…A(…A–…A(…A–…A–MA(MA(XA(XA(XA)%A)7A)7w“7A)7A)7A(σA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(ηA(σA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A–:A–:A–:A(:A(:A4йA(σA)7A)7Aλ7A)7A)7A(ηA(:A(¢A(:A(¢A(¢A(¢A(¢A(¢A(−A–−A(−A(−A(−A(−A(−A(zA(EA–EA(EA(EA(EA(EA–EA(EA(EA(/A(/A–/A(/A(/A(/A(/A(/A(…A(…A(…A(…A(…A(…A–…A(…A–…A(MA(MA(MA(XA(MA(╗A)7I57I57A)7A)7Ib7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(XA–XA7XA(XA(XA(XA(XA(ηA(σA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(:A(XA(:A(:A(:A(:A(:A(:A(XA(:A)7A)7A)7b!7A)7A)7A(σA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(/A(/A(/A(/A(/A(/A(/A(/A–…A(…A(…A(…A–…A(…A(…A(…A(…A(MA(MA(MA(XA(MA(λA)7A)7w^7A)7A)7A(╗A(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA–ηA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(:A(:A(:A–:A(:A4йA(:A)7A)7b^7A)7A)7A(σA(EA(EA(EA(EA–EA(EA(EA(EA–EA(EA(EA(EA(/A(/A(/A(/A–/A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(MA(MA(MA(XA)%A)7A)7Ib7A)7A(λA(╗A(╗A(╗A–╗A(╗A–╗A–╗A(╗A(╗A(σA)7A)7Añ7A)7A)7A(σA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA7XA(XA(:A–:A(:A4йA(ηA)7A)7b^7A)7A)7A(σA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA–EA(/A(/A(/A(/A(/A(/A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(MA(╗A)7A)7Añ7A)7A)7A)%A(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(╗AB7Aλ7A)7A)7A)7A(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A(XA(σA)7A)7b^7A)7A)7A(σA(EA(EA–EA(EA–EA(EA(EA(EA–EA(EA(EA(/A(EA(/A(/A–/A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(MA(λA)7A)7Añ7A)7A)7A(λA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA)7A)7A)7Añ7A)7A)7A(╗A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(:A(:A(:A(XA(σA)7A)7b^7A)7A)7A(σA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(/A(/A(/A(/A(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A)%A)7A)7Añ7A)7A)7A(╗A(MA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(σA)7A)7Añ7A)7A)7A(λA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(:A(:A(:A(σA)7A)7b^7A)7A)7A(σA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(/A(/A(/A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(╗A)7A)7Añ7A)7A)7A)7A(╗A(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(λA)7A)7Añ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(XA(:A)%A)7A)7b^7A)7A)7A(σA(EA(EA(EA(EA–EA(EA–EA(EA–EA(EA(EA(EA(EA(EA(EA(/A(/A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(MA(λA)7A)7Añ7A)7A)7A)%A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(╗A)7A)7Ib7A)7A)7A(╗A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA–XA–XA(XA–XA(XA–XA(XA–XA(XA(:A(XA(:A)7A)7A)7b^7A)7A)7A(σA(EA(EA(EA(EA(EA–EA(EA(EA7EA(EA(EA–EA(EA(EA(/A(/A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A)%A)7A)7Añ7A)7A)7A(λA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA)7A)7A)7Añ7A)7A)7A(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(:A)7A)7A)7bb7A^7A)7A)7A(σA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA–EA(EA(EA(/A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(╗I“7A(╗A(MA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA)%IB7A)7A(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA–XA(XA–XA(XA(XA(:A(XA(:A)7wb7A(σA(EA–EA(EA–EA–EA(EA(EA–EA(EA–EA(EA(EA(EA–EA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(╗A(λA(λA(λA(λA(λA(λA(λA7λA(λA(λA(λA(λA(ÂA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(╗A(λA(λA–λA7λA(λA(λA(λA(λA–λA(λA(:A(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(ηA(ηA–ηA–ηA(ηA–ηA–ηA(ηA(ηA–ηA(ηA–ηA(ηA(ηA(ηA(ηA(ηA(ηA(ηAzηA(ηA(ηA(−A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA–EA(EA–EA(EA(EA(EA(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(XA(XA(XA–XA–XA–XA(XA(XA–XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA4йA4йA4йA4йA4йA4йA4йA4йA3йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA3йA4йA4йA4йA4йA4йA4йA4йA4йA4йA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(…A–…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(ÂA(ÂA(ÂA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(:A(:A(:A(:A–:A(:A(:A–:A(:A(:A7:A(:A(:A(:A(:A(EA(EA(EA(EA(EA(EA(EA–EA–EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A–MA(MA(MA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A–:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA–EA(EA–EA(EA(EA–EA–EA(EA(EA(EA(EA(EA–EA(EA–EA(EA(EA–EA(EA(…A(…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(MA(MA(MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA–XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(EA–EA(EA(EA(EA–EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA(EA–EA(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(MA(MA–MA(MA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA–XA–XA(XA–XA(XA(:A–:A(:A(:A(:A–:A(:A(:A(:A(EA7EA–EA(EA–EA–EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(MA(MA(MA(MA(XA(XA(XA–XA–XA(XA–XA–XA(XA–XA–XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(ηA(ηA(XA(XA–XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(:A(:A(:A(:A–:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA–EA(EA–…A–…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(MA(MA(MA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA7XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(ηA(ηA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA–XA(XA(XA(:A(:A–:A(:A–:A(:A–:A(:A(:A(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(…A7…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A–…A(…A–…A–…A(…A(MA(…A(MA(MA(MA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA7XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–ηA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(:A(:A(:A–:A(:A(:A(:A(:A–:A(EA(EA(EA–EA(EA(EA–EA–EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA(EA–…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(MA(MA(MA–XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–ηA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A–:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA–EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA–EA(EA(EA(EA–EA(EA(EA(EA–EA(EA(EA(EA(EA–…A(…A–…A–…A(…A–…A(…A–…A(…A(…A(…A–…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(MA(XA(MA–XA(XA–XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–ηA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(:A–:A(:A(:A–:A(:A(:A–:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(MA(MA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA7XA(XA(XA(XA(XA–XA(XA(XA(XA(λA(ηA(XA(XA(XA(XA–XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A–:A(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA–EA–EA(EA(EA–EA(EA(EA(EA(EA–EA(EA–EA(EA(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(MA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–ηA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA7EA(EA(EA–EA(EA(EA(EA(EA–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A–…A(…A–…A(…A7…A(…A(…A(MA(MA–MA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA(λA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA–:A(:A(:A(:A(:A–:A(:A–:A(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA–EA(EA(EA–EA(EA(EA(EA–EA(EA(EA(EA(EA(…A(…A(…A(…A(…A–…A(…A(…A–…A(…A–…A–…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A–…A(ÂA(ÂA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(╗A(σA(λA(XA(σA(σA(XA(XA(XA(XA(XA(XA(:A)7A(╗A(XA(XA(XA(XA(XA(λA)7A(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA(σA(σA(XA(XA(XA(λA(σA(XA(:A(:A(XA(λA(σA(σA(:A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A–:A–:A(:A(:A(:A(:A(:A(:A–:A(:A(:A(:A(:A–:A(:A(:A(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(`A(`A(`A–`A(`A(`A–`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(NA(NA(NA(NA–NA(NA–MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(MA(NA(λA)7A)%A(╗A)7A)7A(╗A(╗A(λA(╗A(XA(╗A(λA)7A(╗A(XA(λA(:A(XA(XA(λA)7A(λA(╗A(╗A(λA(XA(λA(:A(XA(╗A)7A(σA(λA(╗A(λA(:A(λA(σA(λA)7A(σA(λA)7A(σA(ηA(:A(:A(λA(:A(:A(λA(λA(:A(:A(λA(:A(XA(XA4йA4йA4йA4йA4йA4йAHйA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA3йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA3йA4йA4йA)KABKA“KA7λA(λA(λA7λA(λA(λA(λA7λA(λA(λA(λA–λA(λA(λA(λA(λA(λA–λA(λA–λA7λA(λA(λA–λA(λA(λA(λA)%A)%A(σA)%A)7A(╗A(λA)7A)%A(╗A)7A)%A)7A(λA)%A)%A)7A(:A(XA(λA)7A)%A)7A(λA)7A(λA)7A(:A(XA(σA)7A(XA(9A(λA)7A)%A(σA)7A(λA)7A(σA(σA)%A(XA4йA(╗A)7A)%A)%A(λA)7A)7A(ηA)%A)%A(σA(:A(σA(ηA(σA(σA(σAzσA(σA(σA(σA(σA(σA(σA–σA(σA(σA–σA(σA(σAzσA7σA(σA(σA–σA7σA(σA(σA(σA–σA(σA–σA(σA)KA)KA)KABKA5KA5KA(λA–λA(λA–λA(λA(λA(λA(λA–λA(λA–λA(λAzλA(λA7λA(λA(λA(λA–λAzλA(λA(λA(λA(όA)%A)%A)7A(λA)7A(╗A)%A(σA)7A(λA)7A(╗A)7A(λA)7A)%A)%A(╗A(XA(λA)7A(╗A)7A(╗A)%A)7A(σA(XA(XA(λA)7A(λA(:A(λA)7A(:A(λA)7A(:A)7A(╗A(λA)7A(╗A(:A(σA)7A(λA)7A(ηA)7A(:A(λA)7A(σA(σA(λA(ηA(ηA(σA(σA(σA(σA(σA7σA(σAYσA(σA–σA–σA(σA(σA–σA–σA7σA(σA(σA(σA(σA–σA–σA(σA–σA7σA(σA(σA(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(NA(NA(NA(NA(NA(NA(NA(MA(MA(MA(MA(MA(MA(MA–MA(MA(MA(MA(MA(NA(λA(σA(λA)7A(λA)7A(╗A)7A)%A)%A(╗A)7A)%A)7A(λA(σA)7A(σA(XA(XA(λA)7A)7A)%A(XA(λA)7A(╗A(XA(XA(:A(σA)7A)%A(λA)7A(XA(λA)7A(XA)%A)7A(:A(σA)7A)7A(:A)%A)7A(σA(:A)7A(:A(:A)%A)7A(ηA(XA(XA(XA(XA4йA4йA4йA4йA4йA4йA4йA4йA4йA3йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA4йA3йA4йA4йA4йA4йA4йA4йA4йA3йA3йA4йA3йA4йA4йA4йA–…A(…A–…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(ÂA(ÂA(ÂA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(:A(XA(XA(XA(XA(XA(:A(XA(╗A)%A)%A(XA(XA(XA(XA(XA(:A(XA(XA(XA(XA(XA(:A(XA(XA(:A(XA(XA(:A(:A(XA(XA(:A(XA(XA(:A(XA(XA(XA(:A(:A(XA(XA(XA(XA(XA–:A(:A(:A(:A(:A(:A(:A(:A(:A–:A(:A(:A–:A(:A–:A(:A(:A(:A(:A(:A(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA–EA–EA(EA(EA(EA(…A(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(MA(MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(╗A(λA(:A(XA(╗A(╗A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(:A(:A(:A–:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA(EA7EA(EA–EA(EA(EA–EA(EA(EA–EA(EA(EA(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–MA(MA(MA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–σA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA–:A–:A(:A(:A(:A(:A(:A(:A(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(MA–MA(MA–XA(XA–XA(XA(XA–XA(XA(XA–XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(λA(λA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA–EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A7…A(MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA7XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(λA(λA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(:A(:A(:A(:A–:A(:A–:A–:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–MA(MA(MA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(λA(λA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA–XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A–:A(EA(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA(EA(EA(EA(EA(EA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(MA(MA(MA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(λA(λA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(:A(:A(:A(:A(:A–:A–:A(:A(:A(EA(EA(EA(EA(EA(EA(EA(EA–EA(EA–EA–EA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A–…A(MA(MA(MA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA–XA(XA(XA–XA(:A(:A(:A(:A(:A(:A(:A(:A(:A–EA(EA–EA(EA(EA–EA(EA(EA(EA7EA(EA–…A–…A(…A–…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A7…A–…A(…A(…A(…A(…A(MA(MA(XA–XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA–λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA–XA(XA–XA–:A(:A(:A–:A(:A(:A(:A(:A(:A–EA(EA–EA(EA(EA(EA(EA–EA(EA(EA(EA(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(MA(MA–MA(XA(XA(XA–XA–XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA–λA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA–XA(XA–XA(XA(XA–XA(XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(:A(:A(:A(:A(:A7:A(:A(:A(:A(EA(EA(EA–EA–EA(EA7EA(EA(EA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(MA(MA(MA(MA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA–XA(XA(XA(λA(λA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(:A(:A(:A(:A–:A–:A(:A(:A(:A(EA–EA(EA(EA(EA(EA(EA(EA(EA(EA(…A(…A(…A–…A(…A–…A–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A–…A(…A–…A7…A(…A(MA–MA–XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA(λA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA7XA–XA–XA(XA(XA(XA–XA(XA(XA–XA(XA(XA–XA–XA(XA(:A(:A(:A–:A(:A(:A(:A(:A(:A(:A–EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(…A(…A(…A7…A–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A–…A–…A(…A(…A–…A–…A(…A(…A(…A(…A(…A–MA(MA(MA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(λA(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–:A(:A–:A(:A(:A(:A(:A–:A(EA(EA(EA(EA(EA(EA(EA(EA(EA(EA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A(`A(`A(`A(`A(`A(…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(MA(MA(MA(MA(MA–XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(λA(λA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–:A(XA(XA–XA(XA(XA(XA(:A(:A(:A(:A(:A–:A(:A–:A(EA(EA–EA(EA(EA(EA–EA(EA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(╗A(╗A(╗A(╗A(╗A(╗A(╗A(╗A(╗A(╗A(╗A(╗A–╗A(╗A–╗A(╗A(╗A(╗A(╗A(╗A(╗A(ÂA(…A(…A(…A(MA(…A(…A(…A(…A(…A(…A(MA(MA(MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(MA(λA(λA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(:A(λA(λA(λA(λA–λA(λA(λA(λA(λA(λA(λA(λA–λA(λA(λA(λA(:A(:A(:A(:A(:A(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(:A–:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(EA–EA(EA(EA(EA(EA(EA(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(`A)Kb)7A)7A)7A)7A)%A(λA(λA(╗A(…A(MA(MA(…A(…A(…A(…A(MA(MA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(MA(λA(λA(XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(λbb7A)7A)7A)7A)%A(σA(ηA(¢A(:A(XA(XA(:A(XA(XA(XA–XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A(:A–EA(EA7EA(EA(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7A)7A“7A!7A57AB7A57Aλ7A)7A)%A(λA(╗A(MA(MA(…A(…A(MA(MA(MA(MA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(MA–λA(XA(XA(XA(XA–XA–XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(λA)7A)7A57I“7Añ7A)7A(σA(:A(XA(XA(:A(XA(XA(XA(XA–:A(:A(:A(:A(:A(:A(:A(:A(:A–EA(EA(EA(EA(EA(EA(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(`A)KA)7A)7Iñ7AB7A)7A57AB7A)7A)"A(╗A(MA(…A(…A(MA(MA(MA(MA(MA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(MA(λA(λA(MA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7Iñ7A57A)7A)7A)7A)7AB7A(σA(:A(XA(:A(XA(XA(XA(:A–:A(:A(:A(:A(:A(:A(:A–:A(:A(EA(EA(EA–EA–…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(`A)KA)7A)7b!7A)7A)7A)7A57A)7A(λA(ÂA(MA(…A(…A–MA–MA(XA(XA–XA7XA(XA(XA(XA(XA(XA(XA(MA(λA(λA(MA(XA(XA–XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7b!7A)7A)7A)7A)7A)7A(:A(XA(:A(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A7:A(EA(EA–EA–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7bñ7A)7A)7A)7A)%A(ÂA(MA(…A(…A(MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(MA(λA(λA(MA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(λA)7A)7bλ7A)7A)7A)7A(:A(XA(:A(XA(XA(XA(:A–:A(:A(:A(:A–:A(:A(:A(:A(EA(EA(EA(EA(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7w)7A)7A)7A)7A(╗A(MA(…A(MA(MA(MA–MA(XA(XA(XA(XA(XA7XA(XA(XA(XA(MA(λA(λA(MA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(λA)7A)7bñ7A)7A)7A)7A(:A(XA(:A(XA(XA(XA–:A(:A(:A–:A(:A(:A(:A(:A7EA(EA–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(`A)KA)7A)7w57A)7A)7A)%A(ÂA(MA(…A(MA(MA(MA(MA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(MA(λA(λA(MA(XA(XA7XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7I)7A“7I!7A)7A)7A(ηA(XA(:A(XA(XA(XA(XA(XA(:A(:A(:A–:A(:A(:A(:A(:A(EA–EA(…A–…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(…A(`A)KA)7A)7wB7A)7A)7A)%A(…A(…A–…A(MA–MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(MA(λA(λA(MA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA(λA)7A)7I^7A)7A)7I57A57A)7A(:A(XA(XA(XA(XA(XA(XA–:A(:A(:A(:A(:A–:A(:A(:A–:A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7I)7A“7A)7A57A)7I!7A)7A)7A(λA(MA(…A(…A(MA(MA(MA(XA–XA(XA(XA(XA(XA(XA(XA(XA(MA(λA(λA(MA(XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(λA)7A)7Ib7A)7A)7A57A)7AB7A)7I57A)7A)7A(¢A(XA(:A(XA(XA(XA(XA(:A(:A(:A(:A(:A(:A–:A(:A(:A(:A(:A(…A(…A(…A(…A–…A–…A(…A(…A(…A(…A(…A–…A(…A(`A)KA)7A)7Iñ7A)7A)7IB7A)7A)7A)7A(ÂA(MA(…A–…A–MA(MA(XA(XA(XA–XA(XA(XA(XA(MA(λA(λA(MA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(:A(:A(:A(:A(:A(λA)7A)7A)7I)7A)7A)7A(ηA(XA(:A(XA–XA–XA(XA–:A(:A(:A(:A(:A(:A(:A–:A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(╗A(╗A(╗A(╗A(╗A(λA)KA)%A57A)7IB7A)7A)7A(λA(MA(…A(…A(…A(MA(MA(MA(XA–XA–XA(XA(XA(XA(MA–λA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(:A)%A)7A)7Ib7A)7A)7A(σA(XA(XA(XA(XA–XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(:A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(`A(…A(…A(…A(`A(…A(…A(╗A)%A)7A)7I57A)7A)7A)7A(ÂA(…A(…A(…A(…A(MA(MA(MA(MA(XA(XA(XA(XA(XA(XA(MA(λA(λA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(:A)7A)7A)7Añ7A)7A)7A(σA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A–:A(:A(:A(:A(:A(`A(`A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(`A(…A)%A)7A)7I57A)7A)7A(╗A(MA(…A(…A(…A(…A(MA(MA(MA(XA(XA(XA(XA(XA(XA(MA(λA(λA(MA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(XA(σA)7A)7Añ7A)7A)7A(σA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A7:A(:A–:A(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A)KA)7A)7I)7A)7A)7A(όA(…A(…A–…A(…A(…A–MA(MA7XA(XA(XA(MA(λA(λA(MA(XA(XA(XA(XA–XA–XA–XA(XA(XA–XA(XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(XA(ηA)7A)7Añ7A)7A)7A(σA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(:A(:A(:A(:A(:A(:A(:A(`A(…A(`A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A)%A)7A)7Ib7A)7A)7A)%A(…A(…A(…A(…A(…A(…A(MA(MA–MA(MA(XA(XA(XA(MA(λA(λA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(XA(ηA)7A)7Añ7A)7A)7A(ηA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(:A–:A(:A(:A(`A(`A–`A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A7…A(…A(…A(…A(…A(…A(╗A)7A)7Ib7A)7A)7A)7A(ÂA(…A(…A(…A(…A(…A(…A(…A(MA(MA(MA(MA(XA(XA(MA–λA(MA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(XA)%A)7A)7Añ7A)7A)7A(λA(XA(XA–XA–XA7XA(XA(XA–XA(XA–:A(:A(:A(`A(`A–`A(…A(…A(…A(…A(…A7…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A)"A)7A)7I57A(╗A(…A(…A(…A(…A–…A(…A(…A(MA–MA(MA(XA(MA(λA(λA(MA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(╗A)7A)7Añ7A57A)7A(:A(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(:A(:A(:A(`A(`A(`A(`A(`A–…A(…A(…A–…A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(╗A)7A)7Ib7A)7A)7A(λA(MA(…A(…A(…A(…A(…A(…A–…A(MA–MA(XA(MA(λA(λA(MA(XA–XA(XA(XA(XA–XA(XA(XA(XA–XA–XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(:A)7A)7A)7Añ7A)7A)7A(ηA(XA(XA(XA(XA7XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(:A(:A(`A–`A(`A–`A(`A(…A(…A(…A–…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A)7A)7A)7Añ7A)7A)7A(λA(MA(…A(…A(…A(…A(…A(…A(…A(…A(…A–MA(XA(MA(λA(λA(MA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(:A(λA)7A)7A)7Añ7A)7A)7A)7A(:A(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(:A(`A(`A(`A(`A–`A(`A–…A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A)%A)7A)7Añ7A)7A)7A(λA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(MA(ÂA(MA–λA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7Ib7A)7A)%A(σA(σA)%A)7A57A)7Añ7A)7A)7A)7A(λA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(:A(`A(`A(`A(`A(`A(`A(`A–`A(…A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A)"A)7A)7Añ7A)7A)7A(λA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(ÂA(MA–λA(MA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7I^7A)7A)7Añ7A)7A57A(λA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(`A–`A(`A(`A–`A–`A(`A(…A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A)"A)7A)7Añ7A)7A)7A(λA(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(MA(λA(λA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(λA)7A)7I)7A“7A)7Aλ7A)7A)7A57A)7A(λA(XA–XA(XA(XA–XA(XA(XA–XA(XA–XA(XA(XA(XA(XA–XA–XA(`A(`A(`A–`A(`A(`A(`A(`A(`A–…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A–…A(…A(…A–…A(…A(…A(…A(…A)%A)7A)7Añ7A)7A)7A(λA(…A(…A(…A–…A(…A(…A7…A–…A(…A(MA(λA(λA(MA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(λA)7A)7b^7A)7A(σA(:A(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA–XA–XA(XA–XA(XA(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A(…A(…A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A)%A)7A)7Añ7A)7A)7A(λA(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(MA(λA(λA(MA(XA(XA–XA7XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(λA)7A)7bB7A)7A)%A(ηA(:A(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A)%A)7A)7Añ7A)7A)7A(λA(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(λA(λA(MA(XA–MA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7b)7A)7A)7A)%A(:A(XA(XA(XA(XA–XA(XA–XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–`A(`A(`A(`A–`A(`A(`A(`A(`A–`A(…A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(ÂA)7A)7A)7Añ7A)7A)7A(╗A(…A(…A–…A(…A7…A(…A(…A(…A(…A(…A(MA(λA(λA(MA(ÂA–MA(MA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(λA)7A)7b“7A)7A(σA(:A(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA7XA(XA(XA(XA(XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A–`A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A(╗A)7A)7Añ7A)7A)7A)7A(╗A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(MA(λA(λA(MA(ÂA(MA–MA7XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(λA)7A)7I)7A)7A)7Ib7A)7A57A)7A(╗A(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A(`A–`A–`A(`A–`A(…A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A–…A–…A(…A(…A(…A(…A(…A)"A)7A)7Añ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(MA(λA(λA(MA(ÂA(MA(MA(MA–MA(XA–XA(XA–XA(XA(XA(XA(XA(XA(MA(λA)7A)7IB7A57Ib7A)7A57A(λA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA–XA(XA–XA(XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(╗A)7A)7Ib7A)7A)7A)%A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA–λA(MA(…A(…A(MA(MA(MA(MA(XA(XA(XA–XA(XA(XA–XA(XA(XA(MA(λA)7A)7Ib7A)7A)%A)%A57A)7Ib7A)7A)7A)7A(:A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A)%A)7A)7Ib7A)7A)7A(λA(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(MA(λA(λA(MA(…A(…A7MA(MA(MA(XA(XA7XA(XA–XA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(╗A)7A)7A)7Ib7A)7A)7A)%A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A(λA)7A)7I57A)7A(╗A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(…A(NA(λA(λA(NA(…A(…A(…A(…A(MA(MA(MA(MA(XA(XA(XA(XA(XA(XA–XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(:A)7A)7A)7Ib7A)7A)7A(λA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A(λA)7A)7I)7A)7A)7A)%A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(NA(λA(λA(NA(…A(…A(…A(…A(…A(MA(MA(MA(XA(XA(XA(XA(XA–XA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(λA)7A)7Ib7A)7A)7A)%A–XA(XA(XA(XA(XA(XA7XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(`A(…A(`A(`A(`A(`A(`A(…A)"A)7A)7I57A)7A)7A(╗A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(NA(λA(λA(NA(…A(…A–…A(…A(MA(MA(MA(MA(MA(XA(XA(XA–XA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(σA)7A)7Ib7A)7A)7A(╗A(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(`A–`A(`A(`A–`A(`A(`A(`A(`A–`A(`A(`A(…A(`A)KA)7A)7Aλ7A)7A)7A)7A(…A(…A(…A(…A(…A(╗A(λA)"A)7A)7A)7I57A)7A)7A)%A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(NA–λA(NA(…A(…A–…A–…A(…A(MA(MA–MA(XA(XA–XA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(╗A)7A)7Ib7A)7A)7A(σA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(…A(`A)KA)7A)7Ib7A)7A)7A57A)7A)7A“7A)7I57A)7A)7A)7A(╗A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A(…A(…A(NA–λA(NA(…A(…A(…A(…A–…A–…A(MA(MA(MA–MA(XA–XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA–XA(XA(XA)%A)7A)7I)7A)7A(:A(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(…A(`A)KA)7A)7Iï7A57A)7IB7A)7A)7A)KA(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(NA(λA(λA(NA(…A(…A(…A(…A(…A–…A(…A(…A(MA–MA–XA(XA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(λA)7A)7Ib7A)7A)7A(λA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A)KA)7A)7I)7A!7I^7A)7A)7A)%A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A–λA(NA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–MA(MA(MA(XA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(:A)7A)7A)7Añ7A)7A)7A)%A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(`A(`A(`A(`A7`A7`A–`A(`A(`A(`A(`A(`A)KA)7A)7w)7A)7A)7A)%A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(`A(λA(λA(NA(…A(…A–…A(…A(…A(…A(…A(…A(…A(MA(MA–MA(MA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(σA)7A)7Ib7A)7A)7A(╗A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A)KA)7A)7bñ7A)7A)7A)7A)%A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(`A(λA(λA(NA(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(MA(MA(MA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(λA)7A)7Ib7A)7A)7A(σA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A)KA)7A)7bλ7A)7A57A)"A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A–λA(`A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–MA(MA(MA(XA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA–XA(XA(XA(XA(XA)7A)7A)7I)7A)7A(:A(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(®A(`A(`A(`A(`A(`A–`A(`A(`A–`A(`A(`A(`A(`A(`A)KA)7A)7b!7A)7A)7A57A)7A(λA(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(`A(λA(λA(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(MA(MA(MA(MA(XA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(XA(σA)7A)7Ib7A)7A)7A(λA(XA(XA(XA(XA(XA–XA–XA(XA(XA–XA(XA(XA–XA(®A(®A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A)KA)7A)7b)7A)7A)7A)7A)7A57A)7A)"A(…A(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A–…A(…A(…A(…A(`A(λA(λA(`A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(MA(ÂA(MA(λA)7A)7Aλ7A)7A)7A)7A(XA(XA(XA–XA(XA(XA(XA(╗A)7A)7Ib7A)7A)7A)%A(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(®A(®A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A)KA)7A)7Iï7A)7A57A!7A)7A)KA(…A(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A–…A(…A(…A(…A(`A–λA(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(MA(ÂA(MA(λA)7A)7AB7A!7A)7A)7A)7A(XA(XA(XA(XA(XA(XA(XA(XA(XA)7A)7A)7I)7A)7A(:A(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(®A(®A(®A–`A(`A(`A–`A–`A(`A(`A(`A(`A(`A(`A)KbB7A)7A)%A)KA(╗A(…A(`A(`A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(`A–λA(`A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(ÂA(MA(λIB7A(XA(XA(XA(XA(XA(XA(XA(XA(XA(σI“7A(σA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA–®A(®A(`A(`A–`A(`A(`A(`A(`A–`A(`A(`A(`A(`A))A)KA)KA5KA)KA)KABKA5KA)KA5KA5KA)KA)KA)KA)KA(╗A(╗A(╗A(…A(…A(`A(`A(…A–…A(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A–…A(…A(…A(…A(`A(λA(λA(`A(…A–…A(…A–…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(MA(╗A(λA(λA(λA–λA(λA(λA(λA(λA(λA(λA(λA(λA(XA(XA(XA(XA–XA(XA(XA(XA(╗A(λA(λA(λA(λA–λA(λA(λA(λA(λA–λA(λA(λA(λA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–®A–®A(®A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(`A(λA(λA(`A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(MA(MA(MA(MA(MA(MA–MA(MA(MA(MA(MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–®A(®A(®A(®A(`A–`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A–…A(…A(…A7…A–…A–…A–…A(…A(…A(…A7…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A–…A(…A(`A(λA(λA(`A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(ÂA(ÂA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(®A(®A(®A–®A(®A(®A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(…A(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A–…A(…A(`A(λA(λA(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A–…A(MA(MA(MA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA–XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(®A(®A(®A(®A–®A(®A–`A(`A(`A(`A–`A(`A–`A(`A–`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(…A(…A(…A(…A(…A(…A(…A(…A7…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A7…A(…A(…A(…A–…A(…A(…A(…A(`A(λA(λA(`A(…A(…A(…A–…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A–…A(MA(MA(MA(MA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA–XA–XA(XA(XA(XA–XA(XA–XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(®A(®A(®A–®A(®A(®A(®A(®A(`A(`A(`A(`A–`A(`A–`A–`A(`A–`A(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A(`A–…A(…A(…A(…A(…A–…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(`A(λA(λA(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A7MA(MA(XA(XA–XA(XA–XA(XA–XA(XA(XA(XA(XA–XA(XA–XA–XA(XA–XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(®A(®A(®A–®A(®A(®A–®A(®A(`A(`A(`A(`A–`A(`A–`A(`A(`A(`A(`A(`A(`A7`A(`A–`A(`A(`A(`A(`A(`A(…A(…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A–…A–…A–…A(…A(…A7…A(…A(…A(…A(`A–λA(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(MA–MA(XA(XA–XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA–XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA–XA(®A(®A(®A(®A(®A(®A–®A–®A(®A–`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A7`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A–…A(…A(…A–…A(…A(…A–…A(…A(…A(…A(`A–λA(`A(…A–…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(MA(MA–MA(XA(XA(XA(XA(XA–XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA–XA(XA(®A(®A(®A(®A(®A(®A(®A(®A(®A(®A(®A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A–`A(`A(`A–`A(`A(`A(`A(`A–…A–…A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(`A–λA(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(MA–MA(MA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–®A(®A(®A–®A(®A(®A7®A(®A(®A(®A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(…A–…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(`A)KA(λA(`A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(MA(MA(MA(MA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA–XA(XA7XA(XA(XA–XA(XA(XA(XA–XA(XA(XA–XA(XA(®A(®A–®A(®A(®A(®A–®A(®A(®A(®A(®A(®A(`A–`A(`A7`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(`A)KA(λA(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(MA(XA(XA(XA(XA(XA(XA(XA(XA–XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA–XA–XA(XA–XA(XA(XA(XA(XA–XA(®A(®A–®A–®A(®A(®A(®A(®A(®A(®A(®A(®A(®A(`A–`A(`A–`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A(`A(…A(`A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A7…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(`A)KA)KA(`A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(MA(MA(XA(XA(XA(XA7XA(XA(XA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(®A(®A(®A(®A(®A(®A(®A(®A(®A(®A(®A(®A–®A(®A–`A(`A(`A(`A(`A(`A(`A(`A(`A–`A–`A(`A(`A(`A(`A(`A–`A(`A(`A–`A–`A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(`A5KA(`A(…A–…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A(…A–…A(…A–…A(…A(…A(…A(…A(…A(…A–…A(…A(MA(MA(MA(MA(XA(XA–XA–XA(XA(XA(XA(XA(XA–XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA–XA(XA(XA(XA7XA–XA(XA(XA(XA(XA(XA(®A(®A(®A–®A–®A(®A(®A(®A–®A(®A(®A(®A(®A(®A(`A(`A–`A(`A(`A–`A(`A(`A(`A(`A(`A(`A(`A(`A(`A(`A–`A(`A(`A(`A(`A–`A(`A(…A(…A(…A(…A(…A(…A(…A7…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A(`A)KA)KA(`A(…A(…A(…A–…A(…A(…A(…A(…A(…A(…A–…A(…A(…A(…A(…A(…A–…A(…A(…A–…A–…A(…A(…A(…A–MA(MA(MA(XA(XA(XA–XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(XA(X""")

def startup():
    "Shows startup screen."
    w, h = resolution(res2pix(300, 300))
    draw(resize(logo(), 300, 300))
    time.sleep(1.5)
    clear()

startup()

