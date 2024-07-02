import time
import AOIToolMain
import AOI3DXToolMain
import traceback
import threading

def AOIToolMainImplementRun():
    print("开启AOI")
    AOIToolMain.main()
    

def AOI3DXToolMainImplementRun():
    print("开启3DX")
    AOI3DXToolMain.main()

def main():
    time.sleep(5)
    AOIToolMainImplement = threading.Thread(target=AOIToolMainImplementRun)
    AOI3DXToolMainImplement = threading.Thread(target=AOI3DXToolMainImplementRun)
    AOIToolMainImplement.start()
    AOI3DXToolMainImplement.start()

if __name__ == "__main__":
    main()


















