import pytest
from playwright.sync_api import Page, expect


def test_kau_homepage(page: Page):
    page.goto("https://www.kau.se/")

    # Close cookie/popup banner if present
    close_btn = page.locator("#WSA_CLOSE")
    if close_btn.is_visible(timeout=3000):
        close_btn.click()

    # Accept only necessary cookies if the dialog appears
    cookie_btn = page.get_by_role("button", name="Jag godkänner enbart att ni använder nödvändiga cookies")
    if cookie_btn.is_visible(timeout=3000):
        cookie_btn.click()

    # ✅ Example 1: Check title
    expect(page).to_have_title(re.compile("Karlstads universitet"))

    # ✅ Example 2: Search for "IT"
    search_toggle = page.locator("button.js-search-modal-toggle")
    search_toggle.wait_for(state="visible")
    search_toggle.click()

    search_input = page.locator("input[type='search']")
    search_input.wait_for(state="visible")
    search_input.fill("IT")
    search_input.press("Enter")

    # Wait for search results text to appear
    result_text = page.locator("p:has-text('Din sökning på')")
    result_text.wait_for(state="visible")
    expect(result_text).to_contain_text("IT")
