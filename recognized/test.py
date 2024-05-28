from datetime import datetime, timedelta

start_time = datetime.now()

while True:
    now = datetime.now()
    if now - start_time >= timedelta(seconds=3):
        print(True)
        break
