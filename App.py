import ctypes
import os
import time
import tkinter as tk
import vlc
from googledriver import download_folder
from Spotify import Spotify
from Utils import Utils
from tkinter import messagebox
import threading
from flask import Flask

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        t1 = threading.Thread(target=self.__init_app)
        t2 = threading.Thread(target=self.__init_api)

        t1.start()
        t2.start()
        

    def __init_app(self):
        self.window_state = "normal"
        self.binds()
        self.start_player()
        self.after(10, self.__remove_window_frame)
        self.attributes("-fullscreen", True)
        self.after(5000, self.media_init)

    def __init_api(self):
        app = Flask(__name__)
        @app.route('/update', methods=['GET'])
        def api_update():
            Utils.log(f'API Update request received')
            try:
                self.update_videos()
                Utils.log(f'API Update request completed')
                return {"status": "success"}
            except Exception as e:
                Utils.log(f"An error occurred while updating the videos: {e}")
                return {"status": "error"}
        
        @app.route('/restart', methods=['GET'])
        def api_restart():
            Utils.log(f'API Restart computer request received')
            try:
                Utils.log(f'API Restart computer request completed')
                os.system("shutdown /r /t 1") 
                return {"status": "success"}
            except Exception as e:
                Utils.log(f"An error occurred while restarting the computer: {e}")
                return {"status": "error"}
        
        app.run(port=5000, host=fr'{Utils.config("API_IP")}')
        
    def media_init(self):
        if Utils.check_internet():
            self.videos_update()
            if Utils.config("WITH_SPOTIFY") == "True":
                self.spotify()
        else:
            self.load_media(loading=False)

    #Function to store all program binds pool
    def binds(self):
        self.bind("<Unmap>", self.__on_window_state_change)
        self.bind("<Map>", self.__on_window_state_change)

    #Function to create and configure a VLC Media Player with the Canva
    def start_player(self):
        Utils.log(f"Starting the media player")
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.media_list_player = self.instance.media_list_player_new()
        self.media_list_player.set_playback_mode(vlc.PlaybackMode.loop)
        self.frame1 = tk.Frame(self, bg='black', width=3840, height=1)
        self.frame1.pack()
        self.media = tk.Canvas(self, bg='black', highlightthickness=0, width=3840, height=2160)
        self.media.place(x=0, y=0)
        self.media.pack()
        self.frame1.bind("<Button-3>", self.__context_menu)
        Utils.log(f"Media player started successfully")
        if self.load_media(loading=True): self.play()
        
    #Function to load media player with the videos in assets directory
    def load_media(self, loading=True):
        try:
            if loading:
                self.loading_media = self.instance.media_list_new()
                self.loading_media.add_media(self.instance.media_new('./_internal/src/default/loading.mp4'))
                self.media_list_player.set_media_list(self.loading_media)
            else:
                Utils.log(f"Loading the media list")
                self.medias = [f'./_internal/src/assets/{file}' for file in os.listdir('./_internal/src/assets')]
                self.media_list = self.instance.media_list_new()
                for media in self.medias:
                    self.media_list.add_media(self.instance.media_new(media))
                self.media_list_player.set_media_list(self.media_list)
                Utils.log(f"Media list loaded successfully")
            self.loaded = loading
            return self.loaded
        except Exception as e:
            Utils.log(f"An error occurred while loading the media: {e}")

    #Function to upload videos and set the media list
    def play(self):
        try:
            Utils.log(f"Trying to play the media list")
            self.media_list_player.set_media_player(self.media_player)
            self.media_player.set_fullscreen(True)
            self.media_player.set_hwnd(self.media.winfo_id())
            self.media_list_player.play()
            Utils.log(f"Media list played successfully")
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
        if Utils.config("WITH_SPOTIFY") == "True":
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
            Utils.log(f"Minimizing the application")
            self.on_minimize()
        elif event.type == tk.EventType.Map and self.window_state != "normal":
            self.window_state = "normal"
            Utils.log(f"Maximizing the application")

    #Function to minimize the main application and all of instances
    def on_minimize(self):
        try:
            self.iconify()
            Utils.log(f"Application minimized")
        except Exception as e:
            Utils.log(f"An error occurred while minimizing the application: {e}")

    #Function to open the settings file
    def on_configure(self):
        Utils.log(f"Opening the settings file")
        ctypes.windll.shell32.ShellExecuteW(None, "open", "notepad.exe", fr"./_internal/config.py", None, 1)

    #Function to call a update list function using tkinter.after
    def update_videos(self):
        if Utils.check_internet():
            if self.load_media(loading=True):
                try:
                    self.after(5000, self.videos_update)
                except Exception as e:
                    Utils.log(f"An error occurred while stop media player: {e}")
        else:
            messagebox.showerror("Sem conexão com a internet", "Verifique sua conexão com a internet e tente novamente.\n"+
                                 "Se o problema persistir contate o suporte.")

    #Function to stop de media player, delete all files in assets directory and download new medias from google drive.
    def videos_update(self):
        try:
            attempt = 1
            while attempt != 4:
                try:
                    self.after(100, Utils.clear_folder('./_internal/src/assets'))
                    Utils.log(f"Trying to download the videos, attempt {attempt}")
                    if download_folder(Utils.config("LINK_DRIVE"), './_internal/src/assets'):
                        attempt = 4
                        Utils.log(f"Videos downloaded successfully")
                except:
                    attempt += 1
                    Utils.log(f"An error occurred while downloading the videos, attempt {attempt}")
                    time.sleep(5)
            if self.load_media(loading=False):
                self.play()
        except Exception as e:
            Utils.log(f"An error occurred while updating assets data: {e}")

    #Function to close de app and all instances
    def destroy_app(self):
        Utils.log(f"Closing the application")
        if hasattr(self, "_spotify"):
            self._spotify.end()
            del self._spotify
        self.destroy()

        #Stop threads   
        os._exit(0)


    def spotify(self):
        if not hasattr(self, "_spotify"):
            Utils.log(f"Starting Spotify")
            self._spotify = Spotify(url=Utils.config("SPOTIFY_PLAYLIST"))
        else:
            response = self._spotify.on_maximize()
            if response == "closed":
                del self._spotify
                self.spotify()

if __name__ == "__main__":
    app = App()
    app.mainloop()
