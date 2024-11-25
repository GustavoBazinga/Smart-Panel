import ctypes
import os
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
        self.window_state = "normal"
        self.binds()
        self.start_player()
        self.after(10, self.__remove_window_frame)
        self.attributes("-fullscreen", True)
        self.after(100, self.media_init)

    def media_init(self):
        if Utils.check_internet():
            self.stop_video_and_update(True)
            if WITH_SPOTIFY:
                self.spotify()

    #Function to store all program binds pool
    def binds(self):
        self.bind("<Unmap>", self.__on_window_state_change)
        self.bind("<Map>", self.__on_window_state_change)

    #Function to create and configure a VLC Media Player with the Canva
    def start_player(self):
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
        if self.load_media(loading=True): self.play()
        
    #Function to load media player with the videos in assets directory
    def load_media(self, loading=True):
        try:
            if loading:
                self.loading_media = self.instance.media_list_new()
                self.loading_media.add_media(self.instance.media_new('./_internal/src/loading.mp4'))
                self.media_list_player.set_media_list(self.loading_media)
            else:
                self.videos = [f'./_internal/assets/{file}' for file in os.listdir('./_internal/assets')]
                self.media_list = self.instance.media_list_new()
                for video in self.videos:
                    self.media_list.add_media(self.instance.media_new(video))
                self.media_list_player.set_media_list(self.media_list)
            self.loaded = loading
            return self.loaded
        except Exception as e:
            Utils.log(f"An error occurred while loading the media: {e}")

    #Function to upload videos and set the media list
    def play(self):
        try:
            self.media_list_player.set_media_player(self.media_player)
            self.media_player.set_fullscreen(True)
            self.media_player.set_hwnd(self.media.winfo_id())
            self.media_list_player.play()
        except Exception as e:
            Utils.log(f"An error occurred while starting the media player: {e}")    

    #Function to remove the window border
    def __remove_window_frame(self):
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -16)
        style &= ~0x00C00000  # Remove WS_CAPTION
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -16, style)
        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x0273)

    #Function to create a dialog box in right mouse button with the context menu
    def __context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        if WITH_SPOTIFY:
            menu.add_command(label="Spotify", command=self.spotify)
            menu.add_separator()
        menu.add_command(label="Atualizar Vídeos", command=self.update_videos)
        menu.add_command(label="Configurações", command=self.on_configure)
        menu.add_separator()
        menu.add_command(label="Minimizar", command=self.on_minimize)
        menu.add_command(label="Fechar", command=self.destroy_app)
        menu.post(event.x_root, event.y_root)

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

    #Function to call a update list function using tkinter.after
    def update_videos(self):
        if Utils.check_internet():
            if self.load_media(loading=True):
                try:
                    self.after(10000, self.stop_video_and_update)
                except Exception as e:
                    Utils.log(f"An error occurred while stop media player: {e}")
        else:
            messagebox.showerror("Sem conexão com a internet", "Verifique sua conexão com a internet e tente novamente.\n"+
                                 "Se o problema persistir contacte o suporte.")

    #Function to stop de media player, delete all files in assets directory and download new medias from google drive.
    def stop_video_and_update(self, init=False):
        try:
            self.after(100, Utils.clear_folder('./_internal/assets'))
            download_folder(LINK_DRIVE, './_internal/assets')
            if self.load_media(loading=False):
                # if not init:
                self.play()
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
                
    #TODO Function to refresh app NAO FUNCIONA
    def restart_app(self):
        self.destroy_app()
        self.__init__()

if __name__ == "__main__":
    app = App()
    app.mainloop()
