import argparse
import subprocess
import os
from pyfiglet import Figlet
from colorama import Fore, Style, init

init(autoreset=True)

def print_logo():
    f = Figlet(font='slant')  
    logo = f.renderText('V X 0')
    
    colored_logo = (
        Fore.RED + "=" * 50 + "\n" +
        Fore.GREEN + logo +
        Fore.RED + "=" * 80 + "\n" +
        Fore.YELLOW + "      A simple tool can enumerating subdomains and filtering only working subdomains and collecting a specific data from wayback machine and\n" +
        Fore.RED + "=" * 80 + "\n"
    )
    print(colored_logo)

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[-] Error running command: {e}")
        return None

def filter_subdomains(domain, output):
    """Filter subdomains from the amass output."""
    subdomains = []
    for line in output.splitlines():
        if f"{domain} (FQDN) --> node -->" in line:
            subdomain = line.split("-->")[-1].strip()
            subdomains.append(subdomain)
    return subdomains

def option_a(domain):
    print(Fore.CYAN + f"[+] Collecting subdomains for {domain}...")
    subdomains_file = f"{domain}_subdomains.txt"
    
    # Run Amass
    print(Fore.YELLOW + "⟹ VX0 ⟸")
    amass_output = run_command(f"amass enum -d {domain}")
    
    # Filter subdomains from Amass output
    subdomains = filter_subdomains(domain, amass_output)
    
    # Save subdomains to file
    with open(subdomains_file, 'w') as file:
        file.write("\n".join(subdomains))
    
    print(Fore.YELLOW + "")
    run_command(f"subfinder -d {domain} -o {subdomains_file} -silent")
    
    print(Fore.YELLOW + "")
    run_command(f"assetfinder --subs-only {domain} >> {subdomains_file}")
    
    print(Fore.GREEN + f"[+] Subdomains collected and saved to {subdomains_file}")

def option_b(domain):
    print(Fore.CYAN + f"[+] Collecting web archive data for {domain}...")
    hidden_file = f"{domain}_hidden.txt"
    sensitive_files = f"{domain}_sensitive_files.txt"
    
    print(Fore.YELLOW + "[+] Fetching data from Wayback Machine...")
    
    curl_command = [
        "curl", "-G", "https://web.archive.org/cdx/search/cdx",
        "--data-urlencode", f"url=*.{domain}/*",
        "--data-urlencode", "collapse=urlkey",
        "--data-urlencode", "output=text",
        "--data-urlencode", "fl=original"
    ]
    
    # فتح الملف لتخزين البيانات المسترجعة
    with open(hidden_file, "w") as file:
        result = subprocess.run(curl_command, stdout=file, stderr=subprocess.PIPE)
        
        # إذا حدث خطأ أثناء تنفيذ الأمر
        if result.returncode != 0:
            print(Fore.RED + f"Error running curl command: {result.stderr.decode()}")
            return
    
    print(Fore.YELLOW + "[+] Filtering out images and non-sensitive files...")
    
    sensitive_extensions = ['.js', '.json', '.php', '.xml', '.config', '.env', '.sql', '.bak', '.log', '.yaml', '.yml', '.txt']
    
    with open(hidden_file, 'r') as file:
        lines = file.readlines()
    
    sensitive_links = []
    with open(hidden_file, 'w') as file:
        for line in lines:
            if not any(ext in line for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.css', '.woff', '.ttf']):
                file.write(line)
                if any(ext in line for ext in sensitive_extensions):
                    sensitive_links.append(line.strip())
    
    # Save sensitive files to a separate file
    with open(sensitive_files, 'w') as file:
        file.write("\n".join(sensitive_links))
    
    print(Fore.GREEN + f" Wayback data collected and saved to {hidden_file}")
    print(Fore.GREEN + f" Sensitive files saved to {sensitive_files}")


def option_c(domain):
    print(Fore.CYAN + f" Collecting working links for {domain}...")
    subdomains_file = f"{domain}_subdomains.txt"
    working_links_file = f"{domain}_working_links.txt"
    
    if not os.path.exists(subdomains_file):
        print(Fore.RED + f" Error: File {subdomains_file} does not exist. Run option A first.")
        return
    
    with open(subdomains_file, 'r') as file:
        subdomains = file.read().strip().splitlines()
    
    if not subdomains:
        print(Fore.RED + f" Error: File {subdomains_file} is empty. No subdomains found.")
        return
    
    valid_urls = [f"http://{subdomain}" for subdomain in subdomains] + [f"https://{subdomain}" for subdomain in subdomains]
    
    temp_urls_file = f"{domain}_temp_urls.txt"
    with open(temp_urls_file, 'w') as file:
        file.write("\n".join(valid_urls))
    
    print(Fore.YELLOW + ">>> Waiting for collecting data... <<<")
    run_command(f"httpx -l {temp_urls_file} -silent -o {working_links_file}")
    
    os.remove(temp_urls_file)
    
    print(Fore.GREEN + f" Working links collected and saved to {working_links_file}")

def main():
    print_logo()
    
    parser = argparse.ArgumentParser(description="vx0 - A simple subdomain and web archive data collection tool.")
    parser.add_argument("-d", "--domain", required=True, help="The target domain to scan.")
    parser.add_argument("-a", "--option_a", action="store_true", help="Collect subdomains using Amass, SubFinder, and AssetFinder.")
    parser.add_argument("-b", "--option_b", action="store_true", help="Collect web archive data using curl.")
    parser.add_argument("-c", "--option_c", action="store_true", help="Collect working links using httpx.")
    
    args = parser.parse_args()
    
    if args.option_a:
        option_a(args.domain)
    
    if args.option_b:
        option_b(args.domain)
    
    if args.option_c:
        option_c(args.domain)

if __name__ == "__main__":
    main()
