from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://inventory.teamrabbil.com/userRegistration", wait_until="networkidle")
    
    # form details fill
    page.locator("#email").fill("kuddus@example.com")
    page.locator("#firstName").fill("Kuddus")
    page.locator("#lastName").fill("mia")
    page.locator("#mobile").fill("01712121212")
    page.locator("#password").fill("mia@123")
    
    with page.expect_navigation(wait_until="networkidle"):
        page.get_by_text("complete", exact=False).click()
    
    print("Current url:", page.url)
    context.close()
    
    # new browser context
    new_context = browser.new_context()
    new_page = new_context.new_page()
    
    new_page.goto("https://inventory.teamrabbil.com/userLogin", wait_until="networkidle")
    new_page.locator("#email").fill("kuddus@example.com")
    new_page.locator("#password").fill("mia@123")
    
    with new_page.expect_navigation(wait_until="networkidle"):
        new_page.get_by_text("Next",exact=False).click()
    
    new_context.storage_state(path="auth.json")
    print("Login successfully")

    new_page.reload(wait_until="networkidle")
    print("page reloaded.")
    print("url after reload:", new_page.url)
    
    new_page.goto("https://inventory.teamrabbil.com/userProfile", wait_until="networkidle")
    new_page.locator("#firstName").fill("Zahir")

    new_page.get_by_text("Update", exact=False).click()
    print("Profile Updated.")
    
    # saved updated session state
    new_context.storage_state(path="auth.json")
    print("Updated session state saved again.")
    
    new_context.close()
    browser.close()
    print("All steps completed successfully.")