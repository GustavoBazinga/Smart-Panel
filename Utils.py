import os
import datetime
from tkinter import messagebox
from cryptography.fernet import Fernet


class Utils:


    @staticmethod
    def config(key, decrypt=False):

        with open("./_internal/config.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if key in line:
                    response = line.split("=", maxsplit=1)[1].replace("\n", "").replace("'", "").replace('"', "").strip()
                    if decrypt:
                        cipher_suite = Fernet(open("./_internal/src/default/secret.key", "rb").read())
                        response = cipher_suite.decrypt(Utils.config("SPOTIFY_PASSWORD"))
                        response = response.decode("utf-8")
                    return response
        return None

    @staticmethod
    def create_default_folders():
        try:
            if not os.path.exists("./_internal"):
                os.mkdir("./_internal")
            if not os.path.exists("./_internal/src"):
                os.mkdir("./_internal/src")
            if not os.path.exists("./_internal/src/default"):
                os.mkdir("./_internal/src/default")
            if not os.path.exists("./_internal/src/assets"):
                os.mkdir("./_internal/src/assets")
            if not os.path.exists("./_internal/src/default/secret.key"):
                key = Fernet.generate_key()
                with open("./_internal/src/default/secret.key", "wb") as f:
                    f.write(key)
        except Exception as e:
            Utils.log(f"An error occurred while trying to create the default folders: {e}")




    @staticmethod
    def check_config_file():
        current_ip = os.popen("ipconfig").read()
        current_ip = current_ip.split("IPv4")[1].split(":")[1].split("\n")[0].strip()

        def set_api_ip():
            with open("./_internal/config.txt", "r") as f:
                lines = f.readlines()
            with open("./_internal/config.txt", "w") as f:
                for line in lines:
                    if "API_IP" in line:
                        f.write(fr"API_IP='{current_ip}'" + "\n")
                    else:
                        f.write(line)

        def create_file():
            Utils.log("Creating the configuration file")
            with open("./_internal/config.txt", "w") as f:

                f.write("LINK_DRIVE='https://drive.google.com/drive/u/1/folders/1fPrFnbURqeJGgq0LcBexrruELP_JGu3W'" + "\n")
                f.write("WITH_SPOTIFY=False" + "\n\n")
                f.write("ACCOUNT_USERNAME=''" + "\n")
                f.write("SPOTIFY_PASSWORD=''" + "\n")
                f.write("SKY_ACCOUNT_USER=''" + "\n\n\n")
                f.write("----XPATHS----"+ "\n\n\n")
                
                f.write("SKY_LOGIN_INPUT=" + "\n")
                f.write("SKY_PASSWORD_INPUT=" + "\n")
                f.write("SKY_ACCESS_BUTTON=" + "\n")
                f.write("SKY_ACCONUT_USER=" + "\n")
                f.write("SKY_SPAM_CLOSE=" + "\n")
                f.write("SKY_SPORTS_REF=" + "\n")
                f.write("SPOTIFY_LOGIN_INPUT=" + "\n")
                f.write("SPOTIFY_PASSWORD_INPUT=" + "\n")
                f.write("SPOTIFY_ACCESS_BUTTON=" + "\n")
                f.write("SPOTIFY_PLAY_BUTTON=" + "\n")
                f.write("SPOTIFY_DAILY_PLAY=" + "\n")
                f.write(fr"API_IP='{current_ip}'" + "\n")

            Utils.log("Configuration file created successfully")
            
        
        if not os.path.exists("./_internal/config.txt"):
            Utils.log("O arquivo de configuração não foi encontrado. Criando arquivo de configuração básico... Necessário acionar a TI para funcionamento do SPOTIFY e SKY+")
            create_file()

        set_api_ip()

        
    @staticmethod
    def clear_folder(folder):
        try:
            Utils.log(f"Cleaning the assets folder")
            for file in os.listdir(folder):
                os.remove(folder + "/" + file)
            Utils.log(f"Assets folder cleaned successfully")
        except:
            Utils.log(f"An error occurred while cleaning the assets folder: {e}")

    @staticmethod
    def log(msg: str):
        #Check if the logs folder exists, if not, create it
        if not os.path.exists("./logs"):
            os.mkdir("./logs")
        today = datetime.datetime.now()
        today = today.strftime("%Y_%m_%d")
        with open(fr"./logs/{today}.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {msg}\n")
            print(f"{datetime.datetime.now()} - {msg}")
    
    @staticmethod
    def check_internet():
        Utils.log(f"Checking internet connection...")
        try:
            import requests
            response = requests.get("https://www.google.com")
            Utils.log(f'Internet connection is OK')
            return True
        except:
            Utils.log(f'No internet connection')
            return False