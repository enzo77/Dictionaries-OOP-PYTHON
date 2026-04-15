"""
Project: Simple web scraper using requests and BeautifulSoup.

This class downloads HTML from a web page and provides simple methods
to extract links and images. All requests and parsing details are
encapsulated inside the class.

https://requests.readthedocs.io/en/latest/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path


class WebScraper:

    def __init__(self, url):
        """Download and parse the HTML of a web page."""
        self.url = url
        html = requests.get(url, timeout=10).text
        self.soup = BeautifulSoup(html, "html.parser")

    def get_all_links(self):
        """Return a list with all link URLs."""
        links = []

        for tag in self.soup.find_all("a"):
            href = tag.get("href")
            if href is not None:
                links.append(href)

        return links

    def get_all_images(self):
        """Return a list with all image files."""
        image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg")
        images = []

        for tag in self.soup.find_all("img"):
            src = tag.get("src")
            if src is not None and src.lower().endswith(image_extensions):
                images.append(src)

        return images

    def download_images(self, folder="images"):
        """Download all images to a local folder."""

        # Create the folder if it does not exist (do nothing if it already exists)
        Path(folder).mkdir(exist_ok=True)

        # Iterate over all image sources found in the page
        for src in self.get_all_images():

            # Build the full URL of the image
            # If the src is already an absolute URL, use it directly
            if src.startswith("http"):
                url = src
            else:
                # Otherwise, combine the base URL with the relative path
                # rstrip("/") removes a trailing slash from the base URL
                # lstrip("/") removes a leading slash from the src
                # Why? We must solve situations like:
                # 1) "https://example.com/" + "/images/photo.jpg"
                #    "https://example.com//images/photo.jpg"
                # 2) "https://example.com" + "images/photo.jpg"
                #    "https://example.comimages/photo.jpg"
                url = self.url.rstrip("/") + "/" + src.lstrip("/")

            try:
                # Download the image content from the URL
                response = requests.get(url, timeout=10)

                # Extract the file name from the URL (everything after the last '/')
                filename = url.split("/")[-1]

                # Build the full path where the file will be saved
                filepath = Path(folder) / filename

                # Write the downloaded content (bytes) to the file
                filepath.write_bytes(response.content)

                # Inform the user that the download was successful
                print(f"Downloaded: {filename}")

            except Exception:
                # If something goes wrong (network error, invalid URL, etc.)
                print(f"Failed: {url}")


if __name__ == "__main__":

    url = "https://www.cs.upc.edu/~jalonso/MCU/B1/test"

    scraper = WebScraper(url)

    print("=== LINKS ===")
    print(scraper.get_all_links())
    print()

    print("=== IMAGES ===")
    print(scraper.get_all_images())
    print()

    print("=== DOWNLOADING IMAGES ===")
    scraper.download_images()