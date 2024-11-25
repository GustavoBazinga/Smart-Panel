import os
import datetime
class Utils:
    def clear_folder(folder):
        try:
            for file in os.listdir(folder):
                os.remove(folder + "/" + file)
        except Exception as e:
            print(f"An error occurred while cleaning the assets folder: {e}")

    @staticmethod
    def log(msg: str):
        today = datetime.datetime.now()
        today = today.strftime("%Y_%m_%d")
        with open(fr"./_internal/logs/{today}.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {msg}\n")
            print(f"{datetime.datetime.now()} - {msg}")
    
    @staticmethod
    def check_internet():
        try:
            import requests
            response = requests.get("https://www.google.com")
            return True
        except:
            return False
