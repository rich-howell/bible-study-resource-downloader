import os
import re
import time
import requests
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, unquote

URL = "https://bibleproject.com/downloads/"
# Where you want the files to be saved
OUTPUT_DIR = r"G:\My Drive\Bible Study\Bible Project"
# True or False
DRY_RUN = False
# Try to keep this at 5 if possible to avoid hammering the server
SLEEP_SECONDS = 1

def safe_name(text: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "", text).strip()

def filename_from_episode_text(text: str, url: str) -> str:
    
    # Build a filename from the episode text and preserve the file extension.    
    # Normalise the title text
    name = text.strip()
    # Remove special chars
    name = re.sub(r"[^\w\s-]", "", name)
    #Replace spaces with underscores
    name = name.replace(" ", "_")

    # Extract extension from URL
    ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"

    return f"{name}{ext}"

def filename_from_url(url: str) -> str:
    
    # Extract a clean filename from the poster URL.    
    path = urlparse(url).path
    return safe_name(unquote(os.path.basename(path)))

def main():
    print("🚀 Launching browser")
    print(f"🧪 Dry-run: {'ON' if DRY_RUN else 'OFF'}")
    if DRY_RUN is False:
        print(f"🕔 Delay: {SLEEP_SECONDS}s\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        # Let JS hydrate
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        # Accept cookies if present
        if page.locator("button:has-text('Accept')").count():
            page.locator("button:has-text('Accept')").first.click()
            page.wait_for_timeout(1000)

        # Expand all accordion sections
        buttons = page.locator("button[aria-expanded]")
        for i in range(buttons.count()):
            btn = buttons.nth(i)
            if btn.get_attribute("aria-expanded") == "false":
                btn.click()
                page.wait_for_timeout(300)

        sections = page.locator("h2.downloads-accordion-item-title")
        total = 0

        for i in range(sections.count()):
            section_el = sections.nth(i)
            section_name = safe_name(section_el.inner_text())
            print(f"\n📂 {section_name}")

            posters = section_el.locator(
                'xpath=following::a[contains(@class,"downloads-accordion-item-episode-link")'
                ' and .//span[normalize-space(.)="Poster"]]'
            )

            for j in range(posters.count()):
                poster = posters.nth(j)

                # Stop if we crossed into the next section
                if poster.locator(
                    "xpath=preceding::h2[contains(@class,'downloads-accordion-item-title')][1]"
                ).inner_text() != section_el.inner_text():
                    break

                url = poster.get_attribute("href")
                if not url:
                    continue

                episode_text = poster.evaluate("""
                (el) => {
                const episode = el.closest('.downloads-accordion-item-episode');
                const titleEl = episode
                    ? episode.querySelector('.downloads-accordion-item-episode-text')
                    : null;
                return titleEl ? titleEl.textContent.trim() : '';
                }
                """)

                if not episode_text:
                    print("    ⚠️  No episode text found, skipping")
                    continue

                filename = filename_from_episode_text(episode_text, url)
                path = os.path.join(OUTPUT_DIR, section_name, filename)

                print(f"  🖼️ {filename}")
                print(f"    ↳ SOURCE URL: {url}")

                if DRY_RUN:
                    print(f"    ↳ WOULD SAVE AS: {path}")
                else:
                    os.makedirs(os.path.dirname(path), exist_ok=True)

                    if os.path.exists(path):
                        print("    ⏭️  File already exists, skipping")
                        continue

                    # download happens here
                    print("    ⬇️  Downloading poster")

                    response = requests.get(url, stream=True, timeout=60)
                    response.raise_for_status()

                    with open(path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                    print(f"    ✅ FILE SAVED AS: {path}")

                    time.sleep(SLEEP_SECONDS)

                total += 1

        browser.close()

    print(f"\n✅ Done. Posters found: {total}")
    print("🧘 Stanley rests, *correctly this time*.")


if __name__ == "__main__":
    main()
