import json
import asyncio
from playwright.async_api import async_playwright


class GTAVehicleLinkScraper:
    BASE_URL = "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page="

    def __init__(self, total_pages = 13, wait_time = 5, max_retries = 3):
        self.total_pages = total_pages
        self.wait_time = wait_time
        self.max_retries = max_retries
        self.all_vehicles = set()

    async def fetch_page_links(self, page, page_num):
        url = f"{self.BASE_URL}{page_num}"
        retries = 0

        while retries < self.max_retries:
            try:
                print(f"🔄 Page {page_num}: Loading {url} (Attempt {retries + 1})")
                await page.goto(url, wait_until = "domcontentloaded")

                print(f"⏳ Waiting {self.wait_time} seconds for full render...")
                await asyncio.sleep(self.wait_time)

                all_links = {await link.get_attribute("href") for link in await page.locator("a").all()}

                vehicle_links = {
                    link for link in all_links if link and (
                            ("/vehicles/grand-theft-auto-v/" in link or "/grand-theft-auto-v/vehicles/" in link)
                            and not link.endswith("/vehicles/")
                            and "/comparison/" not in link
                            and "#" not in link
                            and "?" not in link
                    )
                }

                new_vehicles = vehicle_links - self.all_vehicles
                self.all_vehicles.update(new_vehicles)

                print(f"✅ Page {page_num} - Found {len(new_vehicles)} new vehicles (Total: {len(self.all_vehicles)})")
                return

            except Exception as e:
                print(f"❌ Page {page_num} - Error: {e} (Retry {retries + 1})")
                retries += 1
                await asyncio.sleep(2)

        print(f"⚠️ Page {page_num} - Failed after {self.max_retries} attempts.")

    async def scrape_vehicle_links(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless = True)
            tasks = []

            context = await browser.new_context()
            pages = [await context.new_page() for _ in range(self.total_pages)]

            for page_num, page in enumerate(pages, start = 1):
                tasks.append(self.fetch_page_links(page, page_num))

            await asyncio.gather(*tasks)
            await browser.close()

        with open("vehicles.json", "w", encoding = "utf-8") as f:
            json.dump(sorted(self.all_vehicles), f, indent = 4)

        print("\n🚀 Scraping complete! Data saved to 'vehicles.json'")