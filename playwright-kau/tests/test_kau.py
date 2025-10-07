from playwright.sync_api import sync_playwright


def test_kau_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # False = see the browser
        page = browser.new_page()

        # Go to Karlstad University website
        page.goto("https://www.kau.se/")
        page.click("//*[@id='WSA_CLOSE']")
        page.click("//button[contains(text(),'Jag godkänner enbart att ni använder nödvändiga cookies')]")
        title_1=page.title()
        print(title_1)
        # ✅ Example 1: check title
        assert "xxx xx" in page.title()

        # ✅ Example 2: search for "IT"
        page.click("//button[contains(@class, 'js-search-modal-toggle')]")  # open search box
        page.fill("//input[@type='search']", "IT")
        page.press("//input[@type='search']", "Enter")

        # Wait for results
        page.wait_for_selector("//p[contains(text(), 'Din sökning på')]")
        assert "IT" in page.inner_text("//p[contains(text(), 'Din sökning på')]")

        browser.close()
