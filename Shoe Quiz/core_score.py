from playwright.async_api import Playwright, async_playwright
import asyncio
import pandas as pd 

async def extract_data(page):
    all_items = await page.query_selector_all("li.row.product_list")
    productlist = []

    for item in all_items: 
        product = {}
        name_el = await item.query_selector('div.product-name.hidden-md.hidden-lg.col-md-12.col-lg-12')
        name_el = await name_el.query_selector('span')
        product["name"] = await name_el.inner_text()
        score_el = await item.query_selector('div.product-score.hidden-md.hidden-lg.col-md-12.col-lg-12')
        product["core score"] = await score_el.inner_text()
        list = product["core score"].split()
        product["core score"] = list[0]
        productlist.append(product)
    return productlist

async def save_to_csv(data):
    run_df = pd.DataFrame(data)
    run_df.to_csv('C:/Users/natal/OneDrive/Documents/natalie-code/Shoe Quiz/'+'core_score.csv')

async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()

    page = await context.new_page()
    await page.goto("https://runrepeat.com/catalog/womens-running-shoes?order_by=newest")
    data = []
    data.extend(await extract_data(page))

    for i in range(20):
        await page.locator("text=›").click()
        data.extend(await extract_data(page))
        await page.wait_for_selector("li.row.product_list")
    await context.close()
    await browser.close()
    
    await save_to_csv(data)

async def main() ->None:
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())