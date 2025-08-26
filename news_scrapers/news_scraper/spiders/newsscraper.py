import scrapy
import pandas as pd


class NewsscraperSpider(scrapy.Spider):
    name = "newsscraper"

    # Start URLs (add more websites as needed)
    start_urls = [
        "https://www.indiatoday.in/",  # India Today
        "https://www.timesnownews.com/",  # Times Now
    ]

    def parse(self, response):
        if "indiatoday" in response.url:
            url_list = response.css('nav ul li a::attr(href)').getall()
            for url in url_list:
                yield response.follow(url, self.parse_india_today)

        elif "timesnownews" in response.url:
            url_list = response.css('ul li a::attr(href)').getall()
            for url in url_list:
                yield response.follow(url, self.parse_times_now)

    def parse_india_today(self, response):
        titles = response.css('h1::text, h2::text, h3::text, h4::text').getall()
        paragraphs = response.css('p::text').getall()
        self.save_to_csv(titles, paragraphs, "India_Today")

    def parse_times_now(self, response):
        titles = response.css('h1::text, h2::text, h3::text, h4::text').getall()
        paragraphs = response.css('p::text').getall()
        self.save_to_csv(titles, paragraphs, "Times_Now")

    def save_to_csv(self, titles, paragraphs, source):
    # Adjust lengths if mismatched
        min_length = min(len(titles), len(paragraphs))
        titles = titles[:min_length]
        paragraphs = paragraphs[:min_length]

        # Combine the titles, paragraphs, and source into a DataFrame
        data = {
            "Title": titles,
            "Paragraph": paragraphs,
            "Source": [source] * min_length,
            "Truth": [1] * min_length,  # Assuming all are real news
        }
        df = pd.DataFrame(data)

        # Check if the CSV file exists and append new data
        try:
            existing_df = pd.read_csv("news_data_with_truth.csv")

            # Check for duplicates
            merged_df = pd.concat([existing_df, df])
            duplicates = merged_df.duplicated(subset=["Title", "Paragraph"], keep=False)

            if duplicates.any():
                duplicate_entries = merged_df[duplicates]
                self.log(f"Duplicate entries found:\n{duplicate_entries}")

            # Remove duplicates and save updated DataFrame
            combined_df = merged_df.drop_duplicates(subset=["Title", "Paragraph"], ignore_index=True)
        except Exception as e:
            print("sagar -->> ",e)
            combined_df = df

        
        # Save the updated DataFrame back to the CSV
        combined_df.to_csv("news_data_with_truth.csv", index=False)

        self.log(f"Saved {len(df)} entries from {source} to CSV (including deduplication).")


# Command to run Scrapy and save to CSV:
# scrapy runspider news_spider.py
