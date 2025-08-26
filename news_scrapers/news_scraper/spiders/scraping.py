import scrapy

class NestedDivSpider(scrapy.Spider):
    name = "nested_div"
    
    # Replace this with the URL of the target website
    start_urls = ['https://www.indiatoday.in/']

    def parse(self, response):
        # Select all top-level divs
        top_divs = response.css('div')

        for div in top_divs:
            # Attempt to extract <li> elements inside this <div>
            
            li_elements = div.css('li')

            if li_elements:  # If <li> elements are found
                for li in li_elements:
                    # Try to extract links from <li>
                    link = li.css('a::attr(href)').get()
                    if link:
                        yield {'link': response.urljoin(link)}  # Save the absolute URL
            else:
                # If no <li> is present, check nested divs
                nested_divs = div.css('div')
                if nested_divs:
                    for nested_div in nested_divs:
                        yield from self.parse_nested_div(nested_div)

    def parse_nested_div(self, div):
        """Recursively process nested divs."""
        li_elements = div.css('li')
        if li_elements:  # If <li> elements are found
            for li in li_elements:
                # Extract the link inside <li>
                link = li.css('a::attr(href)').get()
                if link:
                    yield {'link': response.urljoin(link)}  # Save the absolute URL
        else:
            # Check deeper nested <div> elements
            deeper_divs = div.css('div')
            for deeper_div in deeper_divs:
                yield from self.parse_nested_div(deeper_div)
