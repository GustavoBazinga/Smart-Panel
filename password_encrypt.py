from App import App
import os
from Utils import Utils



if __name__ == "__main__":  
    
    Utils.create_default_folders()

    Utils.check_config_file()
    
    try:
        appp = App()
        appp.mainloop()
    except Exception as e:
        print(f"An error occurred while trying load the application: {e}")