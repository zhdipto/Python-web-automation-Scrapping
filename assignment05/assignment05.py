import os
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    upload_logs = []
    page.goto("https://inventory.teamrabbil.com/public/UploadPage", wait_until="networkidle")

    image_files = os.listdir("images")
    
    for fileName in image_files:
        filePath = os.path.join("images", fileName)
        page.set_input_files("input[type='file']", filePath) 
        page.click("button[type='submit']")

        try:
            page.wait_for_selector(".alert-success", timeout=5000)
            print(f"{fileName} uploaded successfully.")
            upload_logs.append(f"{fileName} uploaded successfully.")
        except Exception:
            print(f"Failed to upload {fileName}.")
            upload_logs.append(f"Failed to upload {fileName}.")

        time.sleep(2)
        page.reload(wait_until="networkidle")

    with open("upload_log.txt", "w") as log_file:
        log_file.write("\n".join(upload_logs))
    print("Upload logs saved to upload_log.txt")

    page.goto("https://inventory.teamrabbil.com/DownloadPage", wait_until="networkidle")

    download_buttons = page.locator("a.btn.btn-success.btn-sm")
    total_files_found = download_buttons.count()
    saved_files_count = 0

    for i in range(total_files_found):
        with page.expect_download() as download_info:
            download_buttons.nth(i).click()
            
        download = download_info.value
        file_name = download.suggested_filename
        save_path = os.path.join("downloads", file_name)
        download.save_as(save_path)
        print(f"{file_name} downloaded and saved successfully.")
        saved_files_count += 1
        time.sleep(2) 
            
    print(f"Total download links found: {total_files_found}")
    print(f"Total files successfully saved: {saved_files_count}")

    browser.close()