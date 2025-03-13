import asyncio
from link_fetch import GTAVehicleLinkScraper
from scrape_names import GTAVehicleScraper

async def main():
    print("\n🔍 Starting vehicle link scraper...")
    link_scraper = GTAVehicleLinkScraper(total_pages=13, wait_time=5, max_retries=3)
    await link_scraper.scrape_vehicle_links()

    print("\n🚗 Starting vehicle model scraper...")
    vehicle_scraper = GTAVehicleScraper(chunk_size=10, wait_time=5) # Change chunk_size value if you have more than 16 gb of memory and more than 16 threads (for example if you have 32 threads, set it to 26)
    await vehicle_scraper.scrape_irl_models()

if __name__ == "__main__":
    asyncio.run(main())
