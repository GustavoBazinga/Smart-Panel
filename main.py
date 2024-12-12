from App import App
from Utils import Utils



if __name__ == "__main__":  

    Utils.check_config_file()

    Utils.create_default_folders()
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred while trying load the application: {e}")