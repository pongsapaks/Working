from datetime import datetime

def log(filename, message):
    with open(filename, 'a',encoding='utf-8') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}\n')