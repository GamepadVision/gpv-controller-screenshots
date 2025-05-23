import os
from supabase import create_client, Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from PIL import Image
from apng import APNG  # pip install apng

# === ANSI COLOR CODES ===
class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"

# === SUPABASE SETUP ===
# SUPABASE_URL = "https://your-project.supabase.co"
# SUPABASE_KEY = "your-supabase-api-key"
# TABLE_NAME = "css_data"

SUPABASE_URL = "https://ydnacbpxwspxlzcffnfb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlkbmFjYnB4d3NweGx6Y2ZmbmZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM0NTMxMzksImV4cCI6MjAxOTAyOTEzOX0.xvv06zgvo6QCwO4CAElf5RMZbm52LlOxOifEnM_QNl0"
TABLE_NAME = "css_data"

# === SCREENSHOT SETTINGS ===
CONTROLLERS = ['ds4', 'ds5', 'ps', 'xbox-old', 'xbox']
BASE_URL = "https://gamepadvision.com/customcontroller?controller={}&p=0&theme=light&slug={}"
OUTPUT_DIR = "screenshots"
APNG_DIR = "apngs"
WAIT_TIME = 3

# === INIT SUPABASE ===
print(f"{Colors.CYAN}[INFO]{Colors.RESET} Connecting to Supabase...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
response = supabase.table(TABLE_NAME).select("slug").execute()
slugs = [row['slug'] for row in response.data]
print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Retrieved {len(slugs)} slugs from database")

# === INIT CHROME DRIVER ===
print(f"{Colors.CYAN}[INFO]{Colors.RESET} Launching headless Chrome...")
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,720")
driver = webdriver.Chrome(options=options)

# === SETUP DIRECTORIES ===
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(APNG_DIR, exist_ok=True)
taken_screenshots = set(os.listdir(OUTPUT_DIR))
print(f"{Colors.CYAN}[INFO]{Colors.RESET} Found {len(taken_screenshots)} existing screenshots in '{OUTPUT_DIR}'")

# === MAIN LOOP: Take screenshots ===
for slug in slugs:
    for controller in CONTROLLERS:
        filename = f"{controller}_{slug}.png"
        if filename in taken_screenshots:
            print(f"{Colors.YELLOW}[SKIP]{Colors.RESET} {filename} already exists")
            continue
        url = BASE_URL.format(controller, slug)
        print(f"{Colors.BLUE}[LOAD]{Colors.RESET} {url}")
        driver.get(url)
        sleep(WAIT_TIME)
        try:
            screenshot_path = os.path.join(OUTPUT_DIR, filename)
            driver.save_screenshot(screenshot_path)
            print(f"{Colors.GREEN}[OK]{Colors.RESET} Saved {screenshot_path}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not save {filename}: {e}")

driver.quit()
print(f"{Colors.MAGENTA}✅ Done taking screenshots.{Colors.RESET}")

# === CREATE APNGS per slug ===
print(f"{Colors.CYAN}[INFO]{Colors.RESET} Creating APNGs...")

for slug in slugs:
    frames = []
    for controller in CONTROLLERS:
        filename = f"{controller}_{slug}.png"
        path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(path):
            print(f"{Colors.YELLOW}[WARN]{Colors.RESET} Missing {filename}, skipping frame.")
            continue
        frames.append(path)

    if not frames:
        print(f"{Colors.YELLOW}[SKIP]{Colors.RESET} No frames found for slug '{slug}', skipping APNG.")
        continue

    apng_path = os.path.join(APNG_DIR, f"{slug}.png")
    apng = APNG()

    for frame_path in frames:
        # 1000ms delay = 1 second per frame
        apng.append_file(frame_path, delay=1000)

    try:
        apng.save(apng_path)
        print(f"{Colors.GREEN}[OK]{Colors.RESET} Created APNG: {apng_path}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to create APNG for slug '{slug}': {e}")

print(f"{Colors.MAGENTA}✅ All done!{Colors.RESET}")
