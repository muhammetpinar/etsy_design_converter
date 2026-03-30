import os
import sys
import threading
import time
import socket
import subprocess

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_base_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # In dev mode, go up one level from 'src' to 'etsy_design_converter'
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_path

def run_streamlit():
    try:
        import streamlit.web.cli as stcli
        
        # Configure path
        base_path = get_base_path()
        app_path = os.path.join(base_path, 'src', 'app.py')
        
        # Make sure parent dir is in sys.path
        if base_path not in sys.path:
            sys.path.insert(0, base_path)
        
        # Configure sys.argv for Streamlit CLI
        sys.argv = [
            "streamlit", 
            "run", 
            app_path, 
            "--server.port=8501", 
            "--server.headless=true", 
            "--global.developmentMode=false"
        ]
        
        # Start Streamlit server
        stcli.main()
    except Exception as e:
        import traceback
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())
            f.write(f"\n{e}\n")

def start_desktop_app():
    # 1. Start Streamlit in a daemon thread
    t = threading.Thread(target=run_streamlit)
    t.daemon = True
    t.start()
    
    # 2. Wait for Streamlit server to start bound to the port
    retries = 30
    while not is_port_in_use(8501) and retries > 0:
        time.sleep(0.5)
        retries -= 1
        
    if retries == 0:
        print("Error: Could not start Streamlit server on port 8501.")
        sys.exit(1)
        
    url = "http://localhost:8501"
    
    # 3. Open UI UI Window (Native Edge App Mode)
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    
    browser_started = False
    
    # Try Edge First
    for path in edge_paths:
        if os.path.exists(path):
            subprocess.Popen([path, f"--app={url}"])
            browser_started = True
            break
            
    # Try Chrome Next
    if not browser_started:
        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path, f"--app={url}"])
                browser_started = True
                break
                
    # Fallback to standard default browser tab
    if not browser_started:
        import webbrowser
        webbrowser.open(url)
        
    # 4. Keep app running so Streamlit background thread continues serving
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    start_desktop_app()
