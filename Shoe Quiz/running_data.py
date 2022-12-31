from playwright.async_api import Playwright, async_playwright
import asyncio
import pandas as pd 

names = set()
async def extract_data(page):
    all_items = await page.query_selector_all("div.prodPreview")
    productlist = []

    for item in all_items: 
        product = {}
        name_el = await item.query_selector('div.ellipsis.prodName')
        product["name"] = await name_el.inner_text()
        product["name"], *others = product["name"].splitlines()
        product["link"]= await name_el.eval_on_selector_all('a[href]', 'elements => elements.map(element => element.href)')
        if await item.query_selector("div.prodPriceSale"):
            sale_el = await item.query_selector("div.prodPriceSale")
            product["price"] = await sale_el.inner_text()
        else:
            price_el = await item.query_selector("div.prodPrice")
            product["price"] = await price_el.inner_text()

        if product["name"] not in names:
            productlist.append(product)
            names.add(product["name"])
    return productlist

async def save_to_csv(data):
    run_df = pd.DataFrame(data)
    run_df.to_csv('C:/Users/natal/OneDrive/Documents/natalie-code/'+'neutral_description.csv')

async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()

    page = await context.new_page()
    await page.goto("https://www.runningfree.com/products/Shoes-27/Womens-727/Neutral-Cushion-35/")
    data = []
    data.extend(await extract_data(page))

    for i in range(1):
        next_el = await page.query_selector("div.pageLinks")
        link = await next_el.eval_on_selector_all('a[href]','elements => elements.map(element => element.href)')
        page = await context.new_page()
        await page.goto(link[0])
        data.extend(await extract_data(page))
        await page.wait_for_selector("div.prodPreview")
    for i in range(3):
         next_el = await page.query_selector("div.pageLinks")
         link = await next_el.eval_on_selector_all('a[href]','elements => elements.map(element => element.href)')  
         page = await context.new_page()
         await page.goto(link[1])
         data.extend(await extract_data(page)) 
         await page.wait_for_selector("div.prodPreview")
    
    await context.close()
    await browser.close()

    await save_to_csv(data)


async def main() ->None:
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())

