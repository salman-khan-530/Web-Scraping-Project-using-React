import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [website, setWebsite] = useState("test");
  const [products, setProducts] = useState([]);

  // Loading and error states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const searchProducts = async () => {
    // Clear previous error
    setError("");

    // Check empty search
    if (!query.trim()) {
      setError("Please enter a product name.");
      return;
    }

    // Start loading
    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/products?website=${website}&query=${encodeURIComponent(
          query
        )}&max_products=10`
      );

      const data = await response.json();

      console.log(data);

      // Handle backend errors
      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setProducts(data.products);
    } catch (error) {
      console.error("Error:", error);

      setError(error.message);
      setProducts([]);
    } finally {
      // Stop loading
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>E-Commerce Product Scraper</h1>

      <p className="description">
        Search products from different websites.
      </p>

      <div className="search-area">

        <select
          value={website}
          onChange={(event) => setWebsite(event.target.value)}
        >
          <option value="test">Test Site</option>
          <option value="amazon">Amazon</option>
        </select>

        <input
          type="text"
          placeholder="Enter product name..."
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />

        <button onClick={searchProducts} disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>

      </div>

      {/* Error message */}
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Loading message */}
      {loading && (
        <p className="loading-message">
          Searching for products...
        </p>
      )}

      {/* Results count */}
      {products.length > 0 && (
        <p className="results-count">
          Found {products.length} products
        </p>
      )}

      {/* Products */}
      <div className="products">
        {products.map((product, index) => (
          <div className="product-card">
            {product.image_url && (
              <img
                src={product.image_url}
                alt={product.name}
                className="product-image"
              />
            )}
            <h3>{product.name}</h3>

            <p>
              <strong>Price:</strong> {product.price}
            </p>

            <p className="rating">
              <strong>Rating:</strong>{" "}
              <span className="stars">
                {"★".repeat(Number(product.rating) || 0)}
                {"☆".repeat(5 - (Number(product.rating) || 0))}
              </span>

              <span className="rating-number">
                {product.rating}/5
              </span>
            </p>

            <p>
              <strong>Availability:</strong> {product.availability}
            </p>

            <p>
              <strong>Category:</strong> {product.category}
            </p>

            <p>
              <strong>Source:</strong> {product.source}
            </p>

            <p>
              <strong>Description:</strong> {product.description}
            </p>

            {product.url && (
              <a
                href={product.url}
                target="_blank"
                rel="noopener noreferrer"
                className="product-link"
              >
                View Product
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;