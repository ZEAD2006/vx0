# VX0 Tool

VX0 is a simple and easy-to-use tool designed for **subdomain enumeration** and **web archive data collection**. It helps you discover subdomains, filter live ones, and extract valuable data from the Wayback Machine.

---

## Features

- **Subdomain Enumeration**: Collect subdomains using popular tools like `amass`, `subfinder`, and `assetfinder`.
- **Web Archive Data**: Fetch historical data from the Wayback Machine using `curl`.
- **Live Subdomains**: Filter and check live subdomains using `httpx`.
---

## Installation

1. Make sure you have (Python3) installed on your system.
2. Clone the repository:
   ```bash
   git clone https://github.com/username/vx0-tool.git
   cd vx0-tool
   sh install.sh
   python3 vx0.py -d example.com -a\-b\-c
