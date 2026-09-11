"""
Data processing, cleaning, standardization, and validation pipeline.
"""

import re
import pandas as pd
from scraper.logger import logger


def clean_text_encoding(text):
    """
    Fix common encoding artifacts in text (e.g. latin1 decoded as utf-8).
    """
    if not isinstance(text, str):
        return text

    # Common mojibake / encoding artifacts
    artifacts = {
        "Â£": "£",
        "Â€": "€",
        "Â₹": "₹",
        "Â¥": "¥",
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "â€“": "-",
        "â€”": "--",
    }
    for bad, good in artifacts.items():
        text = text.replace(bad, good)

    try:
        # Attempt standard latin1 to utf-8 recovery
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def clean_product_name(name):
    """
    Standardize product name by stripping extra spaces and artifacts.
    """
    if not isinstance(name, str):
        return "Unknown"

    name = clean_text_encoding(name)
    name = " ".join(name.strip().split())
    return name if name else "Unknown"


def clean_price(price):
    """
    Extract and convert price string to numeric float.
    Handles symbols (£, $, €, ₹), encoding artifacts (Â), commas, and text.

    Examples:
        "£51.77" -> 51.77
        "Â£51.77" -> 51.77
        "$29.99" -> 29.99
        "$1,249.50" -> 1249.50
    """
    if price is None or (isinstance(price, float) and pd.isna(price)):
        return None

    if isinstance(price, (int, float)):
        return round(float(price), 2) if price >= 0 else None

    price_str = str(price).strip()
    price_str = clean_text_encoding(price_str)

    # Remove currency symbols and common artifacts
    for symbol in ["£", "$", "€", "₹", "¥", "Â"]:
        price_str = price_str.replace(symbol, "")

    # Remove thousand-separator commas
    price_str = price_str.replace(",", "").strip()

    # Search for numeric decimal pattern
    match = re.search(r"(\d+(?:\.\d+)?)", price_str)
    if match:
        try:
            val = float(match.group(1))
            return round(val, 2)
        except ValueError:
            return None

    return None


def clean_rating(rating):
    """
    Convert string or numeric rating into standard float between 1 and 5.

    Examples:
        "One" -> 1.0
        "Five" -> 5.0
        "4 out of 5" -> 4.0
        4.5 -> 4.5
    """
    if rating is None or (isinstance(rating, float) and pd.isna(rating)):
        return None

    word_map = {
        "one": 1.0,
        "two": 2.0,
        "three": 3.0,
        "four": 4.0,
        "five": 5.0
    }

    # If it's a list (such as CSS classes from BeautifulSoup)
    if isinstance(rating, (list, tuple)):
        for item in rating:
            item_lower = str(item).strip().lower()
            if item_lower in word_map:
                return word_map[item_lower]
        return None

    # If already a number
    if isinstance(rating, (int, float)):
        val = float(rating)
        return val if 1.0 <= val <= 5.0 else None

    # If it's a string
    rating_str = str(rating).strip().lower()
    if rating_str in word_map:
        return word_map[rating_str]

    # Look for numeric patterns like "4", "4.5", "4 out of 5"
    match = re.search(r"(\d+(?:\.\d+)?)", rating_str)
    if match:
        try:
            val = float(match.group(1))
            if 1.0 <= val <= 5.0:
                return round(val, 1)
        except ValueError:
            pass

    return None


def clean_availability(availability):
    """
    Standardize product availability strings.
    """
    if not isinstance(availability, str):
        return "Unknown"

    text = clean_text_encoding(availability).strip().lower()
    if not text:
        return "Unknown"

    if "in stock" in text or "available" in text:
        return "In Stock"
    if "out of stock" in text or "unavailable" in text:
        return "Out of Stock"

    return " ".join(availability.strip().split()).title()


def handle_missing_values(df):
    """
    Handle missing values gracefully across all product fields.
    Does not drop records for missing optional attributes.
    """
    df = df.copy()

    if "name" in df.columns:
        df["name"] = df["name"].fillna("Unknown")
    if "availability" in df.columns:
        df["availability"] = df["availability"].fillna("Unknown")
    if "url" in df.columns:
        df["url"] = df["url"].fillna("N/A")
    if "category" in df.columns:
        df["category"] = df["category"].fillna("Unknown")
    if "description" in df.columns:
        df["description"] = df["description"].fillna("No description available")
    if "source" in df.columns:
        df["source"] = df["source"].fillna("Unknown")

    return df


def remove_duplicates(df):
    """
    Remove duplicate products based on URL and exact matching.
    """
    before = len(df)

    # 1. Deduplicate identical rows
    df = df.drop_duplicates()

    # 2. Deduplicate on valid URL when present
    if "url" in df.columns:
        valid_url_mask = (
            df["url"].notna()
            & (df["url"].astype(str).str.strip() != "")
            & (df["url"].astype(str) != "N/A")
        )

        df_with_url = df[valid_url_mask].drop_duplicates(subset=["url"], keep="first")
        df_without_url = df[~valid_url_mask]
        df = pd.concat([df_with_url, df_without_url], ignore_index=True)

    removed = before - len(df)
    logger.info(f"Duplicates removed: {removed}")
    return df


def validate_data(df):
    """
    Validate product records.
    Requires valid name and URL.
    Validates price and rating only when present (does not drop if missing).
    """
    before = len(df)
    df = df.copy()

    # Name must be valid non-empty string and not "Unknown"
    valid_name = (
        df["name"].notna()
        & (df["name"].astype(str).str.strip() != "")
        & (df["name"].astype(str).str.strip().str.lower() != "unknown")
    )

    # URL must be valid
    valid_url = (
        df["url"].notna()
        & (df["url"].astype(str).str.strip() != "")
        & (df["url"].astype(str).str.strip() != "N/A")
        & (df["url"].astype(str).str.strip().str.startswith(("http://", "https://")))
    )

    # Price validation: valid when present (>= 0)
    if "price" in df.columns:
        valid_price = df["price"].isna() | (df["price"] >= 0)
    else:
        valid_price = pd.Series(True, index=df.index)

    # Rating validation: valid when present (between 1 and 5)
    if "rating" in df.columns:
        valid_rating = df["rating"].isna() | (df["rating"].between(1, 5))
    else:
        valid_rating = pd.Series(True, index=df.index)

    valid_mask = valid_name & valid_url & valid_price & valid_rating
    cleaned_df = df[valid_mask].reset_index(drop=True)

    removed = before - len(cleaned_df)
    logger.info(f"Invalid records removed: {removed}")
    return cleaned_df


def clean_data(df):
    """
    Full data cleaning and validation pipeline.
    """
    if df is None or df.empty:
        logger.warning("Empty DataFrame passed to clean_data.")
        return pd.DataFrame()

    df = df.copy()

    # Clean individual columns
    if "name" in df.columns:
        df["name"] = df["name"].apply(clean_product_name)

    if "price" in df.columns:
        df["price"] = df["price"].apply(clean_price)

    if "rating" in df.columns:
        df["rating"] = df["rating"].apply(clean_rating)

    if "availability" in df.columns:
        df["availability"] = df["availability"].apply(clean_availability)

    if "category" in df.columns:
        df["category"] = df["category"].apply(
            lambda x: clean_text_encoding(str(x)).strip() if pd.notna(x) else "Unknown"
        )

    if "description" in df.columns:
        df["description"] = df["description"].apply(
            lambda x: clean_text_encoding(str(x)).strip() if pd.notna(x) else "No description available"
        )

    # Handle missing values
    df = handle_missing_values(df)

    # Remove duplicates
    df = remove_duplicates(df)

    # Validate records
    df = validate_data(df)

    return df