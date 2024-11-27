import ctypes
import os
import pyautogui
import requests
import subprocess
import time
import tkinter as tk
import vlc
from config import *
from googledriver import download_folder
from Spotify import Spotify
from Utils import Utils
from dotenv import load_dotenv
from tkinter import messagebox
from sys import exit

load_dotenv()

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.window_state = "normal"
        self.binds()
        
        #     if WITH_SPOTIFY:
        #         self.spotify()
        self.start_player(loading_media=True)
        self.after(10, self.__remove_window_frame)

        #Wait all code before this
        if Utils.check_internet():
            self.after(5000, self.stop_video_and_update)
            #Wait code below

    #Function to store all program binds pool
    def binds(self):
        self.bind("<Unmap>", self.__on_window_state_change)
        self.bind("<Map>", self.__on_window_state_change)

    #Function to create and configure a VLC Media Player with the Canva
    def start_player(self, loading_media=False):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.media_list_player = self.instance.media_list_player_new()
        self.media_list_player.set_playback_mode(vlc.PlaybackMode.loop)
        self.frame1 = tk.Frame(self, bg='black', width=1920, height=1)
        self.frame1.pack()
        self.media = tk.Canvas(self, bg='black', highlightthickness=0, width=1920, height=1080)
        self.media.place(x=0, y=0)
        self.media.pack()
        self.frame1.bind("<Button-3>", self.__context_menu)
        if loading_media:
            self.load_media(state="loading")
        else:
            self.load_media()
        self.play()
    
    #Function to upload videos and set the media list
    def load_media(self, state="normal"):
        try:
            if state == "normal":
                self.videos = [f'./_internal/src/assets/{file}' for file in os.listdir('./_internal/src/assets')]
            elif state == "loading":
                self.videos = [f'./_internal/src/default/{file}' for file in os.listdir('./_internal/src/default') if file == "loading.mp4"]
            self.media_list = self.instance.media_list_new()
            try:
                for video in self.videos:
                    self.media_list.add_media(self.instance.media_new(video))
                self.media_list_player.set_media_list(self.media_list)
                self.media_list_player.set_media_player(self.media_player)
            except Exception as e:
                Utils.log(f"An error occurred while loading the media: {e}")
        except Exception as e:
            Utils.log(f"An error occurred while starting the media player: {e}") 
            return False   
        else:
            print("Media loaded successfully")
            return True
        

    def play(self):
        self.media_player.set_fullscreen(True)
        self.media_player.set_hwnd(self.media.winfo_id())
        self.media_list_player.play()

    #Function to call a update list function using tkinter.after
    def update_videos(self):
        if self.load_media(state="loading"):
            try:
                self.after(1000, self.stop_video_and_update())
            except Exception as e:
                Utils.log(f"An error occurred while stop media player: {e}")

    #Function to stop de media player, delete all files in assets directory and download new medias from google drive.
    def stop_video_and_update(self):
        try:      
            Utils.clear_folder('./_internal/src/assets')
            download_folder(LINK_DRIVE, './_internal/src/assets')
            self.load_media()

        except Exception as e:
            Utils.log(f"An error occurred while updating assets data: {e}")

    #Function to close de app and all instances
    def destroy_app(self):
        if hasattr(self, "_spotify"):
            self._spotify.end()
            del self._spotify
        self.destroy()

    def spotify(self):
        if not hasattr(self, "_spotify"):
            self._spotify = Spotify(url=fr"https://accounts.spotify.com/pt-BR/login?continue=https%3A%2F%2Fopen.spotify.com%2Fplaylist%2F16F6TQwQ1pZGtRn9s9zXpM")
        else:
            response = self._spotify.on_maximize()
            if response == "closed":
                del self._spotify
                self.spotify()
                

            
        #Function to establish the window state
    def __on_window_state_change(self, event):
        if event.type == tk.EventType.Unmap and self.window_state != "minimized":
            self.window_state = "minimized"
            self.on_minimize()
        elif event.type == tk.EventType.Map and self.window_state != "normal":
            self.window_state = "normal"

    #Function to minimize the main application and all of instances
    def on_minimize(self):
        try:
            self.iconify()
        except Exception as e:
            Utils.log(f"An error occurred while minimizing the application: {e}")

    #Function to open the settings file
    def on_configure(self):
        ctypes.windll.shell32.ShellExecuteW(None, "open", "notepad.exe", fr"C:\Programs Files(x86)\CFCSN\smart-panel\config.txt\config.py", None, 1)

        self.destroy_app()
        self.__init__()

   #Function to create a dialog box in right mouse button with the context menu
    def __context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)

        menu.add_command(label="Spotify", command=self.spotify)
        # menu.add_command(label="Sky+", command=self.start_sky)
        # menu.add_separator()
        menu.add_command(label="Atualizar Vídeos", command=self.update_videos)
        menu.add_command(label="Configurações", command=self.on_configure)
        menu.add_separator()
        menu.add_command(label="Minimizar", command=self.on_minimize)
        # menu.add_command(label="Reiniciar", command=self.restart_app)
        menu.add_command(label="Fechar", command=self.destroy_app)
        menu.post(event.x_root, event.y_root)
        #Function to remove the window border

    def __remove_window_frame(self):
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -16)
        style &= ~0x00C00000  # Remove WS_CAPTION
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -16, style)
        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x0273)

if __name__ == "__main__":
    app = App()
    app.mainloop()
