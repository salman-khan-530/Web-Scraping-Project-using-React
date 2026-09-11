"""
Test scraper for Books to Scrape.

This scraper is used to test the complete scraping workflow
without requiring an external API key.
"""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper


class TestScraper(BaseScraper):
    """
    Scraper for the Books to Scrape practice website.
    """

    source_name = "Test Site"
    base_url = "https://books.toscrape.com/"

    def search_products(self, query, max_products=20):
        """
        Search for products matching the query.

        The scraper goes through multiple pages until:
        - enough products are found, or
        - there are no more pages.

        Args:
            query (str): Product name to search for.
            max_products (int): Maximum number of products to return.

        Returns:
            list: List of standardized product dictionaries.
        """

        products = []

        if not isinstance(query, str) or not query.strip():
            return products

        query = query.strip().lower()

        current_url = self.base_url

        while current_url and len(products) < max_products:

            try:
                response = requests.get(
                    current_url,
                    timeout=15
                )
                response.raise_for_status()

            except requests.RequestException:
                break

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            product_cards = soup.select(".product_pod")

            for card in product_cards:

                if len(products) >= max_products:
                    break

                # -----------------------------
                # Product name
                # -----------------------------

                name_tag = card.select_one("h3 a")

                if not name_tag:
                    continue

                name = name_tag.get("title")

                if not name:
                    name = name_tag.get_text(strip=True)

                # Search by product name
                if query not in name.lower():
                    continue

                # -----------------------------
                # Price
                # -----------------------------

                price_tag = card.select_one(
                    ".price_color"
                )

                price = (
                    price_tag.get_text(strip=True)
                    if price_tag
                    else None
                )

                # -----------------------------
                # Rating
                # -----------------------------

                rating = None

                rating_tag = card.select_one(
                    ".star-rating"
                )

                if rating_tag:

                    rating_classes = rating_tag.get(
                        "class",
                        []
                    )

                    rating_map = {
                        "One": 1,
                        "Two": 2,
                        "Three": 3,
                        "Four": 4,
                        "Five": 5
                    }

                    for rating_name, rating_value in rating_map.items():

                        if rating_name in rating_classes:
                            rating = rating_value
                            break

                # -----------------------------
                # Availability
                # -----------------------------

                availability_tag = card.select_one(
                    ".availability"
                )

                availability = (
                    availability_tag.get_text(
                        " ",
                        strip=True
                    )
                    if availability_tag
                    else None
                )

                # -----------------------------
                # Product URL
                # -----------------------------

                product_link = name_tag.get("href")

                product_url = (
                    urljoin(
                        current_url,
                        product_link
                    )
                    if product_link
                    else None
                )

                # -----------------------------
                # Product image
                # -----------------------------

                image_tag = card.select_one("img")

                image_url = None

                if image_tag:

                    image_src = image_tag.get("src")

                    if image_src:
                        image_url = urljoin(
                            current_url,
                            image_src
                        )

                # -----------------------------
                # Category & description
                # -----------------------------

                category = None
                description = None

                if product_url:

                    try:

                        detail_response = requests.get(
                            product_url,
                            timeout=15
                        )

                        detail_response.raise_for_status()

                        detail_soup = BeautifulSoup(
                            detail_response.text,
                            "html.parser"
                        )

                        # Category
                        breadcrumb = detail_soup.select(
                            ".breadcrumb li a"
                        )

                        if breadcrumb:
                            category = breadcrumb[-1].get_text(
                                strip=True
                            )

                        # Description
                        description_tag = detail_soup.select_one(
                            "#product_description + p"
                        )

                        if description_tag:
                            description = description_tag.get_text(
                                " ",
                                strip=True
                            )

                    except requests.RequestException:
                        pass

                # -----------------------------
                # Create standardized product
                # -----------------------------

                product = self.create_product(
                    name=name,
                    price=price,
                    rating=rating,
                    availability=availability,
                    url=product_url,
                    category=category,
                    description=description,
                    source=self.source_name,
                    image_url=image_url
                )

                products.append(product)

            # -----------------------------
            # Pagination
            # -----------------------------

            next_page = soup.select_one(
                "li.next a"
            )

            if next_page:

                next_url = next_page.get("href")

                current_url = urljoin(
                    current_url,
                    next_url
                )

            else:
                current_url = None

        return products

    def get_product_details(self, product_url):
        """
        Get detailed information about a single product.

        Args:
            product_url (str): URL of the product page.

        Returns:
            dict: Product details.
        """

        if not product_url:
            return {}

        try:

            response = requests.get(
                product_url,
                timeout=15
            )

            response.raise_for_status()

        except requests.RequestException:
            return {}

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # -----------------------------
        # Product name
        # -----------------------------

        name_tag = soup.select_one(
            ".product_main h1"
        )

        name = (
            name_tag.get_text(strip=True)
            if name_tag
            else None
        )

        # -----------------------------
        # Price
        # -----------------------------

        price_tag = soup.select_one(
            ".price_color"
        )

        price = (
            price_tag.get_text(strip=True)
            if price_tag
            else None
        )

        # -----------------------------
        # Rating
        # -----------------------------

        rating = None

        rating_tag = soup.select_one(
            ".star-rating"
        )

        if rating_tag:

            rating_classes = rating_tag.get(
                "class",
                []
            )

            rating_map = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }

            for rating_name, rating_value in rating_map.items():

                if rating_name in rating_classes:
                    rating = rating_value
                    break

        # -----------------------------
        # Availability
        # -----------------------------

        availability_tag = soup.select_one(
            ".availability"
        )

        availability = (
            availability_tag.get_text(
                " ",
                strip=True
            )
            if availability_tag
            else None
        )

        # -----------------------------
        # Category
        # -----------------------------

        category = None

        breadcrumb = soup.select(
            ".breadcrumb li a"
        )

        if breadcrumb:
            category = breadcrumb[-1].get_text(
                strip=True
            )

        # -----------------------------
        # Description
        # -----------------------------

        description = None

        description_tag = soup.select_one(
            "#product_description + p"
        )

        if description_tag:
            description = description_tag.get_text(
                " ",
                strip=True
            )

        # -----------------------------
        # Image
        # -----------------------------

        image_url = None

        image_tag = soup.select_one(
            ".item.active img"
        )

        if not image_tag:
            image_tag = soup.select_one(
                ".product_page img"
            )

        if image_tag:

            image_src = image_tag.get("src")

            if image_src:
                image_url = urljoin(
                    product_url,
                    image_src
                )

        # -----------------------------
        # Return standardized product
        # -----------------------------

        return self.create_product(
            name=name,
            price=price,
            rating=rating,
            availability=availability,
            url=product_url,
            category=category,
            description=description,
            source=self.source_name,
            image_url=image_url
        )