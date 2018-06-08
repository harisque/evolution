import os
import subprocess
def get_dir():
    login = os.getenv('username')
    return  os.path.join('C:\\','Users',login,'AppData','Local','SWMScr')
def kill():
    os.rename(os.path.join(get_dir(),'swmscr.exe'),os.path.join(get_dir(),'swmscr1.exe'))
    os.system("taskkill /f /im swmscr.exe")
def restore():
    os.rename(os.path.join(get_dir(),'swmscr1.exe'),os.path.join(get_dir(),'swmscr.exe'))
    os.system(os.path.join(get_dir(),'swmscr.exe'))
def main():
    li = subprocess.check_output('tasklist')
    if 'swmscr.exe' in li:
        kill()
    else:
        restore()
if __name__=="__main__":
    main()
