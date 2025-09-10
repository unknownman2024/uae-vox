import requests
import time

def fetch_seats_page_after_idle(movie_url, timeout=30, interval=5):
    print(f"🌍 Visiting first showtime URL: {movie_url}")

    session = requests.Session()

    # Step 1: open showtime URL -> it will redirect
    response = session.get(movie_url, allow_redirects=True, timeout=30)
    final_url = response.url
    print(f"🔀 Redirected to: {final_url}")

    # Step 2: construct seats fetch URL
    if "/guest" in final_url:
        seats_url = final_url.replace("/guest", "/seats")
    else:
        raise ValueError("⚠️ Unexpected redirect URL format")

    print(f"🎟️ Seats page: {seats_url}")

    # Step 3: poll the seats page until expected content is present or timeout
    start_time = time.time()
    while time.time() - start_time < timeout:
        print(f"⏳ Checking seats page at {time.strftime('%X')} ...")
        seats_response = session.get(seats_url, timeout=30)

        if seats_response.status_code == 200:
            # Example check: does the page include a specific marker?
            if "seat-map" in seats_response.text.lower():
                print("✅ Seats content detected!")
                with open("seats.html", "w", encoding="utf-8") as f:
                    f.write(seats_response.text)
                print("✅ Seats HTML saved to seats.html")
                return
            else:
                print("ℹ️ Seats content not ready yet.")
        else:
            print(f"❌ Failed to fetch seats page, status {seats_response.status_code}")

        time.sleep(interval)

    print("⚠️ Timeout reached. Seats content not available.")
    # Optionally save the last response anyway
    with open("seats.html", "w", encoding="utf-8") as f:
        f.write(seats_response.text)
    print("✅ Last fetched HTML saved to seats.html")

if __name__ == "__main__":
    first_show_url = "https://uae.voxcinemas.com/booking/0036-84656"
    fetch_seats_page_after_idle(first_show_url)
