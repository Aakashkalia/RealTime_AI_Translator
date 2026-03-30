import webview
import threading
import time
import subprocess
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_streamlit():
    subprocess.Popen([
        "python", "-m", "streamlit", "run", "streamlit_app.py", 
        "--server.headless", "true", "--server.port", "8501"
    ])

if __name__ == '__main__':
    # Start the Streamlit server in a background thread
    t = threading.Thread(target=start_streamlit)
    t.daemon = True
    t.start()
    
    # Wait for the Streamlit server to start up
    print("Starting Translation Engine...")
    while not is_port_in_use(8501):
        time.sleep(1)
        
    print("Engine Ready! Launching Desktop Window...")
    
    # Create the native app window
    webview.create_window('Real-Time AI Translator', 'http://localhost:8501', width=1280, height=800)
    webview.start()
