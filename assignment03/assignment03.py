from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://www.scrapethissite.com/", wait_until="networkidle")
    print(page.url)
    page.get_by_text("Login").click()

    print("After Login Click:", page.url)
    
    page.go_back()
    page.locator("#nav-login").click()
    print("After ID Selector Click:", page.url)

    page.go_back()
    buttons = page.locator(".btn")
    print("Total buttons:", buttons.count())
    
    buttons.nth(0).click()
    print("After First Button Click:", page.url)

    page.go_back()
    first_button_text = buttons.nth(0).inner_text()
    print("First Button Text:", first_button_text)

    header_html = page.locator("head").inner_html()
    print("collected")
    with open("header.html", "w", encoding="utf-8") as file:
        file.write(header_html)


    h1 = page.locator("h1").nth(0)

    inner_text = h1.inner_text()
    inner_html = h1.inner_html()
    text_content = h1.text_content()

    print(inner_text)
    print(inner_html)
    print(text_content)

    browser.close()