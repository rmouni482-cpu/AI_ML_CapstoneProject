import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
EXCHANGE_RATE_INR = 105.0  # Approximate conversion rate for GBP to INR


def scrape_books(max_pages=3):
  """Scrapes book data across multiple pages."""
  books_data = []

  for page in range(1, max_pages + 1):
    url = BASE_URL.format(page)
    response = requests.get(url)
    if response.status_code != 200:
      break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
      title = book.h3.a["title"]

      # Clean Price
      price_str = (
          book.find("p", class_="price_color").text.strip().replace("£", "")
      )
      price_gbp = float(price_str)
      price_inr = round(price_gbp * EXCHANGE_RATE_INR, 2)

      # Clean Star Rating
      rating_map = {
          "One": 1,
          "Two": 2,
          "Three": 3,
          "Four": 4,
          "Five": 5,
      }
      rating_class = book.p["class"][1]
      star_rating = rating_map.get(rating_class, 0)

      # Clean Availability
      availability = book.find("p", class_="instock availability").text.strip()
      in_stock = 1 if "In stock" in availability else 0

      # Category (Note: category requires visiting the book page or inferring;
      # for simplicity in this scraper stub, we assign a sample category tag)
      category = "Books"

      books_data.append({
          "title": title,
          "price_gbp": price_gbp,
          "price_inr": price_inr,
          "star_rating": star_rating,
          "in_stock": in_stock,
          "category_name": category,
      })

  return pd.DataFrame(books_data)


def save_to_sqlite(df):
  """Stores data into a normalized SQLite database with Categories and Books tables."""
  conn = sqlite3.connect("store.db")
  cursor = conn.cursor()

  # Create Categories table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE
        )
    """)

  # Create Books table with Foreign Key
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price_gbp REAL,
            price_inr REAL,
            star_rating INTEGER,
            in_stock INTEGER,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
    """)

  # Insert unique categories and map IDs
  for cat in df["category_name"].unique():
    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)", (cat,)
    )
  conn.commit()

  # Fetch category mapping
  cat_df = pd.read_sql("SELECT * FROM categories", conn)
  cat_map = dict(zip(cat_df["category_name"], cat_df["category_id"]))
  df["category_id"] = df["category_name"].map(cat_map)

  # Insert books data
  df[[
      "title",
      "price_gbp",
      "price_inr",
      "star_rating",
      "in_stock",
      "category_id",
  ]].to_sql("books", conn, if_exists="replace", index=False)

  conn.close()
  print("Database created and populated successfully!")


if __name__ == "__main__":
  # 1. Scrape Data
  print("Scraping books...")
  df_books = scrape_books(max_pages=3)
  print(f"Collected {len(df_books)} books.")

  # 2. Save to SQLite Database
  save_to_sqlite(df_books)

  # 3. Run Sample SQL & Pandas Join verification
  conn = sqlite3.connect("store.db")
  query = """
        SELECT b.title, b.price_gbp, c.category_name 
        FROM books b 
        JOIN categories c ON b.category_id = c.category_id 
        LIMIT 5
    """
  print("\n--- SQL Join Query Result ---")
  print(pd.read_sql(query, conn))
  conn.close()