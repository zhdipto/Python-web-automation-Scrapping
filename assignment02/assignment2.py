from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://google.com")
    print("Title:", page.title())
    print("Current URL:", page.url)

    page.goto("https://mern.rabbil.com/")
    print("Current URL:", page.url)

    page.goto("https://www.rabbil.com", wait_until="networkidle")
    print("Current URL:", page.url)

    page.reload()
    print("After Reload:", page.url)
    page.go_back()
    print("After Back:", page.url)
    page.go_forward()
    print("After Forward:", page.url)

    page.screenshot(path="fullPageSS.png",full_page=True)
    page.pdf(path="page.pdf",format="A4", print_background=True)

    #mobile view
    page.set_viewport_size({"width": 375, "height": 667})
    page.screenshot(path="mobile_view.png", full_page=True)

    #desktop view
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.screenshot(path="desktop_view.png", full_page=True)

    html = page.content()
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)


    seo_data = {
        "title": page.title(),
        "description": page.locator(
            'meta[name="description"]'
        ).get_attribute("content"),
        "keywords": page.locator(
            'meta[name="keywords"]'
        ).get_attribute("content"),
        "og:title": page.locator(
            'meta[property="og:title"]'
        ).get_attribute("content"),
        "og:description": page.locator(
            'meta[property="og:description"]'
        ).get_attribute("content"),
        "og:image": page.locator(
            'meta[property="og:image"]'
        ).get_attribute("content"),
        "og:url": page.locator(
            'meta[property="og:url"]'
        ).get_attribute("content"),
    }

    with open("seo_data.json", "w", encoding="utf-8") as f:
        json.dump(seo_data, f, indent=4, ensure_ascii=False)

    print("done")
    browser.close()