from compare import compare_products
from scrapers.amazon_scraper import scrape_amazon
from scrapers.flipkart_scraper import scrape_flipkart


def main():
    print("Program Started")

    print("Scraping Amazon...")
    amazon_df = scrape_amazon(max_pages=2, max_items=40)

    print("Scraping Flipkart...")
    flipkart_df = scrape_flipkart(max_pages=2, max_items=40)

    print("Comparing products...")
    comparison_df = compare_products(amazon_df, flipkart_df)

    print("Done")
    print(comparison_df.head(10))


if __name__ == "__main__":
    main()
