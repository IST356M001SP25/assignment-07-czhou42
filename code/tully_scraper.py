import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.tullysgoodtimes.com/menus/")

    page.goto("https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/")
    page.wait_for_selector(".menu-section")

    all_items = []

    # Select all menu categories
    titles = page.locator(".menu-section h2")
    for i in range(titles.count()):
        title = titles.nth(i).inner_text().strip()

        # Navigate to menu items container div.row
        menu_section = titles.nth(i).locator("..").locator("..").locator(".row")
        item_boxes = menu_section.locator(".menu-item")

        for j in range(item_boxes.count()):
            item_text = item_boxes.nth(j).inner_text().strip()
            try:
                item = extract_menu_item(title, item_text)
                all_items.append(item.to_dict())
            except Exception as e:
                print(f"Failed to parse item in '{title}': {e}")

    # Save to CSV
    df = pd.DataFrame(all_items)
    df.to_csv("cache/tullys_menu.csv", index=False)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)
