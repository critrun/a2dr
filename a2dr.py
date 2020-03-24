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
#to see the people who made this library possible just scroll through the code
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

def clr():
    "Best way to clear the screen."
    print("\033[F"*(get_terminal_size()[1]+2))

def draw(img):
    "Draws img on screen."
    width=int(img[0:4])
    img=img[4:]
    w, h = get_terminal_size()
    he=len(img)/9/width
    we=round((w-width)/2)
    img=img.replace("i", "0")
    temp=round((h-he)/2)
    clr()
    print("\n"*temp)
    line="  "*we
    temp=len(img)
    for xp in range(round(temp/9)):
        x = xp*9
        line+=convert(int(img[x:x+3]), int(img[x+3:x+6]), int(img[x+6:x+9]))
        if(round(xp/width) == xp/width):
            line+="\n"+"  "*we
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
    return uncompress("""IAb!BAαό0ñBIzό0“BIαό0bBb–ό1ïBbzό1!BbZό1BBbαό1)BAZόA)BIZόA5BAYό1bBAYόA“BI–όA“BAYόOñBAZόbbBAZόOλBAZόbbBAZόOïBA£όbbBA£όO^BA£όbbBA£όI)BA7όA)BA(όA)BA7όA)BA(όA)BA(όA)BA(όA)BA(όA)BA–όA5BA(όw5BAZόb5BAZόI)BA(όABBA(όA5BA(όA5BA(όA)BA(όA)BA(όA)BA(όA)BA(όA)BA(όwBBA£όb5BA£όIbBA(όA)BA(όA)BA(όA5BA(όA5BA7όA)BA(όA)BA(όA)BA–όw“BA£όb5BA£όIbBA(όA)BA(όA)BA(όA5BA(όA5BA(όA)BA(όA)BA(όA)BA(όA)BA(όA)BA(όwBBA£όbBBAZόIbBA7όA)BA(όA5BA(όA5BA(όA)BA(όA)BA7όA)BA–όA5BA(όw)BA£όbBBAZόO“BA£όb5BA£όIbBA7όA)BA–όA5BA(όA)BA7όA)BA7όA)BA7όA)BA–όA5BA7όb!BA£όb5BA£όIbBA(όABBA(όA)BA(όA)BA(όA5BA(όA5BA(όABBA(όA)BA(όA)BA(όA)BA(όA)BA(όbïBA£όb5BA£όIbBA(όABBA–όA5BA(όA5BA(όA5BA(όABBA(όA)BA(όA)BA–όA5BA–όb^BA£όb5BA£όIbBA(όABBA(όA)BA(όA)BA(όA5BA(όA5BA(όABBA(όA)BA(όA)BA(όA)BA(όA)BA(όbλBA£όbbBA£όI)BA7όA)BA(όA)BA(όA)BA(όA5BA(όA5BA7όA)BA7όA)BA(όA)BA(όA)BA7όb^BAαόIλBAαόO^BAüόI^BAüόOïBA7όA5BAYόI5BIIόOλBAzόA5BAZόAλBI–όOñBAzόA5BAYόAλBI(ό1bBAzόABBA7όIbBIIό1)BAzόI!BAüό1BBAzόI“BAαό1!BA£όIbBA£ό1ïBAZόIbBAZό0bBAYόAñBAzό0“BA–όIbBA–ό−ïBA7όwïBIYόAλBIαόIλBAYόI5BIZόAλBI£όA^BbIόI!BAZόI5BIαόA^BIαόA!Bb(όI“BA£όI)BIüόA!BA7όI)BAYόA“BA7όI!BAzόI5BAαόb^BAzόA!BA7όIBBAzόABBA7όI^BAzόI)BAüόb^BAzόA“BA7όIBBAzόABBA7όIïBA7όIbBAYόA)BAzόb!BAYόA“BA7όI“BAzόA5BA7όIïBA7όAñBAYόA5BAYόIBBIZόA“BA7όI!BA7όA5BA7όIïBA7όAñBAYόABBAYόIbBI£όA!BA7όI!BA7όA5BA7όIïBA7όAλBAYόA“BAYόAñBIαόA!BA7όI!BA7όA5BA7όIïBA7όAλBAzόA^BAYόAλBI£όA^BA7όI!BA7όA5BA7όI^BA7όAλBAYόAïBAzόAïBIZόAλBA7όI!BA7όA5BA7όI!BA7όAλBAYόA5BI(όA^BAzόbbBA7όI!BA7όA5BA7όA5BIYόAñBAYόA)BI–όA^BA7όb)BA7όI“BA7όABBA7όA5BIzόAñBAYόA5BI7όA!BA7όb)BA7όI“BA7όABBA7όA5BI7όIbBAzόI5BAYόA“BA7όb)BA7όIBBA7όA“BA7όIbBAZόAλBAYόI5BAYόA“BA7όb)BA7όI)BAYόA“BA7όI)BAZόA^BAYόI“BAYόABBIüόA!BIαόA!BA7όI5BAZόA!BAYόI!BAzόABBIüόA!BI£όA^BA7όIBBAZόABBAYόI^BAYόA5BIüόA!BIzόAñBA7όI!BAYόq“BI)4A!BAü–A)BII.O“BA54AλBA54A5BA7–AñBA–.AïBA–.OBBA54AñBA54A)BA––IbBA–.AλBA–.O5BA54AñBA54A––I)BA–.AλBA–.O5BA54AñBA54A––I)BA–.AλBA–.O5BA54AñBA54A––I)BA–.AïBA–.OBBA54AλBA54A)BA––ABBA£–A)BA–.A)BAü.O5BA54A)BAï4ABBA––AλBA––A)BA–.AïBA7.O5BA54A^BA54A“BA––AïBA––A)BA–.AλBA–.O5BA54AïBA54A“BA––A^BA––A)BA–.AλBA(.OBBA54AλBA54A“BAü–A)BII.w)B""")

def startup():
    "Shows startup screen."
    resolution(res2pix(100, 72))
    img = logo()
    draw(img)
    time.sleep(0.5)
    for i in range(6):
        draw(swap_col(img, "306000000", str(i*42+1000)[1:]+"000000"))
    for i in range(6):
        draw(swap_col(img, "306000000", str(255-i*42+1000)[1:]+str(i*42+1000)[1:]+"000"))
    for i in range(6):
        draw(swap_col(img, "306000000", "000"+str(255-i*42+1000)[1:]+str(i*42+1000)[1:]))
    for i in range(6):
        draw(swap_col(img, "306000000", "000000"+str(255-i*42+1000)[1:]))
    draw(img)
    time.sleep(0.5)
    clear()

startup()

