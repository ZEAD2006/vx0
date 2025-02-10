# VX0 Tool

VX0 is a simple and easy-to-use tool designed for **subdomain enumeration**, **filtering specific data and subdomains** and **web archive data collection**. It helps you discover subdomains, filter live ones, and extract sensitive data from the Wayback Machine.

---

## Features

- **Subdomain Enumeration**: Collect subdomains using popular tools instead of `amass`, `subfinder`, and `assetfinder`.
- **Web Archive Data**: Fetch historical data from the Wayback Machine .
- **Live Subdomains**: Filter and check live subdomains instead of `httpx`.
---

## Requirements
- pip install colorama
- pip install -r requirements.txt
---

## Installation

1. Make sure you have (Python3) installed on your system.
2. Clone the repository:
   ```bash
   git clone https://github.com/ZEAD2006/vx0.git
   cd vx0
   sh install.sh
   python3 vx0.py -d example.com -a\-b\-c
