import sys, asyncio
from playwright.async_api import async_playwright
async def main(src,dst,shots=None):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(); await pg.goto('file://'+src); await pg.wait_for_timeout(500)
        await pg.pdf(path=dst,width='794px',height='1123px',print_background=True,prefer_css_page_size=True)
        await b.close()
asyncio.run(main(sys.argv[1],sys.argv[2]))
