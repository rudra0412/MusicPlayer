from tkinter import *
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import themed_tk as tk
import os
import time
import threading

root = tk.ThemedTk()
root.get_themes()
root.set_theme('smog')

menubar = Menu(root)
root.config(menu=menubar)

subMenu = Menu(menubar, tearoff=0)

playList = []

statusbar = ttk.Label(root, text='Welcome to melody', relief=SUNKEN, anchor=W, font= 'Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename_path)
    index = 0
    playListbox.insert(index, filename)
    playList.insert(index, filename_path)
    index += 1


menubar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a Music Player build using python Tkinter library by Rudra')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='About Us', command=about_us)

mixer.init()  # initializing the mixer

root.title("Melody")
root.iconbitmap(r'melody.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=30)

filelabel = ttk.Label(leftframe, text='Bs Bajana Chahiye Gana !!')
filelabel.pack(pady=10)

playListbox = Listbox(leftframe)
playListbox.pack()

addbtn = ttk.Button(leftframe,text='-Add', command=browse_file)
addbtn.pack(side=LEFT)


def del_song():
    selected_song = playListbox.curselection()
    selected_song = int(selected_song[0])
    playListbox.delete(selected_song)
    playList.pop(selected_song)


delbtn = ttk.Button(leftframe,text='-Del', command=del_song)
delbtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()



lengthlabel = ttk.Label(topframe, text='Total Duration : --:--')
lengthlabel.pack(pady=10)

currentTimelabel = ttk.Label(topframe, text='Current Duration : --:--', relief=GROOVE)
currentTimelabel.pack()


def show_details(play_song):
    filelabel['text'] = 'Playing' + '-' + os.path.basename(filename_path)

    file_details = os.path.splitext(play_song)

    if file_details[1] == '.mp3':
        audio = MP3(play_song)
        total_duration = audio.info.length

    else:
        a = mixer.sound(play_song)
        total_duration = a.get_length()

    mins, secs = divmod(total_duration, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = 'Total Duration' + '-' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_duration,))
    t1.start()


def start_count(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentTimelabel['text'] = 'Current Time' + '-' + timeformat
            time.sleep(1)
            t -= 1


played = FALSE

def play_music():
    global paused
    global played

    if paused:
        mixer.music.unpause()
        statusbar['text'] = os.path.basename(filename_path) + '  ' + 'Music Resumed'
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playListbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playList[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = 'Playing Music' + '-' + os.path.basename(play_it)
            played = TRUE
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File Not Found', 'Melody could not find the file Pls check again')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = os.path.basename(filename_path) + '  ' + 'Music Stopped'


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = os.path.basename(filename_path) + '  ' + 'Music Paused'


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


def rewind_music():
    play_music()
    statusbar['text'] = os.path.basename(filename_path) + '  ' + 'Music Rewinded'


muted = FALSE


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
        statusbar['text'] = 'Music Unmuted'
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE
        statusbar['text'] = 'Music Muted'


def on_closing():
    tkinter.messagebox.askyesnocancel('Exit', 'Do you really want to quit')
    if played == TRUE:
        stop_music()
        root.destroy()
    else:
        root.destroy()


middleFrame = Frame(rightframe)
middleFrame.pack(padx=30, pady=30)

playPhoto = PhotoImage(file='play.png')
playBtn = ttk.Button(middleFrame, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='stop.png')
stopBtn = ttk.Button(middleFrame, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn = ttk.Button(middleFrame, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

bottomFrame = Frame(rightframe)
bottomFrame.pack(pady=15)

rewindPhoto = PhotoImage(file='rewind.png')
rewindBtn = ttk.Button(bottomFrame, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='mute.png')
volumePhoto = PhotoImage(file='volume.png')
volumeBtn = ttk.Button(bottomFrame, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, padx=30)


root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()
