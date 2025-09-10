from playwright.sync_api import sync_playwright, TimeoutError
import time

def fetch_html(url, retries=3):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
            locale="en-US",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Connection": "keep-alive"
            }
        )
        
        page = context.new_page()
        
        attempt = 0
        while attempt < retries:
            try:
                print(f"Attempt {attempt+1}: Navigating to homepage to set cookies...")
                page.goto("https://uae.voxcinemas.com/", wait_until="networkidle", timeout=15000)
                time.sleep(3)
                
                print(f"Attempt {attempt+1}: Navigating to target URL {url} ...")
                page.goto(url, wait_until="networkidle", timeout=15000)
                time.sleep(3)
                
                html_content = page.content()
                
                # Save to file
                with open("output.html", "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                print("HTML content saved to output.html")
                
                browser.close()
                return html_content
            
            except TimeoutError as e:
                print(f"TimeoutError: {e}")
            except Exception as e:
                print(f"Error: {e}")
            
            attempt += 1
            print("Retrying in 5 seconds...")
            time.sleep(5)
        
        browser.close()
        raise Exception("Failed to load page after several attempts")

if __name__ == "__main__":
    url = "https://uae.voxcinemas.com/booking/0036-84656"
    try:
        fetch_html(url)
    except Exception as e:
        print(f"Failed: {e}")
