import ctypes
import os
import msvcrt
import subprocess
from ctypes import wintypes
clear = lambda: os.system('cls')
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

#incoming code made by Marfisa and light editing by me
def pixel_size(pix):

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

#incoming code made by granitosaurus and light editing by me
def get_terminal_size(fallback=(80, 24)):
    for i in range(0,3):
        try:
            columns, rows = os.get_terminal_size(i)
        except OSError:
            continue
        break
    else:  # set default if the loop completes which means all failed
        columns, rows = fallback
    return columns/2, rows-3

#incoming code made by me, critcore :)
def resolution(pix_size):
    pixel_size(pix_size)
    w, h = get_terminal_size()
    return int(w), int(h)

def try_res(pix_size):
    clear()
    w, h=resolution(pix_size)
    x2=0
    x3=0
    image=""
    while(x3<h):
        while(x2<w):
            image=image+convert(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x2+=1
        print(image)
        image=""
        x2=0
        x3+=1
    print(image)
    
def test_image():
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
                image=image+convert(r, g, b)
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

def draw_legacy(img, width):
    w, h = get_terminal_size()
    he=len(img)/9/width
    we=round((w-width)/2)
    x=0
    img=img.replace("i", "0")
    temp=round((h-he)/2)
    clear()
    """while(x<temp):
        print(" ")
        x+=1
    """
    print("\n"*temp)
    x=0
    x1=0
    """
    ti=0
    line=""
    while(ti<we):
        line+="  "
        ti+=1
    """
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
        print(line)
        line="  "*we
        """
        line=""
        ti=0
        while(ti<we):
            line+="  "
            ti+=1
        """
        #line="  "*we
        x1=0

def clr(rows):
    print("\033[F"*(rows+2))

def draw(img, width):
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
        x1=0
    print(line)

def img_convert(img, width, height):
    w=width
    h=height
    img = Image.open(img)
    img = img.resize((w, h), Image.ANTIALIAS)
    img=img.convert("RGB")
    y=0
    out=""
    sec=0
    secf=100000/w
    while(y<h):
        x=0
        while(x<w):
            r, g, b = img.getpixel((x, y))
            r=str(int(r)+1000)[1:]
            g=str(int(g)+1000)[1:]
            b=str(int(b)+1000)[1:]
            out+=str(r)+str(g)+str(b)
            x+=1
        if(sec>secf):
            draw_legacy(load(round(y/h*100), "converting image"), 102)
            sec=0
        sec+=1
        y+=1
    return out

def recommended_res(fps):
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
    x=0
    recent=img[0:9]
    times=0
    final=""
    book="""AIbwE/O1064()P2[].KR3–5q"%GN9jH7BMXLD;+':z“”€$¢−_QVY!#&*<=>?@Z^`{|}~•…Â£ï»¿∩╗┐§×ΚαλημέρκόσεüñРуский®"""
    while(x<len(img)+9*18):
        if(img[x:x+9]==recent):
            times+=1
        else:
            final+=str(times+1000)[1:]+recent
            times=1
        if(times==999):
            final+=str(times+1000)[1:]+recent
            recent=""
            times=0
        recent=img[x:x+9]
        x+=9
    x=0
    out=""
    while(x<len(final)):
        out+=book[int(final[x:x+2]):int(final[x:x+2])+1]
        x+=2
    return out

def uncompress(img):
    temp=""
    x=0
    book="""AIbwE/O1064()P2[].KR3–5q"%GN9jH7BMXLD;+':z“”€$¢−_QVY!#&*<=>?@Z^`{|}~•…Â£ï»¿∩╗┐§×ΚαλημέρκόσεüñРуский®"""
    while(x<len(img)):
        temp+=str(book.index(img[x:x+1])+100)[1:]
        x+=1
    img=temp
    x=0
    final=""
    while(x<len(img)):
        times=int(img[x:x+3])
        x2=0
        while(x2<times):
            final+=img[x+3:x+12]
            x2+=1
        x+=12
    return final

def resize(img, img_w, w, h):
    img_w=int(img_w)
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
    return out

def str2img(s):
    img=uncompress("AY9)α9A4AAAAAY9)α9A4AAAAII9)α9A4AAAAA(9)α9A3AAAAA–9)α9A4AAAAA–9)α9A3AAAAIü9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAI(9)α9A4AAAAbI9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA–9)α9A3AAAAA(9)α9A4AAAAA–9)α9A3AAAAA(9)α9A3AAAAA(9)α9A3AAAAA(9)α9A4AAAAA(9)α9A3AAAAA–9)α9A4AAAAA–9)α9A3AAAAA(9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA–9)α9AHAAAAA(9)α9A4AAAAA(9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA(9)α9A3AAAAA(9)α9A3AAAAA(9)α9A3AAAAA–9)α9A4AAAAA–9)α9A3AAAAA(9)α9A:AAAAA–9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA(9)α9A3AAAAAZ9)α9A4AAAAA(9)α9A3AAAAA(9)α9A4AAAAA79)α9A4AAAAA–9)α9A4AAAAA(9)α9A4AAAAAz9)α9A3AAAAA79)α9A4AAAAA(9)α9A3AAAAA(9)α9A4AAAAAY9)α9A4AAAAA79)α9A4AAAAA79)α9A4AAAAA(9)α9A4AAAAA(9)α9A4AAAAA–9)α9A4AAAAA(9)α9A4AAAAA(9)α9A3AAAAA(9)α9A3AAAAA(9)α9A4AAAAIY9)α9A3AAAAAα9)α9A4AAAAA(9)α9A4AAAAA(9)α9A4AAAAA(9)α9A4AAAAA–9)α9A4AAAAA–9)α9A3AAAAA(9)α9A4AAAAA–9)α9A3AAAAA(9)α9A3AAAAA(9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA–9)α9A3AAAAA(9)α9A4AAAAA–9)α9A3AAAAA(9)α9A4AAAAA–9)α9A4AAAAA(9)α9A3AAAAA(9)α9A4AAAAA(9)α9A4AAAAA(9)α9A4AAAAA–9)α9A4AAAAA–9)α9A4AAAAA(9)α9A4AAAAA(9)α9A4AAAAA(9)α9A3AAAAA(9)α9A:AAAAA(9)α9A3AAAAA(9)α9A3AAAAA–9)α9A4AAAAA(9)α9A3AAAAA–9)α9A4AAAAA(9)α9A3AAAAA–9)α9A4AAAAA–9)α9A3AAAAA(9)α9A4AAAAA79)α9A4AAAAAY9)α9A4AAAAAz9)α9A3AAAAAz9)α9A4AAAAAY9)α9A4AAAAAα9)α9A3AAAAA–9)α9A4AAAAA(9)α9A4AAAAAz9)α9A4AAAAA(9)α9A4AAAAA79)α9A4AAAAA(9)α9A4AAAAA(9)α9A4AAAAA(9)α9A4AAAAA(9)α9A4AAAAAü9)α9A3AAAAA£9)α9A3AAAAAz9)α9A3AAAAAY9)α9A4AAAAA(9)α9")
    alpha="abcdefghjklopqrstuvxyz234567890%"
    x=0
    o="000000000"
    f="128128128"
    out=""
    row=0
    while(row<5):
        while(x<len(s)):
            c=s[x:x+1]
            if(alpha.find(c)==-1):
                if(c=="i"):
                    out+=f+o
                if(c=="m"):
                    if(row==0):
                        out+=o+f+o+f+o+o
                    if(row>0):
                        out+=f+o+f+o+f+o
                if(c=="n"):
                    if(row==0):
                        out+=f+o+o+f+o
                    if(row==1):
                        out+=f+f+o+f+o
                    if(row==2):
                        out+=f+o+f+f+o
                    if(row>2):
                        out+=f+o+o+f+o
                if(c=="w"):
                    if(row==4):
                        out+=o+f+o+f+o+o
                    if(row<4):
                        out+=f+o+f+o+f+o
                if(c=="1"):
                    out+=f+o
                if(c==" "):
                    out+=o+o
                if(c=="<"):
                    out+=o
                if(c==">"):
                    out+=f
            else:
                n=alpha.index(c)*3*9+row*96*9
                out+=img[n:n+9+9+9]+o
            x+=1
        x=0
        row+=1
    #imnw1
    return out, len(out)/5/9

def swap_col(img, colour1, colour2):
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
    return out

def load(percent, title):
    bar=uncompress("YIηK7η")
    title="<"+title
    temp, wi=str2img(title)
    temp=""
    while(len(temp)<102-wi):
        temp+="<"
    title, wi=str2img(title+temp)
    title=swap_col(swap_col(title, "000000000", "010010170"), "128128128", "220220220")
    x=0
    temp="<"
    while(x<percent):
        temp+=">"
        x+=1
    while(len(temp)<102):
        temp+="<"
    load, temp=str2img(temp)
    load=swap_col(swap_col(load, "000000000", "183183183"), "128128128", "255255255")
    out=swap_col(bar[:102*9], "183183183", "010010170")+title+swap_col(bar[:102*9], "183183183", "010010170")+bar[:102*9]+load+bar[:102*9]
    return out

def logo():
        return uncompress("""®ε)I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)NÂ)I3)A4PI3[A4OIHAA(EA))A(5Ab_A(]Ab;A–KAb+A(RAb;A(RAb+A(3Ab+A(.AbBA(BAb*A4ïAY;A4AIHAA4[I3Rb@)I3)A4PI3[A4EIHAA4;IA>A($Ab*A(7AbjA(LAbLA–DAbLA–DAbXA(;AbXA(+AbLA(+AbXA(+AbLA('AbXA–:AbMA(:AbXA–zAbXA(zAbMA–”AbXA7€AbMA($AbMA(€AbXA–$AbMA(¢AbBA(¢AbMA(−AbMA–−AbBA(QAb7A–QAbBA(VAbBA(QAbMA(VAbBA(VAbMA(YAbBA–!Ab7Az#AbBA(&Ab7A(!Ab9A(~AbQA(KA7∩A4AIHAA4]I3KI3)I3)A4.I3RA4AIHAA((Az*A(§AbYA(@Ab%A(`AbHA(|AbHA(|AbjA({AbjA(|AbjA–}AbjA7~AbjA(•Ab9A(…AbjA–…Ab9A(ÂAb9A(ÂAbNA(£Ab9A(ïAbNA(ïAb9A(£Ab9A(£AbNA(¿AbNA(»Ab9A(¿Ab9A(¿AbNA(¿Ab9A(∩Ab9A(∩AbNA(∩Ab9A–╗AbNA(∩Ab%A(κAbzA(−A–όA4AIHAA4]I3.b4)I3)A42I32A4IIHAA4“IA−A)/AbzA(κAb3A(εAb%A(üAb"A–üAb%A(ñAb%A(ñAb"A7РAb"A(уAb"A(сAbqAzкAbqA7иAbqA(йAbqA(®Ab5Az®AbqA)AAb5A)AAbqA)IAb5A)IAbqA“wAb5A)EAb–A5EAb5A)/Ab–A)AAb2A)jAb¢A4μAΚεA4AIHAA4]I3.wÂ)I3)A4(I34A4)I3PA(PAbXA(.Ab”A–[Ab'A–]Ab'A(.Ab+A(KAb+A(RAb+A–KAb+A–RAb+A(3Ab+A(KAbXA(HAb*A4κAz•A4AIHAA4[I3RbH)I3)A4PI3[A4EIHAA4;IA>A($Ab*A(HAbjA–LAbLA–DAbLA(;AbXA(DAbLA7+AbXA–'AbXA('AbLA(:AbXA(zAbXA(zAbLA(“AbLA(“AbXA(zAbXA(“AbMA(€AbMA(€AbXA–”AbMA(€AbMA–$AbMA(−AbMA(¢AbMA–−AbBA(−AbMA(_AbBA7QAbBA–VAbBA(YAb7A7!Ab7A7!AbBA–#Ab7A(&Ab7A(*Ab7A(&AbHA(`Ab”A(DA5IA4bIHAA42I3]Aε)I3)A4.I3RA4AIHAA(4Az&A(┐AbVA(@Ab%A–{AbHA(`AbHA(|AbHA–|AbjA(}Ab9A(}AbjA(~Ab9A(~AbjA(•AbjA(~Ab9A(•AbjA(…AbNA(…Ab9A(…AbjA–ÂAb9A(£Ab9A7ïAb9A(»AbNA–¿AbNA–∩AbNA(¿AbNA–╗Ab9A(╗AbNA(┐AbNA(§AbNA–┐AbGA(έAbMA(|A)4A4OI3EA4PI3PIΚ)I3)A42I32A4IIHAA4“IA−A)wAbzA(έAb–A(σAb"A(εAb%A–üAb"A–ñAb"A–РAb"A(РAbqA(уAb"A(РAb"A(уAb"A(сAbqAzкAbqA–иAbqA–йAbqA–®AbqA)AAbqA)AAb5A5AAbqA5bAb5A)bAbqA)bAb5A5EAb5A)EAb–A)EAb5A)/Ab5A)OAb5A)/Ab5A)/Ab–A)1Ab–A)bAb[A)jAb$A(5AYHA4AIHAA4KI3KwA)I3)A4)I3PA46I3OA4KI4%A(]Ab¢A(2Ab'A7[Ab+A(]Ab'A(]Ab+A–.Ab+A(KAb;AzKAb+A–3Ab+A–3Ab;A(3AbXA(HAb*A4иA7όA4IIHAA4[I3Kb4)I3)A4PI3[A4EIHAA4;IA>A($Ab*A(7AbjA(XAbLA(LAbXA–DAbXA–;AbXA(DAbXA(;AbLA(;AbXA(+AbLA(+AbXA('AbMA–'AbXA(:AbMA–zAbMA(“AbMA(zAbXA(“AbXA–”AbMA(€AbMA(€AbBA(€AbXA($AbMA($AbBA(¢AbBA(¢AbMA(−AbBA–−AbMA(_AbMA(QAbMA7VAbBA(VAb7A(VAbBA(YAbBA–!Ab7A(!AbBA(!Ab7A(#Ab7A(#AbBA(&AbBA7*Ab7A(*AbHA(ZAb+A(¢A)]A41I3/A4PI3PAÂ)I3)A4.I3RA4AIHAA(6Az*A(╗AbYA(?Ab%A(^AbHA(^AbjA(`AbjA({AbjA(|Ab9A(|AbjA–}AbjA(|AbjA(}AbjA(•AbjA(~AbjA(•AbjA(…Ab9A(•AbjA–ÂAb9A–ÂAbjA(£Ab9A(ïAbNA–£Ab9A(»AbNA7¿AbNA(¿Ab9A(∩Ab9A(╗AbNA(∩AbNA–┐AbNA–┐Ab9A(§AbNA(§AbGA(§AbNA–ΚAb9A4KI3RA46I30IV)I3)A42I32A4IIHAA4“IA_A)wAb“A(έAb–A(σAb%A(εAb"A(εAb%A(εAb"A(ñAb"A(üAb%A7ñAb"A(РAbqA(уAb"A–сAbqA(кAbqA(сAb"A(сAbqA(кAbqA(кAb"A7иAbqA(йAbqA–®Ab5A)AAb5A)IAbqA)AAbqA5IAb5A)bAb5A)bAb–A)bAb5A)EAb–A)wAb5A)/Ab5A)/Ab–A)/Ab5A)OAb–A5/Ab5A51Ab–A)wAb.A)NAbzA(:AzQA4AIHAA4KI3RbÂ)I3)A4)I3PA40I3wA4–I4BA(KAbQA()Ab;A(PAb'A(2Ab+A72Ab'A([Ab'A([Ab+A(]Ab+A(.Ab+AzKAb+A7RAb+A(3Ab+A(3Ab;A(RAbDA(9AbYA(bA–кA4wIHAA42I3.bA)I3)A4PI3[A4EIHAA4;IA>A(”Ab*A(HAbHA–XAbLA(XAbDA(LAbLA(DAbXA(DAbLA–;AbXA(;AbLA(+AbLA(+AbXA(+AbLA('AbXA('AbLA(:AbLA(zAbXA(:AbXA–“AbMA–“AbXA–“AbMA(”AbXA(”AbMA($AbBA(€AbXA($AbMA–¢AbMA–−AbMA7_AbBA–QAbBA(VAb7A(VAbBA(YAbMA(YAbBA–!Ab7A–!AbBA(#AbBA(#Ab7A(&Ab7A–*Ab7A(&Ab7A(*Ab7A(?AbDA(YAb–A44I36A4(I3(A@)I3)A4.I3RA4AIHAA(4Az*A(╗AbVA(>AbGA(ZAb7A–`AbHA–`AbjA({AbjA–|AbjA–}AbjA7~AbjA–•Ab9A(…Ab9A(…AbjA(ÂAb9A(ÂAbjA7£Ab9A(ïAbNA–»AbNA(¿AbNA–¿Ab9A–∩AbNA–∩Ab9A(╗AbNA(┐AbGA(╗AbNA–┐AbNA(§AbGA(×AbNA(×AbGA(μAbBA4qI4GA41I3OA4PI3PIH)I3)A42I32A4bIHAA4zIA−A)bAbzA(έAb3A(σAb"A(σAb%A(εAb%A(εAb"A(εAb%A(üAb"A7ñAb"A–РAb"A(уAb"A–уAbqA(кAbqA(сAbqA(сAb"A(иAb"A(иAbqA(иAb"A(иAbqA(йAb5A(йAbqA7®AbqA)AAbqA5IAb5A)bAb5A)bAbqA)bAb5A)wAb5A)bAb5A)wAb–A5EAb5A)/Ab5A)OAb5ABOAb–A)1Ab5A)wAbKA)%Ab:A(QAz>A4AIHAA4KI3KbV)I3)A4PI32A41IHIA4"I4:A(KAb#A((AbDA(PAb:A(PAb'A(2Ab+A(PAb'A–2Ab'A([Ab'A(]Ab+A(]Ab'A(]Ab+A(.Ab'A(KAb'A(KAb;A–.Ab+A(RAb;A–RAb+A–3Ab;A(3AbDA(NAbQA(OA5/A4EIHAA42I3]Iε)I3)A4PI3[A4EIHAA4;IA>A(”Ab*A(HAbjA(MAbLA(XAbXA(XAbLA(LAbXA7DAbLA(;AbXA(DAbLA–;AbLA(+AbLA–'AbXA(:AbXA–:AbMA–:AbXA(zAbXA7“AbXA7€AbMA(€AbBA($AbMA(¢AbBA($AbMA(−AbBA(¢AbMA(−AbMA(−AbBA–_AbMA–QAbBA(VAb7A7YAbBA–!Ab7A(YAbBA–!Ab7A(!AbBA(&Ab7A(*Ab7A(&Ab7A(*Ab7A(<Ab7A(>AbXA(&Ab9A42I3[A44I36AV)I3)A4.I3RA4AIHAA(6Az*A(╗AbYA(>AbGA(ZAbHA(^AbjA(`AbHA({AbjA(`AbHA({AbjA7|AbjA–}AbjA(~Ab9A(~AbjA(•AbjA(…Ab9A(…AbjA(…Ab9A–…AbjA(ÂAb9A7£Ab9A(ïAb9A–»AbNA–»Ab9A–¿AbNA(¿Ab9A–∩AbNA(╗AbNA(╗Ab9A(┐AbNA(╗AbNA(┐AbNA(§AbNA(×AbNA(ΚAbNA(┐AbqA(εAb:A4XIA:A4EIHIA4PI32I4)I3)A42I32A4bIHAA4zIA_A)IAb“A(μAbRA(όAb"A(όAb%A(σAb"A(εAb%A(εAb"A–üAb"A(üAb%A–ñAb"A(РAb"A(РAbqA(РAb"A–уAb"A–сAbqA(сAb"A(кAb"A7иAbqA(йAbqA(йAb5A–®Ab5A(®AbqA)AAb5A5IAb5A)IAbqABbAb5A)wAb–A)wAb5A)EAb5A5/Ab5AB/Ab–A51Ab5A)EAbKA)"Ab+A(>A7~A4AIHAA4KI3KbH)I3)A4PI32A4OIHAA49IA_A(KAb*A(4AbXA()Ab'A((Ab:A()Ab'A(PAb'A(PAb+A(PAb'A(2Ab'A–[Ab'A(]Ab+A(]Ab'A(.Ab+A–]Ab+A(KAb+A–RAb+A(KAb+A(RAb;A(RAb+A(3Ab'A(–Ab;A(3AbDA(NAb−A(4A)PA4OIHAA4PI3[IΚ)I3)A4PI3[A4EIHAA4;IA>A(€Ab*A(jAbHA(BAbDA(MAbLA(XAbXA7LAbLA–DAbXA–DAbLA(+AbXA–;AbLA('AbXA(:AbMA('AbMA('AbXA(zAbXA–zAbMA(zAbXA–“AbXA–“AbMA(”AbXA–€AbMA($AbBA–$AbMA(¢AbMA(¢AbBA(_AbBA(−AbBA–_AbBA(QAbBA7VAbBA–YAbMA(YAb7A(!Ab7A(!AbBA–!Ab7A(#Ab7A–&Ab7A(&AbBA(*Ab7A(<Ab7A(=AbBA(=AbXA4KI3–A46I31A:)I3)A4.I3RA4AIHAA(6Az*A(∩AbVA(>Ab%A(`AbHA(`AbjA(^AbHA(`AbHA({AbjA(`AbHA–{AbjA(|AbjA({AbjA(}Ab9A(}AbjA(~AbHA(~AbjA7•AbjA–…Ab9A(ÂAb9A(£Ab9A(ÂAbjA7£Ab9A(ïAb9A(ïAbNA(¿AbNA–¿Ab9A(¿AbGA(∩AbGA(∩AbNA(╗AbGA(╗AbNA(┐AbNA(§AbNA(┐AbNA(§AbGA(×AbGA(×AbNA(×AbGA(╗Ab–A(РAb€A4:IA_A4bIHAA42I32IA)I3)A42I32A4bIHAA4zIA_A)AAb”A(μAb3A(κAb%A(σAb"A(όAb%A(σAb%A–εAb"A–üAb"A(ñAb"A(üAb"A(ñAb"A(ñAb%A(РAb"A7уAb"A–сAbqA(сAb"A(кAb"A–кAbqA(иAb5A–йAbqA5AAb5A(®AbqA)AAbqA)AAb5A5IAb5A)bAb5A)wAb–ABwAb5A)EAb–A5/Ab–A)OAb–A)OAb5A)/Ab5A51Ab–A)/AbRA)5AbDA(}A7╗A4AIHAA4.I3.b4)I3)A4PI3[A4/IHAA47IA=A(KAb*A(0AbXA(4Ab:A–(Ab'A()Ab:A(PAb+A(PAb'A(2Ab'A(PAb'A(2Ab:A(2Ab'A([Ab'A–]Ab+A7.Ab+A(KAb+A–.Ab+A(RAb+A(3Ab+A(3Ab;A(3Ab+A(–Ab+A(3AbDA(%Ab¢A(2A)3A40I3EA4PI3PIÂ)I3)A4PI3[A4EIHAA4;IA>A(”Ab*A(9AbHA(MAbLA(XAbLA(MAbLA(XAbLA(XAbXA(LAbLA(XAbLA(DAbXA7DAbLA(;AbXA7+AbXA–+AbLA7:AbXA(zAbMA(“AbXA(“AbMA(“AbXA(”AbXA–”AbMA(€AbXA(€AbMA($AbMA(¢AbMA(¢AbBA–¢AbMA(_AbMA–_AbBA–_AbMA(QAbBA7VAbBA(!AbBA7!Ab7A7#Ab7A(&Ab7A(&AbBA7*Ab7A(*AbHA(ZAb+A45I4NA41I3/A4PI3PA3)I3)A4.I3RA4AIHAA(4Az*A(╗AbYA(>Ab%A–ZAbHA(ZAbjA(^AbjA(^AbHA(`AbHA({AbHA(|AbjA({AbjA(|AbjA–}AbjA(}AbHA–~AbjA(~Ab9A(•AbjA–…Ab9A(…AbjA(ÂAb9A–£Ab9A–£AbNA–ïAb9A(ïAbNA(»AbNA–»Ab9A(¿AbNA–∩AbNA(∩Ab9A(╗AbGA–╗AbNA7§AbNA(×AbGA(×AbNA(∩Ab5A(сAb¢A4−IA<A4AIHAA42I3[Aε)I3)A42I32A4bIHAA4zIA−A)IAbzA(ηAb–A(κAb%A–σAb"A(σAb%A(εAb"A(σAb"A–εAb"A(üAb"A7ñAb"A–РAb"A(уAbqA–уAb"A–сAbqA7кAbqA(иAb"A(иAbqA7йAbqA–®AbqA)AAbqA)IAbqA5IAb5A)bAb5A)wAb5A)wAb–A5wAb5A5EAb–A)EAb5A5/Ab–A)OAb5A)1Ab–A)OAb5A)/AbRA)3AbXA(¿A–μA4AIHAA4]I3.bA)I3)A4PI3[A4/IHAA47IA=A(RAb*A(0AbXA(4Ab:A((Ab'A((Ab:A((Ab'A(PAb'A()Ab:A–PAb+A(2Ab'A([Ab'A(2Ab+A([Ab+A([Ab'A7]Ab'A(.Ab'A(.Ab+A(.Ab'A(KAb'A(KAb+A(RAb+A(3Ab;A(RAb+A(–Ab;A(%Ab€A(2A)3A40I3EA4PI3PIÂ)I3)A4PI3[A4EIHAA4DIA>A(“Ab*A(jAbjA(BAbLA(BAbDA(MAbLA(MAbDA–XAbLA–LAbXA(LAbLA(DAbLA(DAbXA(+AbXA–;AbXA–'AbMA('AbLA(:AbXA(:AbMA('AbXA(:AbXA(zAbMA(zAbXA–“AbXA–”AbMA–€AbMA($AbMA($AbBA(¢AbMA($AbMA(¢AbBA(¢AbMA(−AbMA(−AbBA(_AbBA(QAb7A–QAbBA(VAbBA–VAb7A–YAbBA7!AbBA7#AbBA(&Ab7A–*Ab7A(*AbHA(@Ab'A45I4NA41I3/A4PI3PA3)I3)A4.I3RA4AIHAA(6Az<A(¿Ab!A(=Ab%A(@AbHA–^AbjA(^AbHA(^AbjA–`AbHA({AbjA(|AbjA({AbHA–|AbjA–}AbjA(}AbHA(~Ab9A(~AbjA(•Ab9A(…Ab9A(•AbjA(ÂAb9A(…AbjA(ÂAb9A(£Ab9A(ÂAb9A(£Ab9A7ïAb9A–»Ab9A–¿AbNA–∩AbNA(╗AbNA(╗Ab9A–┐AbNA(§AbGA–§AbNA(×AbNA(§AbNA(¿Ab–A(иAb_A4&Aε|A4AIHAA42I3[AΚ)I3)A42I32A4bIHAA4zIA−A)IAbzA(ηAb3A(κAb%A7όAb%A(σAb"A(εAb"A(üAb"A(εAb"A(üAb"A(üAb%A–ñAb"A7РAb"A(уAb"A–уAbqA(уAb"A(сAb"A7кAbqAzиAbqA(®AbqA)AAb5A)AAbqA)AAb5A“IAb5A)bAbqA)wAb5A5wAb–A)EAb5A)/Ab5A)EAb–A5OAb5A5OAb–A)1Ab–A)OAb3A)KAb7A(αA–ñA4AIHAA4[I3]IΚ)I3)A4PI3[A4/IHAA4LAε~A(KAb*A(0AbXA(4Ab'A(4Ab:A(4Ab'A((Ab'A((Ab:A()Ab'A(PAb'A()Ab:A(PAb+A(2Ab'A(PAb'A(2Ab'A–[Ab'A(]Ab'A(]Ab+A–]Ab'A(.Ab+A(KAb'A(.Ab+A(KAb;AzRAb+A(3Ab;A("Ab”A(]A)NA44I30A4)I3(I@)I3)A4PI3[A4EIHAA4;IA>A(“Ab*A(NAbHA–7AbLA(BAbDA(MAbLA7XAbLA(LAbXA(LAbLA(LAbXA(DAbLA(;AbLA7;AbXA7+AbXA7:AbXA(zAbXA(zAbMA–zAbXA(“AbMA(“AbXA(”AbXA(€AbMA(€AbBA(€AbMA($AbMA(¢AbMA–¢AbBA7−AbBA(_AbBA(QAbBA–VAb7AzVAbBA(YAb7A(!AbBA(#Ab7A(!Ab7A(#AbBA(!AbBA7&Ab7A(*Ab7A(&AbjA(`Ab”A4NI4XA4OI3wA4PI3PA4)I3)A4.I3RA4AIHAA(0Az*A(¿AbYA(<Ab%A(?AbHA(ZAbHA–ZAbjA(ZAbHA–^AbHA(`AbHA({AbjA(|AbjA7|AbHA(}Ab9A–}AbjA–~AbjA(•AbjA(…Ab9A(ÂAb9A(…AbjA(…Ab9A(…AbjA(ÂAbjA–£AbNA7ïAb9A(»Ab9A–¿AbNA(»AbNA–∩AbNA(╗AbNA(∩AbNA–┐AbNA(§AbNA(┐Ab9A–§AbNA(¿Ab–A(иAb_A4&Aε|A4AIHAA42I3[AΚ)I3)A42I32A4bIHAA4zIA_A(®Ab“A(ηAb3A(όAb"A(κAb%A7όAb%A(όAb"A(σAb%A–εAb"A(üAb"A–üAb%A7ñAb"A(РAbqA(уAbqA(уAb"A(сAb"A(уAbqA(сAbqA(кAb5A(кAbqA(иAbqA(кAb"A(иAb5A–йAbqA)AAb5A(®AbqA5AAb5A)IAbqA)IAb5A)IAbqA)IAb5A)bAb5A)wAb–A)wAb5A)EAb5A)EAbqA)EAb5A)/Ab–A)/Ab5A)OAb5A)OAb–A)OAb5A)/AbRA)KAbBA(ΚA–ñA4AIHAA4[I3]IΚ)I3)A4PI3[A4/IHAA4LAε}A(KAb*A(/AbLA(0Ab:A(6Ab:A(4Ab'A(4Ab:A(4Ab'A((Ab:A()Ab'A()Ab:A()Ab'A(PAb+A(2Ab+A–2Ab'A7[Ab'A–[Ab+A7.Ab+A–KAb+A–RAb+A(3Ab+A(3Ab;A(qAb“A(]A)9A44I30A4)I3(I@)I3)A4PI3[A4EIHAA4DIA>A(zAb*A(NAbHA77AbDA(BAbDA7MAbLA(LAbLA(XAbLA(LAbLA(DAbLA(DAbXA(;AbLA(;AbXA7+AbXA(+AbMA('AbMA–'AbXA(:AbXA(zAbMA–zAbXA(“AbXA–“AbMA(€AbMA(€AbBA–$AbMA(€AbMA($AbMA7¢AbMA(−AbMA(−AbBA7_AbBA(VAbBA(VAbMA(QAbMA(VAbBA(YAbBA(YAb7A(YAbBA(!Ab7A(!AbBA–#Ab7A(&AbBA(*Ab7A(&AbBA(#AbHA(`Ab”A4NI4XA4OI3wA4PI3PA4)I3)A4.I3RA4AIHAA(0Az<A(»Ab!A(<AbGA(?Ab7A–ZAbHA(@AbHA–ZAbHA(^AbjA(^AbHA(`AbjA(`AbHA({AbjAz|AbjA–~AbjA(•Ab9A(•AbjA(•Ab9A(•AbjA(…Ab9A–ÂAb9A–£AbNA–£Ab9A–ïAbNA(»AbNA(»Ab9A(»AbNA(»Ab9A–∩AbNA(¿AbNA–╗AbNA–┐AbGA(§AbGA(┐AbNA–§AbNA(¿Ab3A(йAbQA4ZAε¿A4AIHAA4[I3]AÂ)I3)A42I32A4bIHAA4zIA_A(®Ab“A(αAb5A(ρAbGA7κAb%A–όAb%A(σAb"A(εAb"A(εAb%A(εAb"A–üAb"A(ñAb%A(РAb%A–РAbqA–уAbqA(РAbqA(уAbqA–сAb"A7кAbqA(иAbqA–йAbqA(йAb5A(йAbqA–®AbqA)AAbqA5IAb5A)IAbqABbAb5A)wAb5A)EAb5A5EAb–A)EAb5A)/Ab5A)/Ab–A)OAb5A)1Ab–A)/Ab3A)[AbHA(όA(®A4bIHIA42I32IÂ)I3)A4PI3[A4/IHAA4LAε~A(KAb*A(/AbXA(0Ab:A(6Ab:A(4Ab:A(6Ab:A((Ab'A(4Ab'A((Ab'A()Ab:A7)Ab'A(2Ab'A(2Ab+A([Ab+A([Ab'A([Ab+A(]Ab+A(]Ab'A–]Ab+A(]Ab'A(.Ab'A(KAb+A(KAb'A(KAb+A(RAb+A(3Ab;A(3Ab+A(qAbzA(RAbMA4PI32A4(I34IV)I3)A4PI3[A4EIHAA4DIA>A(zAb*A(9AbjA(HAbLA(7AbDA7BAbLA7MAbLA(XAbLA(LAbDA–LAbLA(DAbXA(;AbXA–;AbLAz+AbXA('AbXA(:AbMA('AbXA(:AbXA–zAbXA–“AbMA–“AbXA(€AbMA(€AbXA–€AbMA–¢AbMAz−AbBA(_AbBA(QAbBA(_AbBA–QAbBA(VAb7A–YAbBA(YAb7A7!AbBA(&Ab7A(#Ab7A7&Ab7A(!Ab9A(}Ab$A4BIA“A4/IHIA4PI32A4.I3RA4AIHAA(0Az*A(»Ab!A(=AbGAz@AbHA(ZAbHA(@AbHA(ZAb7A(^AbjA–`AbHA–{AbjA(|AbHA7|AbjA–}AbjA(~AbjA7•AbjA(…AbjA(ÂAbjAzÂAb9A(£Ab9A(ïAb9A(»AbNA–ïAb9A(»Ab9A(¿Ab9A–¿AbNA(╗AbNA(∩AbNA(╗AbNA(┐AbGA(┐AbNA(§AbGA(┐AbNA(§AbNA(×AbNA(¿Ab3A(®AbYA4…AΚμA4AIHAA4[I3]A@)I3)A42I32A4bIHAA4zIA_A(йAb”A(αAb3A(έAb%A(ρAb%A7κAb%A(όAb"A(όAb%A(όAb"A–σAb%A(εAb"AzüAb"A–РAb"A(ñAb"A(РAb"A(уAb"A7сAb"A(кAb"A(сAb"A(кAb"A(иAbqA(иAb"A–йAbqA(®Ab5A)AAb5A–®AbqA)AAb5A)IAb5A“bAb5A5wAb5A)wAb–A)EAb–A)EAb5A)/Ab–A5OAb–A)EAb–A)[AbHA(όA)AA4bIHIA42I32I@)I3)A42I3]A4EIHAA4'Aε╗A(.Ab*A(EAbXA(0Ab:A(1AbzA(0Ab:A76Ab:A–4Ab:A(4Ab'A((Ab:A7)Ab'A(PAb'A–2Ab:A7[Ab+A([Ab'A(.Ab'A(.Ab+A(]Ab+A(.Ab+A(KAb+A(RAb;A(KAb'A(RAb+A(RAb'A(–AbzA(KAbXA4PI32A4(I34IV)I3)A4PI3[A4EIHAA4DIA>A(:Ab*A(NAbHA(HAbLA–7AbDA(7AbLA(BAbLA(MAbLA(MAbDA7XAbLA(LAbXA–DAbXA7DAbLA(DAbXA7+AbXA–'AbXA('AbLA–:AbMA(zAbMA(zAbLA–“AbXA(”AbMA–”AbXA–€AbMA–$AbMA(¢AbMA–−AbBA(_AbBA–−AbBA(_AbBA(QAbBA(VAbBA(QAbBA–VAbBA(YAbMA(VAbBA(YAb7A(!AbBA(#Ab7A(#AbBA(&Ab7A(#Ab7A(&AbBA(!AbNA(}Ab$A4BIA“A4/IHIA4PI32A4.I3RA4AIHAA(0Az*A(»AbYA(<Ab%A(>AbHA(?Ab7A–@AbHA(@Ab7A(ZAbjA(^AbjA(ZAbHA(^AbHAz`AbjA(|AbjA({AbjA(}AbjA(}AbHA(~Ab9A(}AbHA(~AbjA(~Ab9A(•Ab9A(•AbjA7…Ab9A(ÂAb9A–£Ab9A(ÂAbjA(£Ab9A–ïAb9A–»AbNA–¿AbNA7∩AbNA(╗AbGA–┐AbNA7§AbGA(»Ab3A(йAb!A4•AΚμA4AIHAA4[I3]A@)I3)A42I32A4bIHAA4zIA_A(йAb”A(αAb–A(έAbGA(ρAb%A(ρAbGA–κAb"A(όAb%A(σAb"A(σAb%A(όAb%A(σAb"A(εAb"A(εAb%A–üAb"AzñAb"A(РAb"AzуAb"A(сAbqA(кAbqA(сAb"A(кAbqA7иAbqA(йAbqA7®AbqA(®Ab5A)IAbqA)AAbqA)AAb5A)bAb5A)wAb–A)bAb–A)bAb5A)wAb5A)EAb5A)/Ab–A)EAb5A)/Ab5A)/Ab–A)OAb–A)EAb–A))Ab9A(уA)1A4OI3/A4PI3PIV)I3)A42I3]A4EIHAA4'Aε╗A(]Ab*A(wAbXA(1AbzA(0Ab'A–0Ab:A76Ab:A(4Ab:A(4Ab'AY)Ab'A(PAb'A(2Ab'A([Ab'A–[Ab+A([Ab'A(]Ab'A–]Ab+A–.Ab+A–KAb+A(RAb;A(RAb+A(5Ab:A(KAbXA4PI32A4(I34IV)I3)A4PI3[A4EIHAA4DIA>A(:Ab*A(NAbHA–HAbDA(7AbLA(BAbLA(7AbDA(BAbDA(MAbLA(BAbLA(MAbLA(XAbLA(MAbDA(MAbLA(LAbLA7DAbLA–;AbXA(;AbLA–+AbXA('AbXA(+AbLA(:AbXA–:AbMA(zAbMA–zAbXA–”AbMA–”AbXA–€AbMA($AbBA($AbMA(¢AbMAz−AbBA(−AbMA(_AbMA(_AbBA(QAbMA(VAbBA(QAbBA(VAbMA–YAbBA(!AbBA(!Ab7A(!AbBA(#Ab7A(#AbBA(#Ab7A(VAbNA(|Ab¢A4BIA“A4/IHIA4PI32A4.I3RA4AIHAA(1Az*A(ïAb!A(*AbNA(>Ab7A–?AbHA–?Ab7A(@AbHA(ZAbjA(^AbHA(^AbjA(^AbHA–`AbjA(`AbHA({AbjA–|AbjA({AbjAz}AbjA(~Ab9A–•AbjA(…AbjA–…Ab9A–ÂAb9A7£Ab9A(ïAb9A7»Ab9A(¿Ab9A(¿AbNA–¿Ab9A(∩AbNA–╗AbNA(╗Ab9A(┐AbNA(§AbNA(§AbGA(»Ab3A(®Ab!A4╗AÂуA4AIHAA4]I3.AV)I3)A42I32A4bIHAA4zIA_A(йAb”A(αAb3A(έAb%A(ρAb"A(ρAb%AzκAb%A(σAb"AzσAb%A(εAb"A(üAb"A–üAb%A–РAbqA(ñAb"A–РAb"A(уAbqA(сAbqA(уAbqA(кAbqA(сAb"A–кAbqA(йAbqA(иAbqA(йAb5A–йAbqA(®AbqA)AAb5A5AAbqA)IAb5A5AAbqA)bAb5A)wAb5A5wAb–A5wAb5A)EAb5A5/Ab–A)EAb–A))Ab9A(РA)1A4OI3/A4PI3PIV)I3)A42I3]A4EIHAA4'Aε┐A(]Ab*A(wAbXA(OAbzA(1Ab:A(0Ab:A(1AbzA(0Ab:A(6Ab:A(4Ab'A(4Ab:A(4Ab'A((Ab'A()Ab'A((Ab:A–)Ab'A(PAb+A(PAb'A72Ab'A–]Ab+A([Ab'A(]Ab'A(.Ab+A(KAb+A(.Ab'A–KAb'A(KAb+A(RAb+A(–Ab'A(5Ab:A4]I33A44I31I:)I3)A4PI3[A4EIHAA4DIA>A(:Ab*A(GAbHA(HAbDA(HAbLA–HAbDA(7AbDA(BAbDA–BAbLA–MAbLA(XAbDA(XAbLA(XAbDA–LAbLA(LAbXA(;AbXA–;AbLA(;AbXA(+AbXA(+AbLA(+AbXA(+AbLA('AbXA(:AbXA(:AbMA(:AbXA–zAbXA(“AbMA–”AbXA(”AbMA(€AbMA(€AbXA–$AbMA–¢AbMA(−AbBA(−AbMA(_AbMA(−AbBA(_AbMA–QAb7A(QAbBA(VAbBA(YAb7A(VAbBA(YAbBA(YAb7A(!Ab7A(#AbBA(!AbBA(#Ab7A(YAbNA(`Ab¢A47IA“A4/IHIA4PI32A4]I3RA4AIHAA(OAz<A(£Ab!A(*Ab%A(>AbHA(>Ab7A(?Ab7A(?AbHAz@AbHAz^AbHA(`AbjA({AbjA(|AbjA({AbjA–|AbjA(}AbjA(}AbHA(}AbjA(~Ab9A(•Ab9A(•AbjA(…AbjA(…Ab9A(ÂAb9A(ÂAbjA(…AbjAz£Ab9A(ïAb9A(»AbNA(ïAb9A(¿AbNA(»AbNA7∩AbNA7╗AbNA(┐AbGA(┐AbNA(§AbGA(»Ab3A(йAb!A4╗AÂуA4AIHAA4]I3.AV)I3)A42I32A4bIHAA4:IA_A(иAb”A(ΚAb3A(μAb%A7έAb%A(έAbGA(κAbGA–κAb%A–όAb%A–σAb%A(εAb"A–üAb"A–üAb%A–ñAb"A(РAb"A(РAbqA(уAb"A(уAbqA(уAb"A(сAbqA7сAb"A(иAbqA(йAb5A(йAbqA–иAbqA(®AbqA)AAb5A)AAbqA(®AbqA)AAb5A5IAb5A5bAb5A5bAbqA5wAb5A)EAb5A)EAb–A5/Ab–A)OAb–A)(AbGA(йA)4A44I34I:)I3)A42I3.A4wIHAA4“AΚρA([Ab*A(bAbXA–OAb:A(1Ab:A(1AbzA–0Ab:A(0AbzA(6AbzA(6Ab:A(4Ab:A(4Ab'A((Ab'A(0AbMA(5Ab*A4“AΚαA4AI:AA4┐Az@A(5Ab*A()AbMA([Ab+A(2Ab'A([Ab'A([Ab+A7]Ab+A(.Ab+A(KAb+A(.Ab'A(KAb+A(KAb'A(3Ab+A(3AbzA4]I33A44I31/Κ)I3)A4]I3RA4AIHAA4μAZjA(`Ab*A(€AbNA(−AbMA–QAbBA(_AbMA7VAbBA(YAb7A(YAbBA(!AbBA–!Ab7A(#Ab7A(YAbNA(`Ab−A47IA“A4/IHIA4PI32A4]I3RA4AIHAA(OAz*A(£Ab!A(&AbGA(=Ab7A–?AbHA(>Ab7A(?AbHA(@Ab7A–@AbHA(ZAbHA(@AbjA(|AbDA(&A).A40I31IV)I3)A4[I3]A4AIHAA4ZAΚ×A(σAb!A(}Ab–A(ïAbNA(ïAb9A(»Ab9A(»AbNA(»Ab9A7¿AbNA–╗AbNA(∩Ab9A(╗AbNA(§AbNA(┐AbNA(§AbNA(¿Ab3A(®Ab!A4μA£EA4AIHAA4]I3KE3)I3)A4.I3KA4AIHAA(&A7ïA)PAb'A(кAb3A)AAb5A5IAbqA)IAb–A)wAb–A)wAb5A)bAb5A)wAb–A)wAb5A)EAb–A)/Ab5A)/Ab–A)/Ab5A)4AbGA(иA)6A44I34I:)I3)A42I3.A4wIHAA4“AΚρA([Ab*A(bAbXA–/AbzA(OAb:A(OAb'A–1Ab:A70Ab:A(6Ab:A(4Ab:A(6Ab:A(0AbMA(qAb*A4”AΚαA4AI:AA4┐Az@A(qAb*A((AbXA(PAb'A(2Ab:A(2Ab'A([Ab+A(2Ab'A–[Ab'A(]Ab'A(KAb+A(KAb;A(.Ab'A(KAb'A(RAb:A(3Ab:A4]I33A44I31OA)I3)A4]I3KA4AIHAA4£A£6A(`Ab*A(”Ab%A(_AbBA–QAbMA(QAbBA(VAbBA(YAb7A(YAbBA(YAb7A(YAbBA(!AbBA(!Ab7A(VAbNA({Ab¢A4BIA“A4/IHIA4PI32A4]I3RA4AIHAA(OAz*A(ÂAb!A(#AbGAz>Ab7A(>AbHA(?AbHA(@AbHA(ZAbjA(@AbHA(ZAb9A(}AbDA(#A)KA40I31IÂ)I3)A42I3[A4AIHAA4−Aε@A(ρAbQA(~AbqA–ïAb9A7»Ab9A(¿AbNA(¿Ab9A–∩AbNA–╗AbNA(┐AbNA(┐Ab9A(»Ab3A(йAbYA4ηA£EA4AIHAA4]I3.EH)I3)A4KI3KA4AIHAA(¢A7`A)]Ab:A(кAbRA5AAbqA)IAb5A5bAb5A)wAb–A)bAbqA)wAb5A)EAb5A5/Ab–A)/Ab5A)(AbGA(кA)4A44I34IH)I3)A42I3.A4wIHAA4¢AΚиA(2Ab*A(bAbMA(/AbzA(/Ab:A(OAb:A(/AbzA(OAb:A–1Ab:A(0Ab:A(1Ab:A(6Ab:A(0AbzA(6Ab:A(1AbXA(3Ab*A4LAε|A4/IHAA4]I45A4AIHAA4ïAY¢A(qAb*A(4AbXA(2Ab'A–2Ab+A(2Ab'A([Ab+A([Ab'A(]Ab+A(]Ab'A7.Ab+A(KAb+A(RAb;A(5Ab$A4RI4GA46I3/A4)I3P/Κ)I3)A4]I3KA4AIHAA4£A£6A(^Ab*A(”AbGA(−AbMA(_AbBA–QAbBA(VAb7A–VAbBA7YAbBA(!AbBA(VAb9A(`Ab−A47IA“A4/IHIA4PI32A4]I3RA4AIHAA(OAz<A(ÂAb!A(#Ab%A(=Ab7A(>Ab7A(=Ab7A(>Ab7A7>AbHA(?AbHA–@AbjA(|AbDA(!A)KA40I31IΚ)I3)A42I32A4bIHAA4zIA!A(έAb−A(•Ab5A(ïAb9A(»AbNA(»Ab9A(¿Ab9A–¿AbNA(¿Ab9A–∩AbNA–╗AbNA(┐AbGA(┐AbNA(»Ab–A(иAbYA4üAZ2A4AIHAA4.I3KEH)I3)A4KI3RA4AIHAA(+Az&A).Ab“A(кAbKA)AAbqA)AAb5A)bAb5A)IAb5A)bAb5A)wAb5A)bAb5A)wAb5A)EAb–A)EAb5A)/Ab3A)6AbGA(сA)(A44I36IH)I3)A42I3.A4wIHAA4¢AΚиA(2Ab*A(IAbXA–EAbzA(/AbzA(/Ab:A–/AbzA(OAb:A(1Ab:A–0Ab:A–6Ab:A(1AbMA(3Ab*A4LAε|A4/IHAA4]I45A4AIHAA4£AY−A(qAb*A(4AbMA(PAb+A(PAb'A([Ab'A([Ab+A–2Ab'A7]Ab+A–.Ab+A–KAb;A(5Ab$A4RI4GA46I3/A4)I3P/Κ)I3)A4]I3KA4AIHAA4£A£6A(^Ab*A(”AbGA(−AbMA(−AbBA(_AbBA–QAbBA(VAbBA(QAbBA(QAbMA(YAbMA–YAbBA(VAb9A(^Ab−A47IA“A4/IHIA4PI32A4]I3RA4AIHAA(OAz*A(ÂAb!A(#AbGA–<Ab7A7=Ab7A(>Ab7A(>AbHA(?AbHA(@AbHA(?AbjA({AbDA(#A).A40I31Iε)I3)A4PI32A4wIHAA4LIA”A(λAb€A(•Ab"A(»Ab9A(ïAb9A–»AbNA(¿Ab9A(∩AbNA(∩AbGA7╗AbNA(┐AbNA(╗AbNA(ïAb–A(иAb!A4εAZ2A4AIHAA4.I3KEH)I3)A4KI3RA4AIHAA(+Az&A).Ab”A(сAbKA)AAb5A)IAb5A)AAb5A)AAbqA)IAbqA)IAb5A)bAbqA5wAb5A)EAb5A)EAb–A)4AbNA(сA)4A44I34IH)I3)A42I3.A4wIHAA4$AΚиA(PAb*A(AAbXA(EAbzA(/AbzA(EAbzA(/AbzA(/Ab:A(/AbzA(OAb:A(1Ab'A–1Ab:A–0Ab:A(/AbXA(RAb*A4LAε{A4/IHAA4]I45A4AIHAA4ÂAY¢A(5Ab*A(4AbXA()Ab:A(PAb'A(PAb:A–2Ab'A–[Ab'A(]Ab'A(.Ab+A(]Ab+A(.Ab+A(.Ab'A(KAb;A(5Ab$A4RI4GA46I3/A4)I3P/Â)I3)A4]I3KA4AIHAA4╗AZRA(ZAb*A(“AbNA($AbMA(¢AbMA(−AbMA(_AbBA(_AbMA(_AbBA(_AbMA–QAbBA(QAbMA(YAbBA(!Ab7A(VAbNA(^Ab−A47IA“A4/IHIA4PI32A4]I3RA4AIHAA(OAz*A(…Ab!A(!AbGA(<Ab7A(*Ab7A(<AbHA(=AbHA–=Ab7A(>AbHA(>Ab7A–?AbHA(`Ab;A(!A).A40I31bA)I3)A4PI3PA4/IHwA4jI4DA(×AbzA(ÂAb%A(ïAb9A–»AbNA(»Ab9A(¿AbNA(¿Ab9A(∩Ab9A–∩AbNA(╗AbNA(┐AbGA(ïAb3A(кAbYA4üAZ2A4AIHAA4.I3KE:)I3)A4KI3RA4AIHAA(jAz€A)RAb€A(кAbKA5AAbqA)AAb–A)IAb5A)IAbqA)bAb–A5bAbqA)wAb–A)wAb5A)6AbNA(сA)4A44I34I3)I3)A42I3KA4bIHAA4QA£0A()Ab*A(AAbXA–wAbzA(EAbzA(wAbzA–/AbzA–OAb:A(/AbzA(OAb:A(1AbzA(0Ab'A(OAbXA(]Ab*A4HIA*A4OIHAA4PI3[A4)I3)A4[I3RA4AIHAA4}AYDA(5Ab*A(6AbMA(PAb'A()Ab+A(PAb'A(PAb:A(2Ab+A([Ab'A(]Ab+A–[Ab'A–.Ab+A(KAb+A(]AbDA(qAbQA45I4XA40I3wA4PI3P/:)I3)A4]I3RA4AIHAA4σAY:A(?Ab*A(zAbNA(€AbMA(¢AbMA–¢AbBA(−AbMA–_AbBA(_AbMA(_AbBA7QAbBA(YAbBA(VAbBA(QAbNA(^Ab−A47IA“A4/IHIA4PI32A4]I3RA4AIHAA(OAz*A(…Ab!A(#AbGA–<Ab7A(<AbHA–=Ab7A7>Ab7A(>AbHA(?AbjA(`AbDA(!A)RA40I3ObA)I3)A4PI3PA4/IHwA4jI4LA(ΚAb:A(•AbGA(£Ab9A(ïAb9A(»Ab9A(ïAb9A(»AbNA7¿Ab9A(∩Ab9A(∩AbNA(╗AbGA(┐AbGA(£Ab5A(сAb!A4®AZ"A4AIHAA4.I3KEH)I3)A4KI3RA4AIHAA(jAz€A).Ab€A(уAbKA(®AbqA(®Ab5ABIAb5A5bAb5A)bAbqA)wAb5A)wAb–A)6AbGA(сA)4A44I34I3)I3)A42I3KA4bIHAA4VA£0A(PAb*A4®AbMA(bAbzA–wAbzA(EAb:A7EAbzA7OAbzA(OAb:A(1Ab:A(OAbLA(.Ab*A4HIA*A4OIHAA4PI3[A4)I3)A4[I3RA4AIHAA4}AYDA(qAb*A(6AbMA()Ab:A(PAb:A(PAb'A–2Ab'A(2Ab+A([Ab'A([Ab+A(]Ab'A(]Ab+A(.Ab'A(]Ab+A(]Ab;A(qAbQA45I4MA40I3wA4PI3P/3)I3)A4]I3RA4AIHAA4®AzZA(*Ab*A(:AbHA7€AbMA($AbMAz¢AbMA–−AbMA(_AbBA(_AbMA(QAbBA(QAbMA(VAbBA(YAb7A(QAb9A(^Ab¢A47IA“A4/IHIA4PI32A4]I3RA4AIHAA(/Az*A(•Ab!A(!AbGA(&Ab7A(*Ab7A7<Ab7A(=AbHA(=Ab7A(=AbHA(>Ab7A(?AbjA({AbDA(!A)KA40I31b4)I3)A4PI3PA41I3/A4"I49A(┐AbDA(ÂAbNA(£Ab9A(ïAbNA(ïAb9A–»Ab9A–¿AbNA(∩AbNA(¿Ab9A(∩Ab9A(╗AbGA(£Ab–A(сAb!A4®AZ%A4AIHAA4.I3KEH)I3)A4KI3RA4AIHAA(9Az€A)]Ab$A(уAbKA5AAb5A(®AbqA)AAbqA)IAbqA)IAb5A5bAb5A)wAb5A)bAb5A)0AbGA(уA)4A44I34I3)I3)A42I3KA4wIHAA4QA£6A((Ab*A4®AbXA7bAbzA(wAbzA(EAbzA(wAbzA(EAbzA(/AbzA–OAbzA(OAb:A(1Ab:A(EAbLA([Ab*A4HIA*A4OIHAA4PI3[A4)I3)A4[I3RA4AIHAA4}AYDA(qAb*A(6AbMA–)Ab'A(PAb'A(PAb:A–2Ab'A([Ab'A–2Ab'A([Ab'A(]Ab'A(]Ab+A(]AbDA(5AbQA45I4XA40I3wA4PI3PEε)I3)A4[I3.A4AIHAA([A–εA(VAb_A(:Ab7A(zAbXA–“AbMA(”AbXA(€AbMA(€AbBA($AbBA–$AbMA(¢AbMA–−AbBA(¢AbMA(_AbMA–_AbBA(QAbBA(VAbMA(−Ab7A(>Ab€A4GI4XA4OI3wA4PI3PA4)I3)A4]I3RA4AIHAA(EAz<A(~Ab&A(VAbNA7*Ab7A–<Ab7A–=Ab7A(>AbHA(=Ab7A(>AbHA(^Ab;A(YA)KA40I31b4)I3)A4PI3PA41I3/A4"I49A(┐AbDA(…Ab9A(ïAb9A(£Ab9A(»Ab9A–ïAb9A(»AbNA–¿AbNA(¿Ab9A(∩Ab9A(╗AbNA(ïAb–A(сAbYA4йAZ"A4AIHAA4.I3KE3)I3)A4KI3RA4AIHAA(;Az&A)2Ab€A(уAbRA(®Ab5A–®AbqA(®Ab5A)AAb5A)AAbqA)AAb5A)IAb5A)bAb5A)wAb5A)bAb5A)1AbGA(РA)(A44I36I4)I3)A42I3KA4bIHAA4#AZRA((Ab*A4йAbLA(IAb“A(bAbzA(bAb:A(bAbzA–wAbzA7EAbzA(EAb:A–/Ab:A(/AbDA(PAb*A4GIA−A41IHAA4PI32AH)I3)A4[I3KA4IIHAA4ZAZ"A(5Ab*A(1AbMA–)Ab'A()Ab+A7PAb'A([Ab+A(2Ab'A([Ab'A–]Ab+A(.Ab+A([AbLA("Ab#A4GIAzA41IHIA4PI32E@)I3)A42I3[A4EIHAA("A)OA(¢Ab€A(:Ab7A(zAbXA(zAbMA(“AbXA(”AbMA–“AbXA7€AbMA($AbMA(€AbXA($AbMA(¢AbBA–−AbBA–−AbMA(_AbMA(_AbBA(QAb7A(−AbHA(=Ab€A4GI4XA4OI3wA4PI3PA4)I3)A4]I3RA4AIHAA(EAz<A(}Ab#A(YAbGA(&Ab7A(*Ab7A(&AbBA(*AbBA–<Ab7A(=AbHA(<Ab7A–>AbHA(`Ab;A(YA)KA40I31b4)I3)A4PI3PA41I3/A4"I49A(∩Ab;A(…AbNA(ÂAbjA(£Ab9A(ïAb9A–ïAbNA(»Ab9A(¿AbNA(»Ab9A(¿Ab9A(∩Ab9A(∩AbNA(∩Ab9A(ïAb5A(сAbVA(OAYLA4AIHAA4.I3RE4)I3)A4KI3RA4AIHAA(DAz&A)2Ab€A(РAbRA7йAbqA(®AbqA)AAbqA5AAb5A)AAbqA5IAb5A)bAb5A)OAbNA(РA)(A44I36I4)I3)A42I3KA4bIHAA4#AZRA(4Ab*A4иAbLA(AAb“A(IAbzA(bAbzA(bAb:A–bAb“A7wAbzA(/AbzA(/Ab:A(/AbzA(EAbDA(PAb*A4GIA−A41IHAA4PI32AH)I3)A4[I3RA4IIHAA4@AZ%A(3Ab*A(0AbMA()Ab'A((Ab:A–)Ab'A(PAb'A–2Ab'A([Ab'A([Ab+A([Ab'A–]Ab+A(2AbLA("Ab&A4GIAzA41IHIA4PI32EH)I3)A4(I34A4)I3(A(MAbjA(zAb+A(+AbXA–'AbXA(:AbXA–zAbMA(zAbXA(zAbMA(”AbMA(”AbXA(“AbXA(”AbMA7€AbMA–$AbMA–¢AbMA(−AbBA(−AbMA(−AbBA–_AbMA(−Ab7A(<Ab€A4GI4XA4OI3wA4PI3PA4)I3)A4]I3RA4AIHAA(EAz*A(}Ab#A(VAbNA(#AbBA–*Ab7A(&AbBA–<Ab7A(*Ab7A–<Ab7A(=AbHA(^Ab;A(QA)KA40I3Ob3)I3)A4)I3PA40I31A4RI45A(ïAbMA(…AbjA7£Ab9A(ïAb9A(»AbNA–»Ab9A(¿Ab9A(¿AbNA–∩AbNA(£Ab–A(уAbVA(OAYLA4AIHAA4.I3REA)I3)A4.I3KA4AIHAA(”A7{A))AbzA(ñAb3A(кAb"A(йAbqA–иAbqA–йAbqA(®AbqA)AAb5A5AAbqA)bAb5A)bAb–A)OAbNA(ñA)(A44I36I4)I3)A42I3KA4bIHAA4!AZRA(6Ab*A4иAbXA4®AbzA(IAbzA(IAb“A(AAbzA(bAb“A(wAb:A–bAbzA(wAbzA(wAb“A–/Ab:A(EAb;A()Ab*A4GIA−A41IHAA4PI32AH)I3)A4[I3KA4IIHAA4@AZ"A(5Ab*A(0AbXA–4Ab:A((Ab'A()Ab'A(PAb'A(2Ab+A(PAb:A–2Ab'A–[Ab+A(]Ab+A(PAbLA(5Ab&A4%IAzA41IHIA4PI32EA)I3)A4)I3PA46I3OA4KI4qA(:Ab'A–;AbXA7+AbXA('AbXA7:AbXA(zAbXA(“AbXA–zAbXA–”AbXA–”AbMA(€AbMA($AbBA7$AbMA–¢AbMA(−AbMA(_AbMA(_Ab7A(&Ab'A45I4NA40I3/A4PI3PA3)I3)A4]I3RA4AIHAA(EAz*A(}Ab!A(VAbNA–#AbBA–*Ab7A(&Ab7A(*AbBA–<Ab7A–=AbHA(^Ab;A(VA)KA40I3Ob3)I3)A4)I3PA40I31A4RI45A(»AbBA(ÂAbjA(£Ab9A(ÂAbjA–£Ab9A(»AbNA(»Ab9A(ïAb9A(»Ab9A–»AbNA(∩AbNA(£Ab–A(РAbVA(/AYLA4AIHAA4.I3Rwε)I3)A4.I3KA4AIHAA(YA7ïA)0Ab:A(РAb–A(кAbqA7иAbqA–йAbqAY®AbqA)AAbqA)IAb–A)/AbNA(ñA)(A44I36IA)I3)A4[I3RA4bIHAA4<AZHA(0Ab*A4кAbLA4®Ab“A(AAb“A(AAbzA(AAb“A(IAbzA(IAb“A(IAbzA(wAbzA(bAbzA(wAbzA–EAb:A(wAb+A(4Ab&A4qI4+A40IHbA4PI3PAV)I3)A4[I3KA4IIHAA4<A£PA(5Ab*A(1AbMA(4Ab'A((Ab'A–)Ab'A(PAb'A()Ab'A(PAb'A(2Ab'A–[Ab'A([Ab+A([Ab'A(2AbXA("Ab*A4jIAVA4OIHAA4PI32w@)I3)A4PI32A4/IHAA47IA¢A(”Ab#A(BAbBA(LAbLA(;AbXA7;AbLA(+AbLA(+AbXA('AbXA('AbLA(:AbXA('AbXA–:AbXA–zAbMA(zAbXA(”AbXA(”AbMA–”AbXA–€AbMA($AbBA(¢AbBA($AbMA(−AbMA(−AbBA(_AbMA(VAbLA4.I3–A46I31A:)I3)A4]I3RA4AIHAA(EAz<A(}Ab#A(VAbGA–#AbBA(#Ab7A(*AbBA(*Ab7A(&Ab7A(*AbBA(<AbHA(=Ab7A(<AbHA(^AbDA(VA)KA40I31b3)I3)A4)I3PA40I31A4RI45A(£AbBA(…AbjA(ÂAb9A(ÂAbjA(ÂAb9A–£Ab9A–»AbNA(»Ab9A–¿AbNA(¿Ab9A(ÂAb5A(ñAbYA(/AYDA4AIHAA4.I3RI:)I3)A4.I3KA4AIHAA('A7•A(иAb”A(αAb5A–μAbGA7ρAb%A–κAb%A(όAb%A(σAb"A(όAb%A(σAb"A7εAb"A(εAb%A(üAb"A–ñAb"A–РAbqA(уAb"A(уAbqA–сAbqA7кAbqA–кAb5A–иAbqA(йAbqA(®AbqA(йAbqA7®AbqA)IAb–A)/AbNA(üA)(A44I36IA)I3)A4[I3RA4bIHAA4<AZHA(0Ab*A4кAbXA4®AbzA4®Ab“A–AAbzA–IAb“A7bAbzA–wAb:A(EAb:A(wAb+A(4Ab&A4qI4+A40IHbA4PI3PAV)I3)A4[I3KA4IIHAA4*A£2A(–Ab*A(0AbBA7(Ab'A()Ab'A()Ab:A(PAb'A()Ab:A(2Ab'A(PAb'A–2Ab'A([Ab'A(PAbMA("Ab*A4jIAVA4OIHAA4PI32w:)I3)A42I3[A4wIHAA4:Aε{A($Ab*A(HAbHA(LAbLA–XAbLA(DAbLA(LAbLA(;AbXA(;AbLA(+AbXA('AbXA(+AbMA(+AbXA('AbXA7:AbXA7zAbMA–“AbMA(”AbMA(”AbXA–€AbMA($AbBA(¢AbMA($AbMA(¢AbMA($AbXA(_AbMA(QAbLA4.I3–A46I31A:)I3)A4]I3RA4AIHAA(EAz*A(|Ab#A(_Ab9A7#Ab7A(&Ab7A(*AbHAz*Ab7A(<AbHA(@Ab;A(QA)KA40I31b3)I3)A4)I3PA40I31A4RI45A(ïAbMA–…AbjA(ÂAb9A(£Ab9A(ÂAbjA(£Ab9A(ïAb9A(ïAbNA(»Ab9A(ïAb9A(»AbNA(¿AbNA(ÂAbqA(ñAbYA(/AYLA4AIHAA4.I3RI4)I3)A4[I3]A4AIHAA(<A–сA(ñAb;A(λAb"A–μAb%A7μAbGAzρAb%A–κAb%A(όAb%A(σAb"A(όAb%A(όAb"A(σAb%A(εAb"A7üAb"A(üAb%A(ñAb"A(ñAb%A(уAbqA–РAb"A(уAbqA(уAb"A(уAbqA(кAbqA–кAb5A(кAbqA–иAbqA–®AbqA(йAbqA(®Ab5A(йAb5A)OAbHA(όA)0A4OI3/A4PI3PIA)I3)A42I3RA4bIHAA4<AZHA(1Ab*A4кAbDA4йAb“A4йAbzA3®Ab“A(AAb“A(AAbzA–IAbzA(wAb:A(bAb“A(bAbzA(wAbzA(bAb;A(0Ab*A4qI4'A40IHbA4PI3PAV)I3)A4[I3KA4IIHAA4*A£2A(3Ab*A(OAbBA(4Ab:A(4Ab'A((Ab:A((Ab'A()Ab'A(PAb'A()Ab:A–PAb'A–2Ab'A(2Ab+A()AbXA(qAb*A4jIAVA4OIHAA4PI32w4)I3)A4[I3.A4AIHAA4*AΚРA($Ab*A(jAb9A(MAbLA(XAbLA–MAbLA–LAbLA(XAbLA–DAbXA(;AbXA(;AbLA(;AbXA(+AbLA–'AbXA('AbMA(:AbXA(zAbMA(:AbMA–zAbXA(:AbXA(zAbXA(“AbXA–€AbMA(”AbXA–€AbMA–$AbMA(_AbDA($AbHA42I3[A44I36AV)I3)A4]I3RA4AIHAA(wAz<A(|Ab#A(_AbNA7!AbBA–#AbBA–&Ab7A–*Ab7A(*AbjA(@Ab;A(QA).A40I31b3)I3)A4)I3PA40I31A4RI45A(£AbMA(•AbHA(•Ab9A(ÂAb9A(…Ab9A(ÂAb9A(£AbjA–£Ab9A(ïAbNA(»Ab9A(»AbNA(¿Ab9A(ÂAb5A(üAbYA(EAYDA4AIHAA4.I3RAε)I3)A4PI3PA4OI3EA(~A)(A(κAbMA(ΚAb%A(αAbNA(λAbGA(λAb%A(μAbGA(ηAbGA(ηAb%A(μAb%A(μAbGA(έAbGA–ρAb%A–κAb%A(κAb"A–κAb%A–σAb%A(εAb"A(σAb"A(εAb%A7üAb"A(ñAb"A(ñAb%A(РAbqA–РAb"A–уAb"A(сAbqAzкAbqA(иAbqA7йAbqA(®Ab5A(иAb5A)OAbHA(κA)6A4OI3/A4PI3PAε)I3)A4[I3RA4bIHAA4?AY“A(OAb*A4сAb;A3йAbzA4йAb“A4йAbzA4®Ab“A(AAb“A(AAbzA–AAb“A(IAb“A(bAbzA(bAb“A(IAb'A(1AbVA4RI47A46I3EA4)I3PAÂ)I3)A42I3.A4bIHAA4YA£wA(3Ab*A(OAbMA–4Ab:A(4Ab'A()Ab'A((Ab:A((Ab'A(PAb+A()Ab'A(PAb'A(2Ab+A([Ab'A(2Ab'A()AbBA(%Ab*A4MIA?A4/IHAA4PI3[bΚ)I3)A4[I3KA4AIHAA4}A£2A($Ab*A(NAbjA(7AbLA(7AbDA(BAbLA(BAbDA(MAbLA(BAbDA–XAbLA–LAbLA–DAbLA–DAbXA(+AbXA(;AbLA–+AbXA('AbXA(:AbLA–'AbXA–zAbMA(zAbXA–“AbMA(“AbXA(”AbMA(”AbXA(€AbXA($AbBA(−Ab+A(:AbqA44I36A4(I3(A@)I3)A4]I3RA4AIHAA(wAz*A(|Ab!A(_AbNA–!AbBA–!Ab7A(&AbBA(&Ab7A(#Ab7A(&Ab7A–*Ab7A(?Ab;A(_A)RA40I3Ob3)I3)A4)I3PA40I31A4RI45A(ÂAbMA7•AbjA(…Ab9AzÂAb9A(£Ab9A(ïAb9A(»Ab9A(»AbNA(…Ab–A(üAbYA(/AYDA4AIHAA4.I3RAΚ)I3)A4)I3(A46I36A(ïA)]A(ηAb7A(×AbGA–αAbGA7λAbGA(ηAb%A(ηAbGA(ηAb%A(μAb%A(μAbGA7έAb%A(ρAb%A(κAb"A–κAb%A(όAb"A(όAbGA–σAb%A(εAb"A(εAb%A–üAb"A(üAb%A7ñAb"A(РAb"A–уAbqA–сAb"A(сAbqA7кAbqA(иAbqA(йAb"A(иAbqA(кAb5A)OAbBA(ΚA)IA4bIHIA42I32IA)I3)A4[I3RA4bIHAA4?AYzA(/Ab*A4уAbDA3йAbzA4йAb“A4®Ab“A3®AbzA(AAbzA4®Ab“A(AAb“A–IAbzA(bAb:A(IAb'A(OAb!A4RI47A46I3EA4)I3PAÂ)I3)A42I3KA4bIHAA4YA£wA(3Ab*A(/AbMA(6Ab'A(4Ab'A(4Ab:A((Ab'A((Ab:A7)Ab'A(PAb'A72Ab'A()AbMA(%Ab*A4MIA?A4/IHAA4PI3[bV)I3)A4]I3RA4AIHAA4λAY−A(:Ab*A(GAb7A(HAbLA(HAbDA(HAb;A(7AbLA(BAbLA(7AbDA(BAbLA–MAbLA(MAbDA(XAbXA7LAbLA7DAbLA–;AbXA–+AbXA('AbLA('AbXA(:AbLA(:AbXA(:AbMA(:AbXA(zAbXA(zAbMA–“AbXA–”AbMA(€AbBA(_Ab:A(DA)KA40I3/A4PI3PAÂ)I3)A4]I3RA4AIHAA(bAz<A(`Ab#A(_AbNA–YAbMA(!Ab7A(#Ab7A(!Ab7A7&Ab7A(*Ab7A(*AbHA(?Ab+A(−A)KA40I31b3)I3)A4)I3PA40I31A4RI45A(£AbBA(•AbHA(~AbjA7…Ab9A(ÂAb9A(…AbjA(£AbNA(ÂAb9A(£AbjA(£Ab9A(£AbjA(…Ab5A(üAbYA(EAYDA4AIHAA4.I3RAÂ)I3)A44I34A4PI32A(╗Ab5A(αAbjA(ΚAb%A–αAbGA(αAbNA(αAbGA(αAbNA(λAbGA(ηAbGA(μAb%A(ηAb%A(ηAbGA7μAbGA(έAb%A–ρAb%A(ρAbGA(κAb%A–όAb%A(σAb%A–σAb"A–εAb"A–üAb"A(ñAbqA(ñAb"A–РAbqA(уAb"A–РAb"A–уAb"A(кAb"A(кAbqA(сAb"A(кAbqA(иAb5A(йAbqA(иAb5A)OAb7A(×A)bA4bIHIA42I32IA)I3)A4[I3RA4bIHAA4?AYzA(/Ab*A4уAbDAHиAb“A4йAbzA3йAb“A4®Ab“A(AAbzA(AAb“A–IAbzA(IAb“A(IAb'A(OAbYA4RI47A46I3EA4)I3PAÂ)I3)A42I3KA4bIHAA4VA£EA(RAb*A(OAbBA–6Ab'A(4Ab:A(4Ab'A(4Ab:A(4Ab'A((Ab'A()Ab+A()Ab:A(PAb:A(2Ab'A(PAb'A((AbMA("Ab*A4MIA?A4/IHAA4PI3[bH)I3)A4]I3RA4AIHAA4üAz~A(+Ab*A(%AbBA(9AbDA–jAbDA(jAbLA(7AbLA(7AbDA(HAbDA(BAbLA7BAbDA–MAbLA(XAbLA(XAbDA(XAbLA(LAbLA–DAbXA–;AbXA(;AbLA(+AbXA(+AbLA('AbLA('AbXA(:AbXA('AbXA(:AbMA(zAbMA(zAbXA–“AbMA(zAbBA(VAb$A(%A5wA4wIHAA42I3]Aε)I3)A4]I3RA4AIHAA(bAz<A(`Ab#A(−Ab9A(VAb7A(YAb7A–YAbBA(!AbBA(!Ab7A(#Ab7A(&Ab7A(#AbBA(#AbHA(?AbDA(¢A)RA40I3Ob:)I3)A44I36A4[I3]A(}AbNA(ÂAbHA(•AbjA–…Ab9A(…AbjA–ÂAb9A(£Ab9A(£AbjA(ïAbjA(ïAbNA(»Ab9A(…AbqA(εAbQA()AY$A4AIHAA4.I3RAV)I3)A46I30A4KI3RA(×Ab9A(×AbNA(§AbNA(ΚAbGA(×AbGA–ΚAbGA–αAbGA–λAbGA(λAb%A(ηAb%A–ηAbGA–μAbGA(έAbGA7ρAb%A(κAb"A(κAb%AzόAb%A(σAb%A(εAb%A(εAb"A(üAb"A(üAb%A(üAb"A(ñAb%A(РAb"A(РAbqA–РAb"A(РAbqA–сAbqA(сAb"A–кAb"A(иAbqA(кAb–A)0AbMA(ïA–уA4AIHAA4[I3]IA)I3)A4[I3RA4bIHAA4^AY#A(wAb*A4уAbDAHкAb“AHиAb“A3йAb“A4®Ab“A(AAb“A(AAbzA(AAb“A(IAbzA(EAb¢A4.I4"A44I3OA4)I3PAε)I3)A42I3.A4wIHAA4¢AΚРA(RAb*A(OAbBA–6Ab:A(4Ab'A–4Ab:A–(Ab'A–)Ab'A(PAb'A(2Ab+A(PAb'A()AbMA(GAb*A4+Aε•A4EIHAA42I3[Iε)I3)A4[I3.A4bIHAA(EA–сA(BAbYA("AbLA(GAbDA(NAbDA79AbDA(jAbDA–jAbLA(HAbDA(jAbDA–7AbDA7BAbLA–MAbLA–XAbLA(LAbLA(LAbXA(LAbLA–;AbXA(+AbXA(DAbLA(;AbXA7+AbXA7:AbXA(zAbMA(+Ab7A(YAbQA(2A7έA4AIHAA4[I3KI4)I3)A4]I3RA4AIHAA(bAz<A(`Ab#A(−Ab9A–VAb7A(!AbBA(!Ab7A(YAbBA(!AbBA–#AbBA–&Ab7A(>Ab;A(−A)KA40I31b:)I3)A44I36A4[I3]A(}AbNA(…Ab7A(•AbjA(•Ab9A(…AbjA–…Ab9A–ÂAb9A(ÂAbjA(£AbjA(ïAbjA(ïAbNA(…Ab5A(εAbVA((AY$A4AIHAA4.I3RAH)I3)A4PI3PA41I3OA45I4GA(λAbXA(┐Ab%A–§AbNA–×AbGA(ΚAbNA(×AbNA(ΚAbGA–αAbGA(λAbGA–λAbNA–μAb%A(ηAbGA(έAbGA(έAb%A(έAbGA(έAb%A–ρAb%A7κAb%A(όAb%A(σAb"A(σAb%A(σAb"A(εAb"A(εAb%A(εAb"A(üAb"A(ñAb"A(РAb"A7ñAb"A–уAbqA(уAb"A(уAbqA(сAbqA–кAbqA(сAb5A)1AbLA(ïA–уA4AIHAA4[I3]IA)I3)A4[I3RA4bIHAA4^AY#A(wAb*A4уAbDA4кAb”A4сAb”A3кAb“A4иAb“A4кAb“A4иAb“A4йAb“A4®AbzA4йAb“A(AAbzA4®AbzA(IAbzA(wAb¢A4.I4"A44I3OA4)I3PAε)I3)A42I3.A4wIHAA4¢AΚРA(RAb*A(/AbMA(0Ab:A–6Ab:A74Ab'A((Ab:A((Ab'A((Ab:A()Ab'A(PAb+A(PAb:A((AbMA("Ab*A4;Aε•A4EIHAA42I3[IÂ)I3)A4PI3[A4OIHAA(PA)PA(jAb−A("AbLA7GAbDA(NAb;A–NAbDAYjAbDA(HAbLA(HAbDA(7AbDA(HAbDA(7AbLA(BAbLA(BAbDA–MAbLA(MAbDA(XAbXA(XAbLA–LAbLA(;AbLA(DAbLA–;AbLA(+AbXA(+AbLA('AbLA('AbXA(DAbjA(!Ab*A4кAz=A4AIHAA4]I3RI:)I3)A4]I3RA4AIHAA(bAz<A(^Ab#A(−AbNA(QAbBA(VAb7A(YAbBA(VAbMA(YAb7A7!Ab7A(#AbBA(&AbHA(>Ab;A(¢A)KA40I3Ob:)I3)A44I36A4[I3]A(|AbGA(…AbHA(~Ab9A–~AbjA(•Ab9A(•AbjA(…Ab9A–ÂAbjA(£Ab9A(£AbNA(£Ab9A(•AbqA(σAbVA((AY¢A4AIHAA4.I3RA3)I3)A4PI3PA4OI3wA49I4BA(μAb+A(¿Ab%A(┐AbGA(§AbNA(┐AbNA(§AbNA(×AbNA(×AbGA(ΚAbGA(×AbNA(ΚAbGA(ΚAbNA(αAbGA(λAbGA(λAb%A(λAbGA(ηAbGA(ηAb%A(ηAbGA–μAb%A–έAb%A(ρAb%A(κAb%A(ρAbGA–κAb%A(όAb%A(σAb%A(σAb"A–σAb%A(εAb"A(üAb"A(üAb%A(üAb"A(ñAb"AzРAb"A7сAbqA(сAb"A(РAb–A)1Ab;A({A–ρA4AIHAA4]I3.I4)I3)A4[I3RA4bIHAA4^AY#A(wAb*A4РAb+A4уAb€A:кAb“A4иAb“A4йAb“A4иAb“A3йAb“A4®AbzA(AAbzA(AAb“A(wAb¢A4.I4"A44I3OA4)I3PIA)I3)A42I3]A4wIHAA4zAΚηA(KAb*A(OAbMA(6Ab'A(0Ab:A(4Ab:A(6Ab:A–4Ab:A((Ab'A()Ab:A7PAb'A(4AbMA(qAb*A4;Aε•A4EIHAA4PI3[I@)I3)A4PI3PA40I3EA([A)3A(9Ab¢A("AbDA–"Ab;A(%Ab;A(GAb;A(%Ab;A(GAbDA(NAb;A(NAbDA(9AbLA(jAbLA(jAbDA(9Ab;A(jAb;A(HAbDA(7AbLA(HAbDA(HAbLA(BAbLA–MAbLA(BAbLA(MAbLA–XAbLA–LAbLA(DAbXA(LAbLA(DAbXA(;AbXA–+AbXA(LAb9A(#Ab*A4ηAY;A4AIHAA4]I3RI@)I3)A4]I3RA4AIHAA(AAz=A(^Ab&A(¢AbNA(_AbMA(VAbMA–VAbBA–YAbBA(!Ab7A(YAbBA–#Ab7A(=Ab;A($A)RA40I3Ob3)I3)A4)I3PA40I31A4RI45A(~AbXA(|AbHA(~AbjA(~Ab9A(~AbjA(•AbjA(•Ab9A(•AbjA(…Ab9A(ÂAb9A(…AbjA(…Ab9A–£AbjA(•AbqA(όAbVA(4AY¢A4AIHAA4.I3RA3)I3)A4PI3PA4OI3wA4NI4BA(ηAb+A(¿Ab%A7┐AbNA(┐Ab9A(§AbNA(×AbGA(×AbNA7ΚAbGA(αAbNA–λAbGA–λAb%A(λAbGA–μAb%A(ηAb%A–έAbGA(έAb%A–ρAbGA(ρAb%A(κAb%A(όAb%AzσAb%A(εAbqA(üAb"A(εAb"A(εAb%A(üAb%A(РAbqA(ñAbqA(ñAb"A–РAbqA(уAb"A(уAbqA(РAb5A)0Ab'A(<A7§A4AIHAA4.I3.I4)I3)A4[I3RA4wIHAA4|Az`A(IAb*A4ñAb;A4уAb”A4сAb”A4уAb“A4сAb“AHкAb“A4иAb“A4кAb“A4иAb“A3®AbzA(AAb”A4®AbzA42I3.A4(I30I3)I3)A42I3]A4wIHAA4zAΚλA(.Ab*A(/AbMA(6Ab:A(0Ab:A–6Ab'A–4Ab'A7(Ab'A–)Ab'A(PAb'A(4AbBA("Ab*A4zAε§A4wIHAA42I3]IH)I3)A4(I34A4PI32A(3AbMA("Ab:A(qAb;A–qAbDA("Ab;A–%AbDA(%Ab;A–%AbDA(NAb;A–NAbDA–NAb;A(9Ab;A–jAbDA(HAbDA(7AbDA(HAbDA(7AbLA–BAbDA(MAbDA(MAbLA(MAbDA(MAbLA(XAbLA(LAbLA(XAbLA(LAbXA(DAbXA(MAbNA(!Ab*A4{A£/A4AIHAA4[I3KIε)I3)A4]I3RA4AIHAA(AAz<A(ZAb#A($AbNA(_AbMA(QAbMA(QAbBA(VAbMA–YAbBA–!AbBA(YAbBA(!AbHA(<Ab+A($A)RA40I3Ob3)I3)A4)I3PA40I31A4RI45A(•AbMA(|AbHA(|AbjA–}AbjA(•Ab9A(~AbjA–•Ab9A(…Ab9AzÂAb9A(~Ab5A(όAbVA(4AY¢A4AIHAA4.I3RA4)I3)A4PI32A4EIHIA4MIA:A(έAbzA(»Ab%A(╗AbNA(∩AbNA(┐AbNA(┐AbGA(§AbNA(§AbGA(§AbNA(×AbNA–ΚAbGA7αAbGA(λAbGA(λAbNA(αAbNA(αAbGA(ηAbGA(ηAb%A(ηAbGA(μAbGA(μAb%A(ρAb%A(έAb%A–ρAb%A(κAb"A–κAb%A–όAb%A–σAb%A(εAb%A(εAb"A–üAb"A(üAb%A(ñAb%A–ñAb"A–РAb"A(üAb–A)6AbzA(−A7ÂA4AIHAA4.I3KI3)I3)A4[I3RA4wIHAA4|Az`A(IAb*A4üAb+A4уAb”A3уAb“A3сAb”AHкAb“A4кAb”A4иAb“A4йAb“A4йAbzA4®Ab€A4®AbzA42I3.A4(I30I3)I3)A42I3]A4wIHAA4zAΚηA(.Ab*A(EAbBA(1Ab:A–0Ab:A(6Ab'A(4Ab'A74Ab:A((Ab:A()Ab'A–)Ab:A(6AbBA("Ab*A4zAε§A4wIHAA42I3]I3)I3)A44I31A4]I33A(5Ab:A(qAb+A(–Ab+A(5Ab;A–qAb;A("Ab;A–%Ab;A("Ab+A–%Ab;A(GAbDA(NAbDA(GAb;A(9Ab;A(9AbDA(NAb;A(9AbDA(jAbLA–jAbDA(7AbLA(7AbDA(7AbLA(7AbDA(BAbDA–BAbLA7XAbLA(LAbLA(7Ab9A(QAb*A4!AΚέA4AIHAA42I3]b4)I3)A4]I3RA4AIHAA(AAz=A(@Ab*A($Ab9A–_AbBA(VAb7A(VAbBA(VAbMA–YAbBA(YAb7A(!AbBA(!AbHA(=Ab+A($A)KA40I31b3)I3)A4)I3PA40I31A4RI45A(}AbXA({Ab7A(|AbHA(}AbjA(~Ab9A(}AbjA(~AbjA(•Ab9A(•AbjA(…Ab9A–•Ab9A(ÂAb9A(~Ab5A(κAb!A(bAYLA4AIHAA4.I3RA3)I3)A4PI32A4EIHIA4MIA:A(έAb“A(»Ab%A(╗AbNA(∩Ab9A(∩AbNA(╗Ab9A–┐AbNA(§AbNAz×AbNA(ΚAbGA(×AbNA(ΚAbNAzλAbGA(ηAbGA(ηAb%A(ηAbGA(ηAb%A(μAbGA(έAb%A(ρAb%A(έAbGA(κAb"A–κAb%A(όAb"A(σAb"A(σAb%A(σAb"A(εAb"A(σAb"A(εAb"A(üAb"A(üAb%A(ñAb%A7ñAb"A(εAb3A)4Ab”A(:Az@A4AIHAA4KI3KIH)I3)A42I3RA4wIHAA4{Az`A4®Ab*A4üAb+A4РAb“A3РAb”AHуAb”A4сAb“A4кAb“AHиAb“A4йAbzA4йAb€A4®Ab:A42I3.A4(I30IH)I3)A42I3]A4EIHAA4;AεïA(.Ab*A(EAbXA–1Ab:A(0Ab:A–6Ab'A–4Ab'A–(Ab:A((Ab'A()Ab'A(6AbBA("Ab*A4zAε§A4wIHAA42I3]IA)I3)A4)I3PA46I3/A4RI4GA(qAb$A––Ab;A–5Ab;A(qAb;A(5Ab+A–qAb;A("Ab;A("Ab+A–%Ab;A7GAbDA(GAb;A–NAbDA(9Ab;A(9AbDA(9Ab;A(HAbLA(HAb;A(HAbDA(7AbDA(7AbLA(7AbDA(BAbDA–MAbLA(HAbHA($Ab*A4DIA<A4EIHAA4PI3[b:)I3)A4]I3RA4AIHAA(AAz<A(ZAb&A($Ab9A(−AbBA(_AbBA–QAb7A(QAbBA(VAb7A7VAbBA(!AbHA(<Ab+A(€A)KA40I31b3)I3)A4)I3PA40I31A4RI45A(}AbMA({AbHA(|AbjA7}AbjA(~AbjA–•Ab9A(•AbjA(•Ab9A(…Ab9A(ÂAb9A(}Ab5A(κAb!A(bAYDA4AIHAA4.I3RA3)I3)A4PI32A4EIHIA4MIA:A(έAbzA(£Ab"A(¿Ab9A(∩Ab9A–╗AbNA(╗Ab9A–┐AbNA7§AbGA(×AbNA7ΚAbGA7αAbGA–λAbGA(ηAbGA(ηAb%A–μAbGA(μAb%A(έAb%A(έAbGA(ρAbGA(ρAb%A–κAb%A7όAb%A(σAb%A(εAb"A(σAb%A(εAb"A7üAb"A(РAbqA(σAbRA)(Ab$A(7AzYA4AIHAA4KI3RIH)I3)A42I3RA4wIHAA4}Az∩A4йAb*A4üAb'A3üAb€A4ñAb”A4уAb“A4уAb”A3уAb“A4сAb”A3кAb“A4кAb”A4кAb“A4®Ab¢A4сAbLA4)I3(A4(I34I:)I3)A4PI3]A4EIHAA4;Aε»A(]Ab*A(EAbMA(1Ab:A(1Ab'A(1Ab:A(6Ab'A(6Ab:A(4Ab:A74Ab'A((Ab:A–)Ab'A(4AbBA(%Ab*A4¢AΚόA4bIHAA42I3.Aε)I3)A4)I3PA46I3/A4RI4GA(qAb€A(RAb;A––Ab;A(–Ab+A(5Ab;A(5Ab+A–qAb;A("Ab;A–"Ab+A(%Ab;A(%AbDA–GAb;A(GAbDA–NAbDA–9AbDA–jAbLA–HAbDAz7AbDA(HAbBA(:AbQA4NI4'A4OIHIA4PI3Pb@)I3)A4]I3RA4AIHAA(AAz=A(?Ab&A(€Ab9A–−AbBA–_AbBA–VAbBA(QAbMA(QAbBA(VAbBA(YAb7A(<Ab+A(€A)RA40I3Ob3)I3)A4)I3PA40I31A4RI45A(}AbMA–{AbHA–|AbjA(}AbjA–}Ab9A–~AbjA7•AbjA(|Ab5A(κAbVA(bAYLA4AIHAA4.I3RA4)I3)A42I32A4bIHAA4'IA_A(ρAb$A(ÂAbqA–»Ab9A7∩AbNA(╗AbNA–┐AbGA(╗AbNA(┐AbNA(§AbNA(§AbGA(×AbGA–×AbNA(ΚAbGAzαAbGA(λAbGA(ηAbGA(μAb%A(ηAbGA–μAbGA–έAb%A(κAb%A–ρAb%A(κAb%A(όAb%A(όAb"A(όAb%A(σAb"A(σAb%A–εAb"A(ρAbKA))Ab_A(EAZ–A4AIHAA4.I3KI@)I3)A42I3RA4wIHAA4}Az¿A4йAb*A4εAb:A4üAb€A:РAb”A3сAb“A3уAb”A4сAb”A4иAb“A4кAbzA4®Ab¢A4сAbDA4)I3(A4(I34I:)I3)A4PI3]A4EIHAA4;AεïA(]Ab*A(EAbXA(1AbzA(1Ab:A(OAbzA(6Ab'A(0Ab:A(6Ab'A(6Ab:A–4Ab'A((Ab:A((Ab'A()Ab'A(6AbBA(qAb*A4¢AΚόA4bIHAA42I3.AΚ)I3)A4PI3PA40I3wA45I4XA("AbQA(KAbDA(RAb+A(RAb;A(3Ab+A––Ab;A(–Ab+A(5Ab;A(qAb;A("AbDA7"Ab;Az%Ab;A–GAb;A(NAb;A(9Ab;A–9AbDA7jAbDA(HAbDA(7AbLA(XAbzA4RI4%A46I3OA4)I3PbΚ)I3)A4]I3RA4AIHAA(AAz=A(>Ab*A(”Ab9A–−AbBA(−AbMA–_AbMA(QAbBA(VAbBA(VAbMA(YAbBA(VAb7A(&Ab+A(”A)RA40I3Ob3)I3)A4)I3PA40I31A4RI45A({AbXA({Ab7A({AbHA–|AbjA(|AbHA7}AbjA(~AbjA7•Ab9A({Ab5A(ρAb!A(bAYLA4AIHAA4.I3RA4)I3)A42I32A4bIHAA4'IA_A(ρAb$A(…Ab"A(»Ab9A–¿AbNA(¿Ab9A–∩AbNA(╗AbNA(┐AbNA(╗Ab9A–┐AbNA7§AbNA(§AbGA(ΚAbGA(αAbGA(ΚAbGA–λAbGA(αAbGA–λAbGA–ηAbGA(μAb%A(μAbGA–έAb%A(έAbGA(ρAb%A(κAb%A(κAb"A(κAb%A(όAb%A(λAbRA)6Ab_A4ÂAΚαA4AIHAA4]I3]bA)I3)A42I3RA4wIHAA4~Az»A4йAb*A4σAb'A4ñAb”A3ñAb“A4ñAb”A3РAb”A4уAb“A4РAb”A4уAb”A4сAb“A4кAb“A4сAbzA4®Ab$A4сAb;A4)I3(A4(I34IV)I3)A4PI3[A4/IHAA4MAε`A([Ab*A(EAbXA(1Ab'A(OAb:A(1Ab:A(0Ab:A(6Ab:A(0AbzA(6Ab:A(4Ab'A–4Ab:A()Ab'A(0AbBA(qAb*A4¢AΚσA4bIHAA42I3.AÂ)I3)A4PI32A41IHIA4GIA“A("Ab&A(]AbXA–RAb;A(3Ab;A(3Ab+A(–Ab;A(–Ab+A(5Ab;A(–Ab;A(5Ab;A–qAb;A("Ab;A–qAb;A–"Ab+A(%Ab;A7GAb;A(NAbDA79AbDA(BAb”A(qA)"A44I31wH)I3)A4]I3RA4AIHAA(AAz=A(?Ab&A(”Ab9A7¢AbMA(−AbMA(_AbBA7QAbBA–VAb7A(*Ab;A(”A)RA46I3Ob3)I3)A4)I3PA40I31A4RI45A({AbXA(`Ab7A(`AbjA({AbHA–{AbjA(|AbHA(|AbjA(~AbjA(}AbjA(~AbjA–~Ab9A(|Ab5A(ρAb!A(bAYDA4AIHAA4.I3RA4)I3)A42I32A4bIHAA4'IA_A(ρAb€A(…Ab"A–»Ab9A(¿Ab9A7∩AbNA7╗AbNA(┐AbNAz§AbNA(§AbGA(ΚAbGA(×AbNA(ΚAbNA–αAbGA(αAb%A–λAbGA(λAbNA–μAbGA(έAbGA(έAbNA(μAbGA4.I3KA46I30bε)I3)A42I3RA4EIHAA4}Az∩A4кAb*A4σAb'A3üAb“A3ñAb”A4ñAb€A4ñAb”A3РAb”A3уAb”A4сAbzA4йAb_A4üA)jA44I3OIÂ)I3)A4PI3[A4/IHAA4MAε`A([Ab*A(wAbLA(OAb:A–1Ab:A(0Ab:A(1AbzA–6Ab:Az4Ab:A((Ab'A(0AbBA(qAb*A4VAÂйA4bIHAA42I3.A@)I3)A4PI32A41IHIA4GIAzA("Ab#A(]AbXA(RAb+A(KAb+A–RAb+A–3Ab+A(–Ab;A(–Ab+A(5Ab+A–5Ab;A(qAb;A("Ab;A("AbDA–"Ab;A(%AbDA(%Ab;A7GAb;A(%AbXA(MAb¢A([A)4A4/IHAA42I3[w:)I3)A4]I3RA4AIHAA4®Az=A(>Ab*A(“Ab9A(¢AbMA(−AbMA–¢AbMA(−AbMA(_AbBA(QAbBA(_AbBA(QAbMA(QAb7A(&Ab+A(“A)RA46I3Ob4)I3)A4PI3PA41I3/A4qI49A(•Ab+A(ZAbjA(`AbjA7`AbHA({AbjA({AbHA7}AbjA(~AbjA(~Ab9A(•Ab9A(`AbqA(μAb#A(IAYDA4AIHAA4.I3RA4)I3)A42I32A4bIHAA4'IA_A(έAb$A(…AbqA(»AbNA(ïAb9A(»Ab9A–¿AbNA(∩AbNA(¿AbNA(∩Ab9A(╗AbNA(┐AbNA(┐AbGA(┐AbNA–§AbGA(§AbNA–×AbGA(ΚAbGA(αAbGA(ΚAbNA(ΚAbGAzλAbGA(ηAbGA(μAb%A(μAbGA(μAb%A(ηAb"A(уAbXA4NI47A4/I3EA4PI3PbV)I3)A42I3RA4EIHAA4•A7έA4сAb*A4σAb:A4εAb”A3εAb€A:ñAb”A4РAb”A4РAb“A3уAb”A4сAb“A4иAb_A4εA)jA44I3OIÂ)I3)A4PI3[A4/IHAA4MAε`A(2Ab*A(wAbLA(OAbzA7OAb:A(1Ab:A–0Ab:A–6Ab'A(4Ab'A((Ab'A((Ab:A(0AbMA(qAb*A4VAÂ®A4bIHAA42I3.AV)I3)A4PI32A4OIHAA4HIAVA(%Ab*A(2AbXA(.Ab'A7KAb+A(3Ab+A(RAb+A(3Ab;A7–Ab+A(5Ab;A–qAb;A(5Ab+A(qAb+A("Ab;A(qAb;A–%AbDA("AbXA(XAb&A4®A7έA4IIHAA4[I3KwÂ)I3)A4]I3RA4AIHAA4®Az=A(>Ab*A(“Ab9A(¢AbBA(¢AbMA–¢AbBA–−AbMA(−AbBA–QAbBA(QAb7A(&Ab+A(“A)RA46I3Ob4)I3)A4PI3PA41I3/A4qI49A(~Ab+A(@AbjA(^AbHA(`AbHA–`AbjA({AbjA–|AbjA({AbHA(|AbjA–}Ab9A(•Ab9A(`AbqA(μAb!A(IAYLA4AIHAA4.I3RA4)I3)A42I32A4wIHAA4+IA_A(μAb$A(…Ab5A–ïAbNA–»Ab9A–¿AbNA(∩Ab9A–∩AbNA(╗AbNA–┐AbNA–§AbGA7§AbNA–ΚAbGA(×AbGA(ΚAbGA(αAbGA(λAbGA(αAbGA–λAbGA–ηAbGA(μAb%A(μAbGA(έAb%A(αAb5A(®Ab“A4:IA¢A4bIHAA42I32bH)I3)A42I3RA4EIHAA4•A7έA4сAb*A4κAbzA4σAb”A4εAb”A4εAb€A4εAb”A4üAb”A4üAb€A4ñAb€A4ñAb”A4РAb”A4РAb“A3уAb“A4иAb_A4üA)jA44I3OIΚ)I3)A4PI32A4OIHAA4jIA&A(PAb*A(EAbLA(OAb:A(/AbzA71Ab:A(0Ab'A(0Ab:A–4Ab'A(4Ab:A((Ab'A(0AbBA(qAb*A4VAÂ®A4bIHAA42I3.AV)I3)A4PI32A4OIHAA4jIAVA("Ab*A(2AbXA7.Ab+A(KAb;A(RAb;A(RAb+A(3Ab;A(3Ab+A(3Ab;A––Ab+A(5Ab+A75Ab;A("Ab;A("Ab+A(5AbMA(XAb*A4όAz}A4AIHAA4[I3Rwε)I3)A4]I3RA4AIHAA4йAz=A(=Ab*A(“Ab9A($AbMA(¢AbMA($AbMA(¢AbMA(−AbBA–−AbMA(_AbBA(QAbBA(QAb7A(#Ab+A(“A)KA46I31b4)I3)A4PI3PA41I3/A4qI49A(~Ab+A(@AbjA(^AbHA–^AbjA–`AbHA({AbjA(|AbjA({AbjA(|Ab9A(}AbjA–}Ab9A(^Ab"A(έAb!A(IAYLA4AIHAA4.I3RA4)I3)A42I32A4wIHAA4'IA_A(μAb$A(•AbqA7ïAbNA(»AbNA–¿Ab9A(¿AbNA(¿Ab9A(∩Ab9A–╗AbNA(╗AbGA7┐AbNA(§AbNA(×AbNA(§AbNA–ΚAbNA(ΚAbGA(αAbGA(λAb%A(αAbGA7λAbGA–ηAbGA(μAb%A–έAb%A(ρAb%A(αAbRA)wAb−A4&Aε`A4AIHAA42I3[b4)I3)A42I3RA4EIHAA4…A7έA4уAb*A4κAbzA4εAb”A3εAb€A4εAb”A4üAb”AHüAb€A4ñAb”A4РAb”A4РAb“A4иAb!A4κA)qA40IHbA4PI32IΚ)I3)A4PI32A4OIHAA4jIA&A()Ab*A(wAbDA(/Ab:A(/AbzA(OAb:A–1Ab:A(0Ab:A(0AbzA76Ab:A(4Ab:A(1AbMA(5Ab*A4VAÂ®A4bIHAA42I3.AV)I3)A4PI32A4OIHAA4jIAVA("Ab*A([AbMA–.Ab+A(.Ab'A–KAb+A7RAb+A(3Ab+A(3Ab;A(–Ab;A(–Ab+A(5Ab;A(qAb;A(3AbBA(LAb*A4ïAYXA4AIHAA4[I3RE3)I3)A4]I3RA4AIHAA4йAz=A(=Ab*A(“Ab9A($AbBA7$AbMA(¢AbMA(−AbBA–−AbMA(_AbMA(_Ab7A(!Ab'A(“A)RA46I3ObA)I3)A4PI3PA4OIHbA49I4DA(•Ab“A(>AbNA(@AbHA(ZAbHA(^AbjA(^AbHA(`AbjA(`AbHA(`AbjA(|AbjA–{AbjA(}AbjA(|AbjA(ZAbqA(μAb&A4РAZGA4AIHAA4.I3KA3)I3)A42I32A4wIHAA4'IA_A(μAb$A(•AbqA–£Ab9A(»Ab9A(ïAb9A–»Ab9A(¿AbNA(∩AbNA(∩Ab9A(╗AbNA(∩Ab9A(╗AbNA(╗AbGA(╗AbNA–§AbNA–§AbGA(§AbNA(ΚAbNA(ΚAbGA(×AbGA(ΚAbNA–αAbGA(λAb%A(λAbGA(ηAbGA(μAbGA–μAb%A(μAbGA–έAbGA–ρAb%A(αAbKA)1AbVA4┐AΚüA4AIHAA4]I3.IÂ)I3)A42I3KA4/IHAA4£A7уA4РAb*A4κAbzA4όAb”AHσAb”A3εAb€A4εAb”A4üAb€A4üAb”A4ñAb”A4РAb”A4ñAb“A4кAbYA4κA)qA40IHbA4PI32IΚ)I3)A4PI32A4OIHAA4jIA&A((Ab*A(bAbDA(/Ab:A(/AbzA(OAb:A(OAb'A71Ab:A(6Ab:A(0Ab:A(6Ab:A(4Ab'A(6Ab'A(1AbBA(5Ab*A4&A£6A4IIHAA4[I3KA:)I3)A4PI32A4OIHAA4jIAVA(qAb*A(2AbMA([Ab'A(]Ab'A(]Ab+A(.Ab+A7KAb+A(RAb+A(RAb;A(3Ab+A(3Ab;A(–Ab+A(KAb7A(LAb*A4ZA£PA4AIHAA4[I3KE:)I3)A4]I3RA4AIHAA4йAz=A(<Ab*A(zAbjA–€AbMA($AbBA($AbMA($AbXA(¢AbMA(−AbBA(−AbMA(_AbBA(QAb7A(#Ab+A(zA)3A46I3ObA)I3)A4PI3PA4OIHbA49I4DA(~Ab“A(>AbNA(@AbHA(ZAb7A–^AbHA(`AbHA(`AbjA(^AbHA(`AbHA({AbjA({AbHA–|AbjA(ZAb"A(μAb&A4РAZGA4AIHAA4.I3KA3)I3)A42I32A4wIHAA4+IA_A(ηAb$A(~AbqA(ÂAb9A–£Ab9A(»AbNA(»Ab9A(¿Ab9A(»AbNA–¿AbNA–∩AbNA–╗AbNA(╗AbGA(┐AbNA(§AbNA(§AbGA–§AbNA–×AbGA–ΚAbGA–αAbGA–λAbGA(ηAbGA(ηAbNA(ηAb%A(μAb%A(ηAbGA(μAbGA(έAb%A7ρAb%A(κAb%A(αAbRA)1AbVA4уAZ(A4AIHAA4.I3KIV)I3)A42I3KA4/IHAA4£A7уA4ñAb*A4κAbzA3όAb€A4σAb”A4εAb”A4σAb”A4üAb”A4üAb€A4εAb€A3üAb”A4ñAb”A4ñAb“A4сAb!A4ρA)5A40IHbA4PI32Iε)I3)A4PI32A41IHAA4%IA$A(4Ab*A(bAb;A–/Ab:A(OAbzA(OAb:A(1AbzAz0Ab:A(0Ab'A(6Ab:A(1AbMA(5Ab*A4&A£6A4IIHAA4[I3KAH)I3)A4PI3[A4/IHAA4MIA?A("Ab*A(PAbMA([Ab+A–[Ab'A–]Ab'A–.Ab+A–KAb+A(RAb+A(RAb;A(]Ab7A(BAb*A4VAΚñA4IIHAA42I3.E@)I3)A4]I3RA4AIHAA4йAz>A(<Ab*A(:Ab9Az€AbMA($AbBA(¢AbMA(¢AbBA–−AbMA(_Ab7A(!Ab'A(:A)RA46I3OIε)I3)A4PI32A4EIHAA4MIA€A(ÂAb−A(<AbGA(@AbHA(?Ab7A7ZAbHA–^AbHA(`AbHA(`AbjA({AbHA–`AbjA(|AbjA(ZAbqA(ηAb&A4РAZGA4AIHAA4.I3KA3)I3)A4PI32A4wIHAA4+IA_A(λAb−A(~Ab"A(ÂAb9A(ÂAbjA(£Ab9A(ïAbNA7ïAb9A(»Ab9A(∩AbNA(¿AbNA(¿Ab9A(∩AbNA(╗AbGA(╗AbNA–╗Ab9A–§AbGA(§AbNA(┐AbNA(§AbNA(×AbGA(ΚAbGA(ΚAbNA(ΚAbGA(αAbGA(αAb%A(λAb%A7ηAbGA(μAbGA–μAb%A–έAb%A(έAbGA(ρAb%A–ρAbGA(λAbRA)0Ab_A((AYBA4AIHAA4.I3RIH)I3)A42I3KA4/IHAA4ÂA7уA4ñAb*A4έAb“A4ρAb€A3όAb€A3σAb”A4σAb€A4εAb”A4üAb”A4üAb€A4üAb”A4ñAbzA4кAb&A4λA)[A41IHAA4PI3[bA)I3)A4PI32A41IHAA4%IA$A((Ab*A(bAb;A(EAbzA(/AbzA(OAb:A(OAbzA–OAb:A(OAbzA(1Ab:A(0Ab:A(6Ab:A(0Ab:A(/AbMA(–Ab*A4&A£6A4IIHAA4[I3KAH)I3)A4PI3[A4/IHAA4MIA?A(qAb*A()AbXA([Ab:A–[Ab'A(.Ab'A(]Ab'A(.Ab'A(.Ab+A–KAb+A(RAb+A(]Ab7A(7Ab*A4$AΚλA4bIHAA42I3]EÂ)I3)A4]I3RA4AIHAA4иAz>A(*Ab*A(:Ab9A–”AbMA–$AbBA–$AbMA(¢AbMA(−AbBA(¢AbMA(−AbBA(!Ab'A(:A)RA46I3OIΚ)I3)A42I32A4wIHAA4'IA!A(ÂAbQA(*Ab%A(?AbHA(>AbHA(?Ab7A–@AbHA(ZAbHA(^AbjA–ZAbHA(^AbjA({AbjA(`AbjA({AbHA(@AbqA(λAb*A4μAZ]A4AIHAA4]I3KAH)I3)A4PI32A4wIHAA4+IA_A(λAb$A(}AbqA–ÂAb9A(ÂAbNA–£Ab9A(ïAbNA(»AbNA(ïAb9A(¿Ab9A(»Ab9A(¿Ab9A–∩Ab9Az╗AbNA–┐AbNA(§AbGA(§AbNA(§AbGA–ΚAbGA(αAbGA(ΚAbGA(αAbGA–λAbGA(ηAb%A(λAbGA(ηAbGA(ηAb%A(μAbGA(έAb%A(μAbGA(έAbGA(ρAb"A(κAb%A(ρAb%A(κAb%A(όAb"A(μAb3A)EAb¢A(NAzYA4AIHAA4.I3RIA)I3)A42I3.A4OIHAA4»A5wA4üAb*A4έAb“A4κAb$A4κAb€A4όAb”A:όAb€AHεAb”A4üAb”A4σAb“A4сAb&A4λA)[A41IHAA4PI3[bA)I3)A4PI32A41IHAA4%IA$A(4Ab*A(IAb;A(EAb:A(EAbzA–/AbzA–OAbzA71Ab:A(0Ab:A(0AbzA(6Ab:A(OAbMA(3Ab*A4>AZ–A4IIHAA4[I3KA3)I3)A4PI3[A4/IHAA4MIA?A(5Ab*A((AbMA(2Ab'A([Ab+A–]Ab+A–]Ab'A(.Ab'A–.Ab+A(KAb+A(]Ab7A(7Ab*A4$AΚλA4bIHAA42I3]EÂ)I3)A4]I3RA4AIHAA4иAz=A(*Ab*A(:Ab9A(”AbMA–”AbXA–€AbMA($AbMA($AbBA–¢AbBA(−Ab7A(!Ab+A(:A)3A46I3OIÂ)I3)A42I3[A4IIHAA4€AεZA(£Ab!A(#Ab"A(=Ab7A(>AbHA(>Ab7A(>AbHA(?AbHA(@AbjA–@AbHA(ZAbHA(`AbHA(^AbHA(^AbjA(`AbjA(`AbHA(>AbqA(αAb&A4μAZ[A4AIHAA4]I3KAH)I3)A4PI32A4wIHAA4+IA_A(αAb¢A(}Ab"A(ÂAb9A(ÂAbjA(ÂAb9A(£AbNA(£Ab9A(ïAb9A(ïAbNA(ïAb9A–»Ab9A–¿AbNA7∩AbNA7╗AbNA–┐AbNA(§AbNA–×AbGA(ΚAbGA(×AbNA–ΚAbGA(αAbGA(λAb%A7λAbGA(ηAbGA–ηAb%A(έAb%A(έAbGA(ρAb%A(έAbGA(έAb%A(κAb"A–κAb%A–όAb%A(κAb–A)bAb'A(YA7×A4AIHAA4.I3.AÂ)I3)A42I3.A4OIHAA4ïA5wA4εAb*A4μAb“A3ρAb€A4ρAb$A4κAb$A3όAb”A4όAb€A4εAb€A4εAb”A4σAb”A4εAb€A4εAb“A4сAb*A4αA)]A41IHAA4PI3[b4)I3)A4PI3PA40IHbA45I4;A(0Ab&A(wAb+A(EAbzA(EAb:A(/Ab:A7OAb:A(OAbzA(1AbzA–0Ab:A(6Ab'A(1AbMA(–Ab*A4>AZ3A4IIHAA4[I3KA3)I3)A4PI3[A4/IHAA4MIA?A(qAb*A((AbMA(PAb:A(2Ab'A([Ab+A(2Ab'A([Ab'A(]Ab+A([Ab+A–.Ab+A(.Ab'A(KAb+A([Ab7A(7Ab*A4VAΚñA4IIHAA42I3.E@)I3)A4]I3RA4AIHAA4иAz=A(*Ab*A('AbHA(“AbMA7€AbMA(€AbXA–$AbMA(¢AbMA($AbXA(¢AbBA(VAb'A('A)3A46I3OI@)I3)A42I3[A4AIHAA4VAεÂA(ïAb&A(!Ab"A(=AbHA(=Ab7A–>AbHA–?Ab7A(?AbHA(@AbjA(@AbHA(ZAbHA(^AbHA(ZAbHA(^AbHA–`AbjA(?AbqA(λAb&A4μAZ[A4AIHAA4]I3KAH)I3)A4PI32A4wIHAA4+IA_A(αAb¢A(}AbqA–…AbjA(ÂAb9A(…Ab9A(£AbjA(ÂAbjA(ïAb9A(£Ab9A(»Ab9A(ïAb9A(~Ab–A(йAb*A4VAε`A4уAZ3A(кAb&A(£Ab5AY┐AbNA–§AbNA(×AbNA–×AbGA(ΚAbGA(ΚAbNA–αAbGA(λAbGA(αAbGA(λAbGA(ηAbGA(μAbGA(μAb%A(έAb%A(μAbGA(μAb%A–ρAb%A(ρAb"A(κAb"A(κAb%A(όAb%A(σAb%A(όAb%A(όAbqA(®AbDA(}A–сA4AIHAA4[I3]AV)I3)A42I3.A4OIHAA4£A5EA4σAb*A4έAb“AHρAb€A3κAb$A4κAb€A4σAb€A4σAb”A3σAb€A4σAb“A4сAb*A4×A5OA4OIHAA42I3.b3)I3)A4PI3PA40IHbA45I4;A(1Ab&A(bAb'A(EAb:A(EAbzA(EAb:A(/Ab:A(/AbzA(OAb:A(1Ab:A(OAb:A(1AbzA(0AbzA(0Ab'A(OAbMA(3Ab*A4>AZ–A4IIHAA4[I3KA3)I3)A4PI3[A4/IHAA4MIA?A(–Ab*A((AbMA(PAb+A72Ab'A([Ab+A([Ab'A–]Ab+A(.Ab'A(]Ab'A(.Ab+A([Ab7A(HAb*A4VAΚñA4bIHAA42I3.E@)I3)A4]I3RA4AIHAA4иAz>A(&Ab*A(+AbjA(zAbXA(”AbMA(“AbXA(”AbMA(€AbBA(€AbMA($AbBA($AbMA(¢AbMA($Ab7A(VAb+A(+A)3A46I3OI:)I3)A4[I3.A4AIHAA4`AΚσA(ïAb*A(VAb%A(*Ab7A(<AbHA(<Ab7A–=AbHA(>AbHA(?AbHA(>AbHA–@AbHA7ZAbHA(ZAb7A–^AbHA(=AbqA(ΚAb*A4╗A£OA4AIHAA4]I3KA:)I3)A4PI32A4wIHAA4+IA_A(ΚAb−A(|Ab"A7…AbjA(ÂAb9A(ÂAbjA(£AbNA(£Ab9A7ïAbNA(•Ab3A(ñAb#A4…AΚσA4IIHAA4AIHAA4уAZ–A(уAb!A(£Ab–A(╗AbNA(┐AbGA–┐AbNA(§AbNA–×AbGA(×AbNA–ΚAbGA(ΚAbNA–αAbGA–λAbGA(ηAb%A(μAb%A–ηAbGA(μAbGA–έAb%A(ρAbGA–ρAb%A(όAb%A(όAb"A(όAb%A(σAb%A(όAb"A(σAb"A(σAbqA(кAb7A(×A)4A4OI3/A4PI3PA3)I3)A4PI3]A41IHAA4»A5PA4κAb*A4ηAb”A3έAb€A3ρAb€A3κAb€A3όAb€A4κAb€A3όAb€A4σAb“A4сAb*A4§A51A4OIHAA42I3.b3)I3)A4PI3PA40IHbA45I4;A(OAb*A(bAb+A(EAb:A(wAbzA(EAb:A(/Ab:A(/AbzA(/Ab:A(OAb:A–OAbzA–1Ab:A(0Ab:A(/AbXA(3Ab*A4`AZ7A4IIHAA4[I3RA4)I3)A4PI3[A4/IHAA4MIA?A(–Ab*A(6AbXA()Ab:A(PAb'A(2Ab'A–[Ab'A([Ab+A([Ab'A(]Ab'A(]Ab+A(.Ab'A(KAb+A(.Ab+A(KAb+A(RAb+A(3Ab;A–3Ab+A(3Ab;A(3Ab+A(–Ab+A––Ab;A(5Ab;A–qAb;A("Ab;A("AbDA("Ab;A–%Ab;A(GAbDA(GAb;A(NAb;A(GAb;A(9AbDA(NAb;A(9AbDA–jAbDA–HAbDA–HAb;A(7AbLA(BAbLA–BAbDA(MAbLA7XAbLA(LAbXA(LAbLA(DAbXA(DAbLA(DAbMA(:Ab“A4–I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4кAz>A(#Ab*A('Ab9A(“AbMA–“AbXA(”AbMA–”AbXA(€AbMA(€AbXA($AbMA(¢AbMA(¢AbBA($AbMA7−AbBA(_AbMA(QAb7A7QAbBA(VAbBA7YAbBA–!AbBA(!Ab7A(#Ab7A(#AbBA(#Ab7A(&Ab7A7*Ab7A7<Ab7A(>AbHA(=AbHA(>AbHA–?AbHA–@AbHA–ZAbHA(^AbHA(ZAbHA(=AbqA(ΚAb*A4╗A£/A4AIHAA4]I3KA:)I3)A4PI32A4wIHAA4+IA_A(ΚAb−A(|Ab"A(•AbjA7…Ab9A(…AbjA(ÂAb9A–ÂAbjA–ïAb9A(•Ab–A(ñAb!A4…AΚόA4AIHAA4[I3.A4]I3.A4AIHAA4×A£AA(сAb!A(£Ab3A(╗AbNA(┐AbNA(┐AbGA–§AbNA–×AbGA(ΚAbGA(×AbNA(αAbGA(αAbNA–αAbGA(ηAb%A–ηAbGA(ηAb%A(μAb%A(ηAbGA(ηAb%A(έAbGA(ρAbGA–ρAb%A(κAb%A(όAb%A(όAb"A(σAb%A(όAb%A(σAb%A(σAb"A(εAb%A(üAb"A(εAb"A3)I3)A4PI3]A41IHAA4»A5PA4κAb*A4ηAb“A3έAb€A4έAb$AHρAb€A3όAb€A4κAb€A4όAb€A4όAb$A4κAbzA4уAb*A4§A51A4OIHAA42I3.bH)I3)A4)I3PA46I3EA4RI4jA(/AbVA(bAb:A–wAbzA–EAbzA(/AbzA(EAbzA–OAb:A–1AbzA(0Ab'A(/AbBA(RAb*A4^AZBA4IIHAA4[I3RA3)I3)A4PI32A4OIHAA4jIAVA(3Ab*A((AbXA(2Ab'A(PAb'A72Ab'A([Ab+A(]Ab+A(]Ab'A–.Ab'A(.Ab+A7KAb+A–3Ab;A(RAb;A(3Ab;A(–Ab+A(3Ab+A75Ab;A(5Ab+A(qAb;A–"Ab;A–%Ab;A(%Ab+A–GAbDA(GAb;A(9AbDA(NAbDA(9AbDA–jAbDA(jAbLA(HAbLA(HAbDA(HAbLA(7AbLA(7AbDA7BAbLA–MAbDA(MAbLA(XAbLA(LAbLA(XAbLA(DAbLA(DAbXA(zAbzA4–I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4кAz>A(!Ab*A(+AbjA(zAbMA(zAbXA7“AbXA(”AbMA7€AbMA–$AbMA(¢AbBA–¢AbMA(_AbBA(−AbMA(_AbMA(QAbBA(_AbBA(VAbBA(QAbBA–VAbBA(YAb7A(YAbBA–!Ab7A(!AbBA(#Ab7A(#AbBA(#Ab7A–&Ab7A(*Ab7A–<Ab7A(<AbHA(=AbHA(=Ab7A(>AbHA–?AbHA(?Ab7A7@AbHA(ZAbHA(<AbqA(§Ab*A4…AÂсA4AIHAA4[I3.AV)I3)A4PI32A4wIHAA4+IA_A(§Ab−A(`Ab"A(•Ab9A–•AbjA–…Ab9A–ÂAb9A(£Ab9A(£AbNA(£Ab9A(~Ab–A(üAb!A4…AΚόA4AIHAA4[I3.AH)I3)A4[I3]A4AIHAA4=Aε£A(РAbVA(£Ab–A(┐AbNA–§AbNA(×AbGA(ΚAbNA(×AbNA(ΚAbNA(ΚAbGA(λAbGA(αAbNA(λAb%A7λAbGA(ηAb%A7μAb%A(ρAb%A–ρAbGA(ρAb%A(κAb%A(ρAb%A(όAb%A(όAb"A(σAb%A–σAb"A(üAb"A(εAb"A3)I3)A4PI3]A41IHAA4ïA5PA4ρAb*A4λAb”A4μAb€A4μAb$A4έAb$A4μAb$A4μAb€A4έAb€A4ρAb$A3κAb”A4όAb”A4κAbzA4уAb*A4»A–йA4/IHAA42I3Kb:)I3)A4)I3PA46I3EA4RI4jA(/AbVA(bAb:A–wAbzA(EAb:A(EAbzA(/Ab:A(EAb:A(OAb:A(/AbzA(OAb:A–1Ab:A(/AbMA(RAb*A4^AZ7A4IIHAA4[I3RA3)I3)A4PI32A4OIHAA4jIAVA(3Ab*A(6AbXA–)Ab'A(PAb'A(2Ab+A(2Ab'A([Ab+A([Ab'A(]Ab+A(]Ab'A(.Ab+A(]Ab+A(.Ab+A–.Ab'A–KAb+A–3Ab;A(3Ab+A(–Ab;A(3Ab+A(5Ab;A(–Ab;A(–Ab+A(5Ab+A(qAbDA(qAb;A–"Ab;A–%Ab;A–GAbDA(GAb;A–NAb;A(NAbDA(9AbDA(jAbDA–jAb;A–HAbDA(HAbLA(7AbLA(7AbDA(BAbLA(BAbDA(BAbLA(MAbLA(XAbLA(XAbXA(XAbLA(LAbLA(DAbXA('Ab“A4–I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4сAz>A(!Ab*A(+AbjA(:AbXA(zAbXA(“AbXA(zAbXA–“AbXA–”AbMA–€AbMA–$AbMA7¢AbMA(−AbMA(−AbBA(_AbBA(_AbMA7QAbBA(VAbBA(YAbBA–!Ab7A–!AbBA–#Ab7A–&Ab7A(&AbBA(*Ab7A(*AbBA(*AbHA(<Ab7A(=AbHA(=Ab7A(<Ab7A(>AbHA(?Ab7A(>Ab7A(?AbHA(@Ab7A(?AbHA(ZAbHA(<AbqA(§Ab*A4…AÂсA4AIHAA4[I3.AV)I3)A4PI32A4wIHAA4+IA_A(×Ab−A({Ab"A(~AbjA(•Ab9A(•AbjA(•Ab9A(•AbjA(…Ab9A7ÂAb9A(ïAb9A(~Ab3A(εAb#A4…AΚσA4AIHAA4[I3.AV)I3)A42I32A4IIHAA4”IA#A(üAb¢A(»Ab5A(┐AbNA(×AbGA(×AbNA(×AbGA–ΚAbNA(ΚAbGA(αAbNA–λAb%A–ηAb%AzμAb%A(μAbGA(ρAbGA–ρAb%A7κAb%A(κAb"A(κAb%A(σAb"A(όAb%A(σAb"A(εAb"A4)I3)A4PI3[A40IHAA4¿A)–A4έAb&A3ηAb€A3μAb€A4μAb$A3έAb€A3έAb$AHκAb€A4κAbzA4РAb*A4¿A–йA4/IHAA42I3Kb:)I3)A4)I3PA46I3EA4RI4jA(EAbVA(bAb'A(bAbzA(wAbzA(bAbzA(wAbzA(EAb:A(EAbzA–/Ab:A(OAb:A(1Ab:A(OAb:A(OAbzA(EAbLA(KAb*A4~AY“A4IIHAA4[I3RA4)I3)A4PI32A4OIHAA4jIAVA(RAb*A(6AbXA()Ab'A(PAb+A(PAb'A(PAb:A(2Ab+A(2Ab'A([Ab'A(]Ab'A([Ab:A(.Ab+A–]Ab'A(.Ab+A–KAb+AzRAb+A(3Ab;A(–Ab+A(–Ab'A(–Ab;A(5Ab;A(5Ab+A(qAb;A(qAb+A(qAb;A(%Ab;A("Ab;A(%Ab;A(%AbDA(%Ab;A(GAbDA–NAbDA–9AbDA(9Ab;A(jAbDA(jAbLA(jAbDA7HAbDA(7AbLA(7AbDA(BAbDA(BAbLA(MAbLA(XAbXA(MAbDA(XAbXA(LAbLA(LAbXA(:AbzA4–I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4сAz>A(!Ab*A(;AbjA(:AbMA–zAbMA–zAbXA(“AbMA(“AbXA(”AbMA7€AbMA($AbBA($AbMA–¢AbMA(−AbBA(_AbMA(_AbBA(−AbMA(_AbBA(VAbBA–QAbBA(VAbBA(YAb7A–YAbBA(#Ab7A(#AbBA(!AbBA(#Ab7A7&Ab7A–*Ab7A(<Ab7A(<AbHA(<Ab7A(>AbHA–=Ab7A(>Ab7A–?AbHA(@AbHA(*AbqA(┐Ab*A4^AΚέA4AIHAA4[I3]A@)I3)A4PI32A4wIHAA4+IA_A(§Ab−A(`Ab"A–}AbjA(•Ab9A(•AbjA(•Ab9A(•AbjA(…Ab9A(ÂAbjA–£Ab9A(~Ab3A(εAb#A4•AΚσA4AIHAA4[I3.AÂ)I3)A4PI3PA4EIHbA47I4;A(κAb:A(╗AbqA(┐AbNA(×AbGA(×AbNA(×AbGA(×AbNA–ΚAbNAzλAbGA(ηAbGA(ηAb%A–μAbGA(μAb%A–έAbGA–ρAb%A(κAb%A(ρAb%A–όAb%A(σAb%A(σAb"A(σAb%A4)I3)A4PI3[A40IHAA4¿A)3A4έAb*A4ηAb€A4λAb$A4ηAb$A4ηAb¢A4μAb¢A4έAb€A4έAb$A4ρAb$A4ρAb€A3ρAb$A4κAb€A4ρAb“A4ñAb*A4»A–иA4/IHAA42I3KbV)I3)A4)I3PA44I31A4]I45A(bAb$A(IAb“A(bAbzA–wAbzA–EAb:A(/AbzA(/Ab:A7OAb:A(1Ab:A(/AbXA(.Ab*A4}AY”A4IIHAA4[I3RA4)I3)A4PI32A4OIHAA49IAVA(KAb*A(6AbXA–(Ab:A–PAb'A(PAb:A(2Ab:A(2Ab'A([Ab+A([Ab'A(]Ab+A–[Ab'A–.Ab+A(KAb+A(RAb+A(KAb+A–3Ab+A(3Ab;A(3Ab+A––Ab;A(–Ab+A(5Ab+A(5Ab;A–qAb;A7"Ab;A–%AbDA–GAbDA(GAb;A(NAbDA79Ab;A7jAbDA–HAbDA(7AbLA–7AbDA(BAbDA(BAbLA(BAbDA(BAbLA(MAbLA(XAbLA(LAbXA(+Ab”A43I49A40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4сAz=A(YAb*A(DAbjA('AbMA(zAbMA7zAbXA(zAbMA(“AbMA–”AbMA–€AbMA($AbMA($AbBA($AbMA(¢AbBA(¢AbMA(−AbBA–−AbMA(−AbBA(_AbBA–QAbMA(VAb7A–YAb7A–YAbMA(YAb7A–!Ab7A–#Ab7A–&Ab7A(*Ab7A(*AbBA(<AbHA–<Ab7A(=Ab7A(=AbHA7>AbHA(>Ab7A(&AbqA(┐Ab*A4^AΚρA4AIHAA4[I3]A@)I3)A4PI32A4wIHAA4+IA_A(┐Ab−A(^Ab"A(}Ab9A(}AbjA(~AbjA(•AbjA(…Ab9A(•Ab9A(…Ab9A–ÂAb9A(£AbNA(|Ab–A(σAb#A4•AΚόA4AIHAA4[I3.I4)I3)A46I30A4]I3.A(§AbGA(ΚAbjA–×AbGA(ΚAbGA(αAb%A(αAbGA(λAbGA(αAbGA(αAbNA(ηAbNA(ηAb%A–μAbGA(μAb%A–έAb%A(μAbGA(έAb%A(ρAb%A–κAb%A(όAb"A–όAb%A(εAb"A4)I3)A4PI3[A40IHAA4¿A)–A4έAb*A4λAb€A4λAb$A4ηAb$A4ηAb€A4ηAb$A3μAb$A3μAb€A4έAb$A4κAb€A4ρAbzA4ñAb*A4…A7όA4EIHAA42I3Kb@)I3)A4)I3PA44I31A4]I45A(bAb$A(IAb”A–bAbzAzwAbzA(EAbzA–/Ab:A(/AbzA(1AbzA(EAbXA(]Ab*A4}AY”A4IIHAA4[I3RA3)I3)A4PI32A41IHIA4%IA“A(.Ab*A(4AbDA()Ab:A()Ab+A()Ab'A–PAb'A–2Ab'A7[Ab'A(]Ab'A(]Ab+A(]Ab'A(KAb'AzKAb+A–RAb+A(3Ab'A––Ab;A(–Ab+A(5Ab;A(5Ab+A(qAbDAz"Ab;A–%Ab;A7GAbDA(NAb;A(9AbDA(NAbDA(NAb;A(jAb;A–jAbDA–HAbDA(7AbLA(7AbDA7BAbLA(MAbLA(MAbDA(XAbLA(LAbXA(+Ab“A43I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4уAz=A(YAb*A(DAbjA–'AbXA–:AbXA–zAbXA(“AbMA–“AbXA(”AbMA(”AbXA(€AbMA(€AbXA($AbMA(¢AbBA($AbMA(¢AbMA(−AbBAz_AbBA–QAbBA(VAbBA–VAbMA–YAb7A(!Ab7A(!AbBA(#AbBA(!Ab7A–&Ab7A(&AbBA(*Ab7A(&AbBA(<Ab7A(*Ab7A–<Ab7A(=AbHA(>AbHA(>Ab7A(&Ab%A(∩Ab&A4*Aε∩A4AIHAA4[I3]AÂ)I3)A4PI32A4wIHAA4;IA_A(╗Ab−A(^AbqA–}AbjA–~AbjA(•AbjA(•Ab9A(…Ab9A(•Ab9A(…Ab9A(£Ab9A(|Ab5A(όAb#A4•AΚόA4AIHAA4[I3.I:)I3)A40I31A(…A)[A(μAbBA(×Ab%A(ΚAbNA(ΚAbGA–αAbGA(λAb%A7λAbGA(ηAbGA(μAb%A–μAbGA–έAb%A(ρAb%A(έAb%A(κAb"A(όAb%A(κAb"A(κAb%A(όAb%A4)I3)A4PI3[A40IHAA4¿A)–A4μAb*A4αAb€A4λAb¢A4λAb$A4ηAb€A3ηAb$A4ηAb€A3έAb$A3ρAb€A4μAbzA4ñAb*A4…A7όA4EIHAA42I3Kb@)I3)A4)I3PA44I31A4]I45A(IAb$A–IAb“A(IAbzA(bAb“A(bAbzA(bAb“A(wAbzA(EAb:A(EAbzA(/Ab:A–/AbzA(OAbzA(EAbLA(]Ab*A4£AY!A4IIHAA4[I3RA4)I3)A4PI32A41IHIA4%IA“A(.Ab*A(6AbLA((Ab'A7)Ab'A(PAb'A(PAb+A(PAb:A(2Ab'A–[Ab'A(]Ab'A([Ab'A([Ab+A7.Ab+A–KAb+A(RAb+A(RAb;A(RAb+A–3Ab+A(–Ab;A(5Ab;A(5Ab+A(5Ab;A(qAb;A("Ab;A(qAb;A("Ab;A–%AbDA(%Ab;A(GAbDA(NAbDA–GAbDAz9AbDA(jAbLA(HAbLA(HAbDA(HAbLA(HAbDA(7AbLA(BAbDA–BAbLA(BAbDA(MAbDA(XAbXA(+Ab“A43I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4уAz=A(VAb*A(LAbHA(+AbMA(:AbXA(:AbLA–:AbXA–zAbXA(“AbXA(”AbMA–”AbXA(€AbXA($AbBA($AbMA(€AbXA($AbMA(¢AbBA7¢AbMA(_AbMA(_AbBA–QAbMA(VAbBA–QAbMA–YAbBA(YAb7A(YAbBA(!AbBA(!Ab7A(#AbBA(#Ab7A(&AbBA(#AbBA–*Ab7A–<Ab7A(<AbHA–=Ab7A(&Ab%A(»Ab#A4_Aε}A4AIHAA42I3[AΚ)I3)A4PI32A4wIHAA4+IA_A(┐Ab−A(^Ab"A(}AbjA(}Ab9A–~Ab9A(•AbjA(~AbjA–•AbjA(…Ab9A(ÂAb9A(|Ab–A(όAb&A4•AΚσA4AIHAA4[I3.IV)I3)A42I3[A4bIHAA(>A)IA(όAbDA(×Ab"A(ΚAbNA(αAbGA(λAbGA(λAb%A–λAbGA(λAb%A(ηAb%A–μAbGA7έAb%A(ρAb%AzκAb%A(όAb"A4)I3PA44I3EA4∩A)jA4λAb#A4ΚAb€AHαAb$A4λAb$AHηAb$A4ηAb€A4έAb€A4έAb$A4έAb€A4έAbzA4ñAb*A4…A7όA4EIHAA42I3KbΚ)I3)A4(I36A42I3]A(AAb'A(IAb€A(bAbzA(IAbzA(bAbzA(bAb“A(wAbzA–EAbzA7EAb:A(OAb:A(EAbDA(.Ab*A4£AY#A4IIHAA4[I3RA3)I3)A4)I3PA40I3wA4–I4XA([AbVA(6Ab;A((Ab:A–(Ab'A(PAb:A–PAb'A(2Ab'A([Ab'A(2Ab'A([Ab'A(]Ab+A(.Ab+A–]Ab'A(KAb+A–KAb'A(RAb+A(KAb'A–RAb+A(3Ab+A(3Ab;A––Ab;A–5Ab;A(qAb;A(5Ab;A(qAb;A("Ab;A–"Ab+A(GAbDA7GAb;A(GAbDAz9AbDA(jAbDA(jAb;A(jAbDA(jAb;A(HAbDA(7AbLA(BAbDA(BAbLA(BAbDA–MAbLA(;Ab”A43I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4уAz=A(VAb*A(DAbHA–'AbXA('AbLA(:AbXA–zAbMA–zAbXA7“AbXA–”AbMA(”AbXA–$AbMA($AbXA–¢AbMA–−AbBA(_AbBA(_AbMA7QAbBA7VAbBA–YAbBA–!Ab7A(!AbBA(#Ab7A(#AbBA–&Ab7A(*Ab7A(&AbBA–<Ab7A(<AbHA(#Ab%A(ÂAbVA4“IA=A4bIHAA42I3[Aε)I3)A4PI32A4wIHAA4;IA_A(╗Ab−A(ZAb"A({AbjA(|AbjA7}AbjA(~AbjA(•Ab9A(•AbjA(•Ab9A(…AbjA(|Ab5A(όAb#A4•AΚσA4AIHAA4[I3.IΚ)I3)A4.I3KA4AIHAA(:A7╗A(РAb”A(§Ab5A–λAbGA–ηAb%A(ηAbGA(ηAbNA(ηAbGA–έAb%A(μAbGA(έAb%A(έAbGA(ρAbGA(κAb"A(κAb%A(όAb"A4)I3PA44I3EA4¿A)HA4λAb!A3ΚAb$A4αAb$A4αAb¢A4λAb$A4ηAb€A3ηAb$A4μAb$A3μAb€A4ηAbzA4üAb*A4|A7§A4EIHAA42I3Rbε)I3)A4(I36A42I3]A(AAb'A(IAb$A(IAbzA(bAbzA(IAbzA–bAbzA(wAb:A(EAb:A(EAbzA7EAb:A(EAbLA(]Ab*A4ÂAY#A4IIHAA4[I3RA3)I3)A4)I3PA40I3wA4–I4XA([AbYA(6Ab;A((Ab'A()Ab'A((Ab'A((Ab:A()Ab'A(PAb+A(PAb'A72Ab'A–[Ab+A7]Ab'A(KAb'A–KAb;A7RAb+A(3Ab+A–3Ab;A(–Ab;A(–Ab+A(5Ab+A–5Ab;A7"Ab;A7%Ab;A(GAb;A(GAbDA7NAbDA79AbDA(jAbDA(HAbDA(jAbDA(HAb;A(HAbDA(7AbDA(BAbLA(7AbLA(BAbLA(MAbXA(;Ab“A43I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4уAz=A(QAb*A(LAbHA(+AbLA(+AbXA7'AbXA(:AbLA(zAbXA–zAbMA(“AbXA(“AbMA(”AbMA(”AbXA–€AbMA($AbBA(€AbMA–$AbMA(¢AbBA–−AbMA(_AbBA–_AbMA7QAbBA–VAbBA–YAbBA(!Ab7A(#Ab7A(!Ab7A(#Ab7A(#AbBA(&AbBA(&Ab7A(*Ab7A(*AbHA(<Ab7A(#AbGA(•AbQA4DIAQA4wIHAA4PI32IA)I3)A4PI32A4wIHAA4;IA_A(∩Ab−A(^Ab"A–|AbjA(|AbHA–}AbjA(~Ab9A–•AbjA(…Ab9A(•AbjA(`Ab5A(κAb#A4•AΚόA4AIHAA4[I3.bA)I3)A4.I3RA4AIHAA(GAz<A(иAb¢A(§Ab5A(αAbGA(λAb%A(ηAb%A(ηAbGA7μAbGA(έAbGA(μAb%A(έAb%A(ρAbGA(ρAb"A–κAb%A4)I3PA44I3EA4»A)jA4αAb!A4×Ab$A4ΚAb$A4ΚAb¢A4αAb€A4ΚAb$A4ΚAb¢A4λAb€A4ηAb€A4λAb$A4ηAb€A4μAb€A4λAbzA4üAb*A4|A7§A4EIHAA42I3Rbε)I3)A4(I36A42I3]A4йAb:A(AAb$A7IAbzA(bAb:A(bAbzA(wAbzA(wAb:A(wAbzA7EAbzA(/Ab:A(EAbDA(2Ab*A4∩Az`A4IIHAA4[I3RA3)I3)A4)I3PA46I3/A4KI4GA(PAb−A(4Ab'A((Ab'A(4Ab:A((Ab'A7)Ab'A(2Ab'A–PAb'A–[Ab+A–]Ab+A([Ab+A([Ab'A(]Ab'A(KAb+A(RAb+A(KAb'A(KAb+A(3Ab;A(3Ab+A–3Ab;A(3Ab+A(–Ab;A(5Ab+A(–Ab;A(5Ab+A("Ab;A(qAb+A(qAb;A("Ab;A–%Ab+A–GAbDA–GAb;A–NAbDA(9AbDA–jAbDAzHAbDA(7AbDA(BAbLA(MAbLA(BAbXA(+AbzA4–I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4РAz>A(_Ab*A(XAbHA–;AbLAz'AbXA7:AbXA–zAbXA(“AbXA–”AbMA7€AbMA($AbMA($AbBA(¢AbBA(¢AbMA(−AbBA(_AbBA(−AbBA(−AbMA(QAbMA7QAbBA–VAbBA(YAb7A(YAbBA7!AbBA(#AbBA(&AbBA(#Ab7A–*Ab7A(#Ab9A(|Ab$A47IA:A4/IHIA4PI32I4)I3)A4PI32A4wIHAA4;IA_A(∩Ab−A(ZAb"A({AbjA(|AbjA({AbjA–|AbjA(}AbHA(}AbjA(~AbjA(~Ab9A(•AbjA(`Ab5A(κAb#A4•AΚόA4AIHAA4[I3.b3)I3)A4.I3RA4AIHAA(4AYDA(®AbQA(┐Ab–A(λAbNA(λAbGA(ηAbGA(μAb%A(ηAb%A(μAbGA–έAb%A(έAbGA–ρAb%A(κAb%A4(I36A4∩A)MA4×AbYAH×Ab¢A3ΚAb$A4αAb$A4αAb€A3λAb€A4λAb$A3ηAb$A4λAbzA4εAb*A4{A7×A4EIHAA42I3RwA)I3)A4(I3(A4(I34A4кAbXA(bAb¢A–IAbzA(IAb“A(bAb“A–bAbzA–wAbzA–EAbzA(EAb:A(wAbDA(2Ab*A4¿Az{A4IIHAA4[I3RA:)I3)A44I31A4[I33A((AbzA()Ab:A(4Ab'A((Ab:A((Ab'A()Ab:A–PAb'A(PAb:A72Ab'A([Ab+A–[Ab'A(.Ab+A(.Ab;A(.Ab+A(.Ab'A–KAb+A(RAb+A–3Ab+A(RAb+A(–Ab+A(3Ab;A(5Ab+A(–Ab+A–5Ab;A(5Ab+A(qAb;A("Ab;A(%Ab;A("Ab+A–%Ab;A7GAbDA–9AbDA(9Ab;A–jAbDA–HAbDA(HAb;A–HAbDA(7AbLA(BAbXA(;Ab”A43I49A40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4РAz>A(_Ab*A(XAbHA(;AbXA(;AbLA('AbLA7'AbXA7:AbXA–zAbXA(“AbMA(”AbMA(”AbXA(”AbMA(”AbXA(€AbMA(€AbXA($AbMA($AbXA–¢AbMA(−AbMA(−AbBA–−AbMAzQAbBA–VAbBA(YAb7A(!AbBA(YAbBA(!AbBA(#Ab7A(#AbBA(&Ab7A(#Ab7A(>Ab;A4–I4GA40I3/A4)I3PIH)I3)A4PI32A4wIHAA4;IA_A(¿Ab_A(@Ab%A({AbjA–{AbHA({AbjA7}AbjA7~AbjA(`Ab5A(κAb#A4•AΚόA4AIHAA4[I3.bV)I3)A4]I3KA4AIHAA4κA£OA)bAbYA(┐AbRA(ηAb%A(ηAbGA(μAb%A(μAbGA(έAb%A(μAb%A–ρAb%A(ρAbGA4(I36A4∩A)MA4ΚAbYA4┐Ab$A4§Ab¢A4×Ab$A4×Ab¢A4αAb$A4ΚAb€A4αAb$A3αAb€A4λAb$A4λAb€A4αAb:A4üAb*A4@Az…A4EIHAA42I3Rw4)I3)A4(I3(A4(I34A4кAbXA(IAb¢A(AAbzA–AAb“A(IAbzA(IAb“A(bAbzA–wAbzA(EAb:A(wAb:A(wAbzA(wAbDA(2Ab*A4¿Az{A4IIHAA4[I3RAV)I3)A4(I36A4PI32A(1AbDA((Ab“A–(Ab'A()Ab'A()Ab:A7PAb'A(2Ab'A(2Ab:A([Ab:A–[Ab'A([Ab+A(]Ab+A(]Ab'A–.Ab+A7KAb+A(RAb'A(RAb+A(–Ab;A(–Ab+A––Ab;A–5Ab;A(qAb;A(qAbDA–qAb;A("Ab;A(%AbDA(%Ab;A(GAb;A–GAbDA–NAbDAz9AbDA–jAbDA(HAbDA(7AbLA(HAbDA(7AbLA(DAb”A43I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4ñAz>A(_Ab*A(LAbHA(;AbLA(;AbXA(;AbLA(+AbLA(+AbXA–'AbXA(:AbXA('AbXA(:AbMA7zAbXA(“AbXA(”AbMA(”AbXA(”AbMA(€AbMA–$AbMA($AbXA–¢AbMA–−AbMA(−AbBA(−AbMA(QAbMA(QAbBA(QAbMAYVAbBA(YAbMA–!AbBA(#AbMA(*AbMA4.I3RA46I30IV)I3)A4PI32A4wIHAA4;IA_A(»Ab_A(?Ab%A(`AbjA(`AbHA({AbHA–|AbjA(|Ab9A–}AbjA–~AbjA(`Ab5A(ρAb&A4~AΚσA4AIHAA4[I3.bÂ)I3)A4]I3]A4AIHAA4£AΚρA)bAbVA(§AbKA(μAb%A(ηAbGA7μAbGA(έAbGA(ρAb%A4(I36A4¿A)XA4§AbYA3§Ab$A4×Ab¢A4ΚAb$A4×Ab$A4ΚAb¢A4×Ab¢A4ΚAb$A3λAb$A4αAb$A4ΚAb:A4εAb*A4@Az…A4EIHAA42I3Rw4)I3)A4(I3(A4(I34A4кAbMA(IAb¢A–AAbzA–AAb“A(IAbzA(bAbzA–bAb“A(wAbzA–wAb“A(/Ab:A(wAbDA(PAb*A4§A7¿A4bIHAA4[I3RAV)I3)A4)I3(A44I30A(/A)HA(PAb$A((Ab+A–(Ab'A()Ab:A()Ab'A–PAb'A–2Ab+A(2Ab'A–[Ab'A([Ab+A(]Ab+A(.Ab+A–.Ab'A(KAb'A(KAb+A(RAb+A(3Ab+A–RAb+A(3Ab+A(–Ab;A(–Ab+A–5Ab;A(qAb+A–qAb;A("Ab;A7%Ab;A(%AbDA(GAbDA–GAb;A(NAbDA(9Ab;A(9AbDA–jAbDA(HAbDA(HAbLA–HAbDA(7AbLA(LAb€A43I49A40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4ñAz>A(¢Ab*A(XAbHA–;AbLA–;AbXA–+AbXA(+AbLA(+AbXA(:AbMA7:AbXA(zAbXA(“AbXA–”AbMA(”AbXA(€AbMA(€AbBA(€AbMA(¢AbBA($AbMA(¢AbBA(¢AbMA(−AbMA(−AbBA–−AbMA(_AbBA(_AbMA–QAbBA7VAbBA(=Ab+A(:A)[A41I3EA4PI3PIΚ)I3)A4PI32A4wIHAA4;IA_A(¿Ab−A(?Ab"A(`AbjA–`AbHA({AbjA({AbHA({AbjA(}AbjA(}Ab9A–}AbjA(`Ab5A(έAb#A4~AΚσA4AIHAA4[I3.bε)I3)A4[I3[A4AIHAA4<Aε~A)IAb−A(§Ab3A(ηAbGA(μAb%A(έAbGA–έAb%A4╗Ab−A4╗Ab¢A4┐Ab$A3§Ab¢A4§Ab$A4×Ab¢A4§Ab¢A4×Ab$A3ΚAb$A3αAb$A4αAb€A4αAb:A4σAb*A4@Az…A4EIHAA42I3Rw3)I3)A4)I3PA46I3/A4РA)NA(IAbQA–AAbzA(IAb“A–IAbzA(bAbzA7wAbzA(wAb:A(EAb:A(wAb;A(PAb*A4§A7¿A4bIHAA4[I3RAΚ)I3)A42I3]A4/IHAA4иA5OA([Ab!A(4Ab+A()Ab'A(PAb'A(PAb+A(PAb'A72Ab'A–[Ab+A7]Ab+A(.Ab+A7KAb+A(RAb;A(RAb+A(3Ab;A(RAb+A(3Ab+A(–Ab;A(3Ab+A–5Ab;A–qAb;A(qAb+A(qAb;A(%Ab;A–"Ab;A–GAb+A–GAb;A–NAb;A–9AbDA(jAbDA(jAbLA(HAbDA–7AbLA(LAb”A43I4NA40I3/A4)I3PA3)I3)A4]I3RA4AIHAA4ñAz?A(−Ab*A(BAbHA(LAbLA–DAbLA(;AbXAz+AbXA('AbXA–:AbXA(zAbXA(:AbMA(“AbMA(zAbXA(“AbXA(“AbMA(”AbMA(”AbXA–€AbMA–$AbMA($AbBA(¢AbBA(¢AbMA(−AbMAz_AbBA(_Ab7A(?Ab¢A(%A–ñA4AIHAA4[I3.b4)I3)A4PI32A4wIHAA4;IA_A(»Ab_A(?Ab%A–^AbHA({AbjA(`AbHA({AbHA(|AbjA(}AbjA(}Ab9A(|AbHA(}AbjA(ZAb5A(μAb&A4~AΚσA4AIHAA4[I3.w4)I3)A42I32A4IIHAA4“IAQA(иAb€A(ΚAb3A(ηAbGA(έAb%A(έAbG®ε)I3)4H)I3)A4"IÂIA(!EHwA)3/Κ/A)b/31A4§bÂ/A(€E40A)%/V)A)I/4PA4┐bÂ1A40I36A4PI3PA4PI3)IA)I3)A44I3)A42I3)A(Dw39A)DEΚ”A4GI:2A4OI4(A4PI3)AΚ)I3)A4[I3PA4wI44A4:IVRA)Ow:@A(РwH=A4AAΚEA4RIH2I@)I3)A4]I32A4AI3OA4£I:+A(ÂIεΚA)(b3сA(%IΚ?A4AI4wA4KI32A42I3PA4bI31A4zIHGA(κI@сA(PI4`A(BIH»A)#Iü9A4zAÂMA4(I3).Κ)I3)A44I4)A(»EΚbA)&OVEA)*OV1A)*O:0A)*O:4A)*OH)A)#O3PA)*O3]A)%/V[A4£b:PA4AAε)A4]IH)IA)I3)A44I3)A42I3)A(Dw39A)*/4¢A49I:2A4/I4(A4PI3)AΚ)I3)A4[I3PA4wI44A4:IVRA)Ow:@A(РwH=A4AAΚEA4RIH2IV)I3)A4KI32A4AI4EA((IÂ!A)−bYOA)*b£(A)VbY(A("IÂ@A4AI4wA4]IHPA43I4KA4.AΚRA4QI:9A)'bIKA(qIH•A(BI:ïA)&bI9A4}AΚ€A4)I3)A4(I3)I:)I3)A44IH4A4RAεKA4HAHNA46IH4A4PI3)[Κ)I3)A4%IΚAA)−O:EA(α/AEA4RIH)A4üwAOA)VO36A(`EV0A4(I3(A4Рbε)A)*OH]A(.wH2A4AA@)A4HI@4A(KwHPA)5/4qA)7/HGA(¿E35A4∩b:[A4EIA)A4]IH)A41I4)A4qI:PA(DwH"A(×EA7A(_wV9A('w39A)*/A$A4jIV2A4IIA4A4όbH%A(κwΚzA)BEHQA)1EA−A4εb39A4]I3PA44I3)A4PI3)A4)I3)A4[I3PA4wI44A4zIV3A)Iw:?A)4wV^A4κIΚXA(ΚwA>A(”bVVA4£IÂBA4AI40A4BI:KA)*wÂρA(Âb@`A42I3PA4EI44A(╗b@}A)*w:®A4−IV"A4AI40A42I3PA4)I3)A4.I32A4AI4OA4σI@”A)“b£wA)0bHñA4*IHBA4EI30A4(I3(A4qI4RA(RIH^A)!bz.A)wIüAA4XAΚHA(∩IÂσA(]I3{A(9I3£A)*Iü7A)&Iü7A4•AΚ¢A4)I3)A4BA@9A(#I4όA)HIYGA)”IzDA4^I3'A4AI3AA(0IA~A)(IIGA)LI('A)KI(7A(1AVïA42AÂKA4/I:OA4'AεHA(>AYEA)*A£•A)IAαjA4AIHAA47I4"A(“A3йA)[Az€A)"AzYA(|A–[A4LA4MA4(I3)[3)I3)A4LbAIA)_OVwA(|EÂbA4KIH)A4§bΚOA)VO34A(“E41A4EI44A4κbÂ(A)*O3]A(]w3]A4AAΚ0A(ïE:[A)*O4"A(×EVRA(−wΚKA)5/AGA)“/:jA(IbεKA4AAε4A4|bH2A)z/4LA)_/3+A)/E:XA)DEε'A(<wV7A)*/A¢A4%I:2A4кbV%A)”EVVA)!EΚ!A(<wH;A)RE4QA)*/A`A(GbΚDA4(I3PA4(I3)A4PI3)A4[I3PA4wI44A4“IV3A(уwH=A)HwÂ|A(…bε#A)*EA×A)*wΚ×A)”w@┐A4®Iε'A4NI:]A)*wÂόA(ZbV@A42I3PA4/I44A(∩b@}A)*wH®A4−IV"A4AI40A42I3PA4)I3)A4KIHPA4AAΚ6A(`bA»A)*wIRA(1IΚVA4AI4wA4KIH2A40IAPA(2IHZA)*bZ"A)7b–6A4иI3&A4|IA“A)*b–jA(¢I:┐A(jIH£A)*bIjA(<IHέA4”A@XA4wI40A(сIZ/A)*I£:A(YI3όA(иI–)A4+I3GA("I3¿A)*I7!A)AI(KA(%AΚ×A(ηAü)A)*Aü>A(3I4╗A4bAε0A(~AZ0A)*Aü^A)PAZ+A(zAΚРA4[I42A(έA7"A)YAY}A(|AzPA(•A7]A)*A7∩A)MA7?A4;A4MA46I44[4)I3)A4LbAAA)_OVwA(ÂEΚbA4KIH)A4§bÂOA)VO34A(−E31A4OI44A4κbÂ(A)*OH]A4иbε[A4£b:PA)_/ε–A(zwΚ]A46IH6A4bIA)A4QIε2A)–/ANA)wE@NA4GIV(A(σE3jA)X/ALA4@bA]A44I3)A42I3)A(GwANA)*/3−A4]IHPA)KEH”A(όwΚ:A4HIV[A4(I3)A4AAΚ1A(όw@¢A)*EV@A4…bA"A4AIA6A4]IHPA4[I3PA4EI44A4+IVRA(уwH=A)–w@|A4“I:qA4bI46A4MI:KA(ñw4{A)jw:¿A4+I3"A)*wÂέA(Yb:=A42I3PA4/I44A(•bV{A)*w:йA4−IV"A4AI40A32I3PA4(I3(A4NI4–A)wbHρA)(b:üA4−IH9A4/I36A40I34A4MI35A(×IΚέA)+b–4A4╗I3”A4AI3bA4>I:MA)*b(jA($I:┐A(NIHÂA)#Iü9A4DAÂ7A44I3(A4кIA?A)*I£DA(OAε|A4[I4[A40IH6A4“AÂMA)GI7HA(×Aü1A47Aε%A41I:0A4EAÂ)A(ïAα6A)/AüGA4ηA:?A)RAα;A)1AZBA4KA@3A4EI40A4κA3|A)*AZ…A(AA:ïA41IH6A4)I4)A4*A3€A)&A7¿A(•A(3A4RI4.A40I36[A)I3)A4LbAAA)_OVwA(╗EεwA4RI:)A4§bÂOA)QOH6A(QE31A41I4(A4όbε(A)*OV]A4όbÂ2A(Pw4]A)+/ÂRA4£b:PA4AAε)A4PI3)A4[IH(A(−wÂ3A)G/A9A4ηb@]A)]EΚBA(•wε9A4IIA(A3PI3)A(3wAGA)*/A−A4=IΚKA)zEÂ−A(=wHDA)7EHQA)*EΚ<A)&E@*A)QE:<A)*EÂ`A4кbHjA4AAε1A4.IHPA42I3PA4EI44A4MI:KA(кwH?A(сwH>A4AAΚEA4RIHPA41I4(A4κIΚ;A)¢w@×A4όIΚ;A)−wVλA(Vb:<A42I3PA4/I44A(?b:ZA)*w:йA4_IV"A4AI40A42I3PA4PI3)A4.IHPA4AAÂ(A(┐b3┐A)”bZwA4…I:;A4AI31A4/I36A4−IH9A)2b(AA)EbAкA4/AÂ[A4II3OA4*I:BA)*b(jA(€I:╗A(–IH•A)#bINA4DAÂ7A40I34A(”IHαA)”IZHA4:IHGA4EI30A41I36A4»Aε_A)$I7:A(€AÂόA4PAε[A4]IH2A4AI3AA("I4§A)AAα%A(XAÂκA)DAα−A(ïII6A4AIHAA4"IA–A(BA:üA)_AZ^A(YAzEA)*AY»A)&Az£A)*A7ïA)*A7∩A)[A7VA4qI43A4OI30A4PI3)2ε)I3)A4LbAIA)_O:wA(α/AwA43I:)A4ΚbΚOA)VO34A(QE31A4OI44A4уbε)A)*OV]A4РbΚ2A4έb@2A)z/Â3A(IwA)A4AAε0A4[I3PA42IH4A(“w@3A)M/4HA4μb@]A)AEVjA)7/ALA40I36A4(I3)A4.IHPA)(EH+A)9EV“A4)I3)A)jEV$A)5EH¢A4ïb4qA4¢IÂRA4*IÂ–A4#IÂ–A4@IΚqA49I:]A40I4(A4PI3)A42I3)A46I3(A4.I32A(^bεVA)3w@{A4"I3KA40I34A4RIH[A(Lb:QA)+wV╗A4#I:9A);w:ΚA(…bÂ^A42I3PA4/I44A(Zb:^A)*wHкA4−IV"A4AI40A42I3PA4)I3)A4KI32A4AI4/A(0IΚVA)*bü6A(×b4αA4MI4"A4AI3EA4QIHjA)2b(AA)EbAкA4/AÂ[A4II3OA4*I:BA)*b(jA(”IV╗A(PI3{A)&Iü9A4zAÂMA44I3(A4ñIA=A)&I£LA(6Aε~A4[I4[A41IH6A4€AÂXA)GI7HA(ηII0A4XIAGA4EI:OA4KAÂKA(έAα]A(кAü–A(wAVÂA)VA£<A(§Aü)A4AIHAA4PIA2A4РAH~A)*AY»A(”A:®A4QA3:A4*A3$A4&A4”A4&A4€A4=A4−A4[I42A4(I3([A)I3)A4LbAIA)_O:wA(α/AwA4RI:)A4μbΚ1A)YO36A(QE31A4/I44A4®w4(A)*O:]A(0w4[A4[IH4A)E/A.A):/@5A(/w42A(2w3[A(?EA3A(^wε5A)'/37A4Zb3PA4ñb@KA)*/V+A(üEH7A(%w3"A(¿wεBA)*/4€A(3bεNA4(I3)A()bÂNA)!EεQA(ρwΚ:A(6b@9A(αwV”A(§w:€A4−IÂRA4II44A4[I3)A3)I3)A4]I3PA4AIA0A4…IεNA)MwÂ•A)Aw3ZA4кbA;A(_bVVA)*wÂαA(&b@&A4PI3)A(┐b@{A)&wVκA(∩b@{A(ïb@|A)¢w3σA)*w:кA4”IVqA4AI40A42I3PA4)I3)A4PI3PA4PIH)A4PIA]A(*IΚïA)*bα]A)5bHйA(…Iε×A(“IÂ…A)wb4уA)1bAйA4OAÂ[A4II3OA4*I:BA)*b(HA(;IH»A4YAÂ;A)*IüHA(ñIYIA(OIA`A40I34A(ΚI:®A)*I£“A(»I3йA)2I––A4:IHGA(7I4§A)*I7&A)II(RA(LAÂέA)bII5A)*I(`A(bI4|A4=I4'A)*AαÂA(ΚIIPA4AI3AA44I3(A4LIANA(ñA79A)*AYÂA(ñAzHA(GA3üA)9Az*A((A4αA42I3PA44I3([4)I3)A4;bAIA)_OHEA(α/4EA4KI:)A4üwAOA)#OH4A(QE30A4EI44A(ww4)A)*O:]A(KwH[A4AAV(A4^b3)A(®EΚRA)*/εGA)*/Κ9A)IEÂ"A(>wε–A)”/HHA4Zb42A4(I3)A4ηbVKA)bE:MA)€/A'A(уE3LA4кb@5A4PI3)A4)I3)A41I4(A(IbVGA).E3$A)*EÂ&A)zE:#A(+bεDA4jI:]A4OI4(A42I3)AH)I3)A4[I3PA4AI46A4QI@5A(ñw4?A)zwΚ»A)Gw:£A(Xb:_A4EI44A4(I3)A4.I32A(∩b@{A)QwHκA)Gw4ΚA)VwHεA)&wHРA4“IV5A4II40A42I3PA3)I3)A4PI3)A4PIH)A4(IA[A(OIV&A)–b:иA)3bH®A(`IΚ§A)6b4иA)ObAиA4OAÂ[A4II3OA4*I:BA)*b–HA(;I:¿A44I3(A([I4}A)4IZ4A(…I:ñA4–I3.A4AI3OA(€I3λA)"IY"A)*IY”A4~I3“A4AI3AA(qIA∩A)XI–;A)YI–−A)BII'A(3AV×A4AAÂEA4ρI3<A)*A£ïA(§AüPA4AI3AA43I3.A4/I30A4NI45A(`A7(A)€AY^A)*Az£A)(A7$A4§A4@A4PI3PA4(I3(Rε)I3)A44I3(A4]I3PA(IIε“A4σIÂ:A4ηIÂ'A(йbÂ¿A)9bερA4'I:–A4bI40A42I3P"@)I3)A46I3(A4[I3PA(:b3&A)&w:σA)*wHεA)RbεΚA4уI@”A4]I32A46I3(%A)I3)A4−IH9A4¢I39A42I3PA4(I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)®ε)I3)N:)I3)""")

def startup():
    w, h = resolution(res2pix(256, 1))
    draw(resize(logo(), 256, w, h), w)
    time.sleep(1.5)

startup()
    

