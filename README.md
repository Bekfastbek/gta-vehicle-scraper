# 🚗 GTA Vehicle Scraper

This project scrapes vehicle data from [GTA Base](https://www.gtabase.com) and extracts real-life car models based on GTA vehicles.  

It consists of two scrapers:  
1. **Vehicle Link Scraper** - Collects links to GTA V/Online vehicles.  
2. **Vehicle Model Scraper** - Extracts real-life models for each vehicle.  

## 📦 Features  
✅ Scrapes vehicle links from multiple pages  
✅ Extracts real-life car models  
✅ Saves results in `vehicles.json` and `vehicle_list.json`  
✅ Uses **Playwright** for fast, headless browsing  

## 🛠 Installation  

**Clone the repository**
```
git clone https://github.com/Bekfastbek/gta-vehicle-scraper.git
cd gta-vehicle-scraper
```
   
**Create a virtual environment (optional but recommended)**
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**Install dependencies**
```
pip install playwright asyncio
playwright install
```
# 🚀 Usage
Run the main script to scrape vehicle links first, then extract real-life models:
```
python main.py
```
Alternatively, you can run each scraper separately:

**Scrape vehicle links**
```
python -m vehicle_link_scraper
```
**Scrape real-life models**
```
python -m vehicle_scraper
```
**📂 Output Files**\
vehicles.json → Contains all scraped vehicle links.\
vehicle_list.json → Contains GTA vehicles and their real-life counterparts.