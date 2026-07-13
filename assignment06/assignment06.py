import os
import csv
import getpass
from playwright.sync_api import sync_playwright

BASE_URL = "https://inventory.teamrabbil.com"
CSV_FILE = "customers.csv"
LOG_FILE = "customer_upload_log.txt"

TEST_EMAIL = os.environ.get("TEST_ACCOUNT_EMAIL") or input("Test account email: ").strip()
TEST_PASSWORD = os.environ.get("TEST_ACCOUNT_PASSWORD") or getpass.getpass("Test account password: ")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # login with test account
    page.goto(f"{BASE_URL}/userLogin", wait_until="networkidle")
    page.locator("#email").fill(TEST_EMAIL)
    page.locator("#password").fill(TEST_PASSWORD)
    with page.expect_navigation(wait_until="networkidle"):
        page.get_by_text("Next", exact=False).click()

    print("Login successful. Current URL:", page.url)

    # open customer page
    page.goto(f"{BASE_URL}/customerPage", wait_until="networkidle")

    with open(CSV_FILE, newline="", encoding="utf-8") as csv_file:
        customers = list(csv.DictReader(csv_file))

    results = []
    success_count = 0
    failure_count = 0

    for row in customers:
        name = row["customerName"].strip()
        email = row["customerEmail"].strip()
        mobile = row["customerMobile"].strip()

        page.locator("button[data-bs-target='#create-modal']").click()
        page.wait_for_timeout(1500)

        page.locator("#customerName").fill(name)
        page.locator("#customerEmail").fill(email)
        page.locator("#customerMobile").fill(mobile)
        page.locator("#save-btn").click()
        page.wait_for_timeout(1500)

        if page.locator("#create-modal.show").count() == 0:
            status = f"SUCCESS: {name} ({email}) added."
            success_count += 1
        else:
            status = f"FAILURE: {name} ({email}) could not be added."
            failure_count += 1
            page.locator("#modal-close").click()
            page.wait_for_selector("#create-modal.show", state="hidden")

        print(status)
        results.append(status)

    total_processed = len(customers)
    results.append(f"Total rows processed: {total_processed} (Success: {success_count}, Failure: {failure_count})")

    with open(LOG_FILE, "w", encoding="utf-8") as log_file:
        log_file.write("\n".join(results))

    print(f"Total rows processed: {total_processed} (Success: {success_count}, Failure: {failure_count})")
    print(f"Log saved to {LOG_FILE}")

    context.close()
    browser.close()
