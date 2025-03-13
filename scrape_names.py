import json
import asyncio
from playwright.async_api import async_playwright


class GTAVehicleScraper:
    def __init__(self, vehicle_file = "vehicles.json", output_file = "vehicle_list.json", chunk_size = 10,
                 wait_time = 5):
        self.vehicle_file = vehicle_file
        self.output_file = output_file
        self.chunk_size = chunk_size
        self.wait_time = wait_time

        with open(self.vehicle_file, "r", encoding = "utf-8") as f:
            self.vehicle_links = json.load(f)

    async def extract_irl_model(self, page, url):
        full_url = f"https://www.gtabase.com{url}" if not url.startswith("https") else url
        print(f"Navigating to: {full_url}")  # Debugging
        await page.goto(full_url, wait_until = "domcontentloaded")
        await asyncio.sleep(self.wait_time)

        page_text = await page.inner_text("body")
        start_phrase = "is based on a real life"
        start_index = page_text.find(start_phrase)
        if start_index != -1:
            start_index += len(start_phrase) + 1
            end_index = page_text.find(".", start_index)
            if end_index != -1:
                irl_model = page_text[start_index:end_index].strip()
                return irl_model
        return "Unknown"

    async def process_chunk(self, browser, chunk):
        context = await browser.new_context()
        pages = [await context.new_page() for _ in range(len(chunk))]
        results = []

        tasks = [self.extract_irl_model(pages[i], chunk[i]) for i in range(len(chunk))]
        irl_models = await asyncio.gather(*tasks)

        for i, url in enumerate(chunk):
            gta_vehicle = url.split("/")[-1].replace("-", " ").title()
            results.append({"Gta_Vehicle": gta_vehicle, "IRL_Version": irl_models[i]})

        await context.close()
        return results

    async def scrape_irl_models(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless = True)
            all_results = []

            for i in range(0, len(self.vehicle_links), self.chunk_size):
                chunk = self.vehicle_links[i:i + self.chunk_size]
                print(f"🔄 Processing {len(chunk)} vehicles...")
                results = await self.process_chunk(browser, chunk)
                all_results.extend(results)

            await browser.close()

        with open(self.output_file, "w", encoding = "utf-8") as f:
            json.dump(all_results, f, indent = 4)
        print(f"🚀 Scraping complete! Data saved to '{self.output_file}'")
