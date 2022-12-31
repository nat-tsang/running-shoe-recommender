from playwright.async_api import Playwright, async_playwright
import asyncio
import pandas as pd

folderpath = 'C:/Users/natal/OneDrive/Documents/natalie-code/csv/'+'shoe_neutral.csv'
async def save_to_csv(data2):
    run_df = pd.read_csv(folderpath)
    type_df = pd.DataFrame(data2)
    frames = [run_df, type_df]
    pd.concat(frames, keys=['Info', 'Specs'], axis=1).to_csv(folderpath,index=False)
    return run_df

async def page_extract_data(page):
    specs_list = []
    specs = {}
    all_specs = await page.query_selector('div.prodSpecs')
    cat_el = await all_specs.query_selector('div:nth-child(2)')#productForm > div.prodSpecs > div:nth-child(2) > h4
    specs_el = await cat_el.query_selector('h4')
    specs["category"] = await specs_el.inner_text()
    drop_el = await all_specs.query_selector('div:nth-child(3)')
    if drop_el is not None:
        specs2_el = await drop_el.query_selector('h4')
        specs["drop"] = await specs2_el.inner_text()#productForm > div.prodSpecs > div:nth-child(4)
    else:
        specs["drop"] = 'None'
    weight_el = await all_specs.query_selector('div:nth-child(4)')
    if weight_el is not None:
        specs3_el = await weight_el.query_selector('h4')
        specs["weight"] = await specs3_el.inner_text()
    else:
        specs["weight"] = 'None'
    print(specs["weight"])
    specs_list.append(specs)
    item = await page.query_selector('div.prodDescription')
    if item is not None:
            descrp_el = await item.query_selector('p')
            specs["description"] = descrp_el.inner_text()
    return specs_list

async def get_links(playwright: Playwright) -> None:
    run_df = pd.read_csv(folderpath)
    links = run_df["link"] 
    data2 = []
    for i in range(0, len(links)):
        go_to = links[i]
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(go_to[2:-3])
        data2.extend(await page_extract_data(page))
        await context.close()
        await browser.close()
    return data2

async def run(playwright: Playwright) ->None:
    data2 = await get_links(playwright)
    await save_to_csv(data2)

async def main() ->None:
    async with async_playwright() as playwright: 
        await run(playwright)

asyncio.run(main())