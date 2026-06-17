from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
   
    print("browser opened")
    browser.close()
    print("Browser closed")