"""
Abstract Base Scraper defining the standard interface for all web scrapers.
"""

from abc import ABC, abstractmethod


class ApiNotConfiguredError(Exception):
    """Raised when a scraper requires authorized API credentials that have not been configured."""

    def __init__(self, service_name, env_var):
        self.service_name = service_name
        self.env_var = env_var

        super().__init__(
            f"{service_name} API is not configured. "
            f"Please configure the required authorized API credentials "
            f"via {env_var} in your environment (.env)."
        )


class ApiError(Exception):
    """Raised when an external API returns an error response (such as 401, 403, 429)."""

    pass


class BaseScraper(ABC):
    """
    Common interface for all website and API scrapers.
    """

    source_name = "Base Scraper"

    @abstractmethod
    def search_products(self, query, max_products=20):
        """
        Search for products.

        Args:
            query (str): Search query.
            max_products (int): Maximum number of products to return.

        Returns:
            list: List of standardized product dictionaries.
        """
        pass

    @abstractmethod
    def get_product_details(self, product_url):
        """
        Get details for a specific product.

        Args:
            product_url (str): Product page URL.

        Returns:
            dict: Product information.
        """
        pass

    def is_configured(self):
        """
        Check whether the scraper is properly configured.

        Returns:
            bool: True if configured, otherwise False.
        """
        return True

    @staticmethod
    def create_product(
        name=None,
        price=None,
        rating=None,
        availability=None,
        url=None,
        category=None,
        description=None,
        source=None,
        image_url=None
    ):
        """
        Create a standardized product dictionary.

        Args:
            name (str): Product name.
            price: Product price.
            rating: Product rating.
            availability (str): Product availability.
            url (str): Product page URL.
            category (str): Product category.
            description (str): Product description.
            source (str): Source website.
            image_url (str): Product image URL.

        Returns:
            dict: Standard product format.
        """

        # Fix common price encoding artifacts.
        if isinstance(price, str):
            price = price.replace("Â£", "£")
            price = price.replace("Â€", "€")
            price = price.replace("Â₹", "₹")
            price = price.replace("Â¥", "¥")

        return {
            "name": name,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": url,
            "category": category,
            "description": description,
            "source": source,
            "image_url": image_url
        }