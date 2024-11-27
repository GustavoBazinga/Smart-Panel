from App import App
from config import *
import os


def create_folder():
    try:
        os.mkdir(fr'C:\smart-panel')
    except:
        pass

if __name__ == "__main__":  
    create_folder()    

    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred while trying load the application: {e}")