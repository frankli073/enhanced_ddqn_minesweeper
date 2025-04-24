import asyncio
from playwright.async_api import async_playwright

async def fetch_unabated_nba_odds():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page    = await browser.new_page()
        await page.goto("https://unabated.com/nba/odds")
        # wait for the table rows
        await page.wait_for_selector("table tbody tr", timeout=30000)

        games = []
        rows = await page.query_selector_all("table tbody tr")
        for r in rows:
            away_el  = await r.query_selector("td:nth-child(1)")
            home_el  = await r.query_selector("td:nth-child(2)")
            away_ml_el = await r.query_selector("td.moneyline:nth-child(1)")
            home_ml_el = await r.query_selector("td.moneyline:nth-child(2)")

            away    = (await away_el.inner_text()).strip()
            home    = (await home_el.inner_text()).strip()
            away_ml = (await away_ml_el.inner_text()).strip()
            home_ml = (await home_ml_el.inner_text()).strip()

            games.append({
                "away": away,
                "home": home,
                "away_ml": away_ml,
                "home_ml": home_ml,
            })

        await browser.close()
        return games

# Run outside the notebook’s loop
odds = asyncio.get_event_loop().run_until_complete(fetch_unabated_nba_odds())
for g in odds:
    print(f"{g['away']} @ {g['home']}: Away {g['away_ml']}  Home {g['home_ml']}")
