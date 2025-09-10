from playwright.sync_api import sync_playwright

def fetch_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print(f"Navigating to {url} ...")
        page.goto(url, wait_until="networkidle")
        
        html_content = page.content()
        
        browser.close()
        return html_content

if __name__ == "__main__":
    url = "https://uae.voxcinemas.com/booking/0036-84656"
    html = fetch_html(url)
    
    # Save to file
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("HTML content saved to output.html")
