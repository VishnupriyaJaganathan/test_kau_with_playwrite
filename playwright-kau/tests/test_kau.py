import re
from playwright.sync_api import Page, expect


def test_kau_homepage(page: Page):
    page.goto("https://www.kau.se/")

    # Close WSA popup if present
    close_btn = page.locator("#WSA_CLOSE")
    if close_btn.is_visible(timeout=3000):
        close_btn.click()

    # Dismiss Klaro cookie overlay — wait for it then click
    cookie_btn = page.locator("button.cm-btn-success")
    if cookie_btn.is_visible(timeout=5000):
        cookie_btn.click()

    # Wait for the overlay to disappear completely
    page.locator("#klaro").wait_for(state="hidden", timeout=5000)

    # ✅ Example 1: Check title
    expect(page).to_have_title(re.compile("Karlstads universitet"))

    # ✅ Example 2: Search for "IT"
    search_toggle = page.get_by_label("Search").first
    search_toggle.wait_for(state="visible")
    search_toggle.click()

    search_input = page.locator("input[type='search']")
    search_input.wait_for(state="visible")
    search_input.fill("IT")
    search_input.press("Enter")

    # Wait for search results
    result_text = page.locator("p:has-text('Din sökning på')")
    result_text.wait_for(state="visible")
    expect(result_text).to_contain_text("IT")
