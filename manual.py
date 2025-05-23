import os
from supabase import create_client, Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from colorama import Fore, Style, init

# === INIT COLOR ===
init(autoreset=True)

# === SUPABASE SETUP ===
# SUPABASE_URL = "https://your-project.supabase.co"
# SUPABASE_KEY = "your-supabase-api-key"
# TABLE_NAME = "css_data"

# === CONTROLLER SETTINGS ===
CONTROLLERS = ['ds4', 'ds5', 'ps', 'xbox-old', 'xbox', 'custom']
BASE_URL = "https://gamepadvision.com/customcontroller?controller={}&p=0&theme=light&slug={}"
WAIT_BEFORE_NEXT = 0.5

# === INIT SUPABASE ===
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
response = supabase.table(TABLE_NAME).select("slug").execute()
slugs = [row['slug'] for row in response.data]
print(f"{Fore.GREEN}✅ Retrieved {len(slugs)} slugs from Supabase")

# === INIT CHROME (VISIBLE) ===
print(f"{Fore.GREEN}🟢 Launching visible Chrome browser...")
options = Options()
options.add_argument("--window-size=1280,720")
driver = webdriver.Chrome(options=options)

# === MAIN LOOP ===
try:
    for slug in slugs:
        print(f"\n{Fore.CYAN}🔵 Slug: {slug}{Style.RESET_ALL}")
        for controller in CONTROLLERS:
            url = BASE_URL.format(controller, slug)
            print(f"{Fore.YELLOW}➡️  Controller: {controller}{Style.DIM} | URL: {url}{Style.RESET_ALL}")
            driver.get(url)
            input(f"{Fore.MAGENTA}⏎ Press [Enter] to show the next controller...")

        print(f"{Fore.GREEN}✅ Done with slug: {slug}")

    print(f"{Fore.LIGHTGREEN_EX}🎉 All slugs processed.")

except KeyboardInterrupt:
    print(f"\n{Fore.RED}⛔ Interrupted by user.")

finally:
    driver.quit()
    print(f"{Fore.BLUE}🧹 Chrome closed.")
