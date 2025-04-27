# Testbomber
# Advanced SMS Bomber with 10 Threads

This is a Python-based SMS bombing tool that uses multithreading (10 threads) to send multiple SMS to a target number. The tool randomly selects an API and uses it to send SMS.

## Features

- **10 Threads** for fast SMS bombing.
- **Random delay (0.5 - 2.0 seconds)** between requests to avoid blocking.
- **Retry system** in case an API fails to send an SMS.
- **Number format randomization** for better results.
- **Console logs** for success and failure feedback.

## Requirements

- Python 3.x
- `requests` library (can be installed using `pip install requests`)
- A valid list of working APIs (see `apis.py`)

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Joybrobd/Testbomber
   cd sms-bomber
