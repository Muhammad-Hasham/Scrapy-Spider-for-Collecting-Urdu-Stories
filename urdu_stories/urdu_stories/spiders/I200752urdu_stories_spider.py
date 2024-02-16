# Muhammad Hasham Ul Haq 
# I200752
# i200752@nu.edu.pk
import scrapy
import re
from scrapy.exporters import CsvItemExporter

# Define a dictionary for replacing English numbers with Urdu numbers
number_mapping = {
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹',
}

class I200752urduStoriesSpiderSpider(scrapy.Spider):
    name = "I200752urdu_stories_spider"
    allowed_domains = ["www.urduzone.net"]
    start_urls = ["https://www.urduzone.net/page/{}/?s".format(page) for page in range(1, 227)]

    def __init__(self, *args, **kwargs):
        super(I200752urduStoriesSpiderSpider, self).__init__(*args, **kwargs)
        self.csv_exporter = None

    def open_spider(self, spider):
        # Specify the file path for the CSV file
        self.csv_exporter = CsvItemExporter(open('urdu_stories.csv', 'wb'))
        self.csv_exporter.fields_to_export = ['Title', 'Urdu Story']
        self.csv_exporter.start_exporting()

    def close_spider(self, spider):
        if self.csv_exporter:
            self.csv_exporter.finish_exporting()

    def parse(self, response):
        # Extract links to story pages along with titles
        story_links = response.css('h3 a::attr(href)').getall()
        story_titles = response.css('h3 a::text').getall()
        
        for story_link, title in zip(story_links, story_titles):
            yield scrapy.Request(url=story_link, callback=self.parse_story, meta={'title': title})

    def parse_story(self, response):
        title = response.meta['title']
        urdu_text = " ".join(response.css('p[dir="rtl"]::text').extract())
        cleaned_urdu_text = self.clean_urdu_text(urdu_text)
        
        if cleaned_urdu_text:
            item = {
                'Title': title,
                'Urdu Story': cleaned_urdu_text
            }
            yield item

    def clean_urdu_text(self, text):
        # Remove HTML entities and extra spaces
        cleaned_text = re.sub(r'&[^;]+;', '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        # Replace English numbers with Urdu numbers
        for eng_num, urdu_num in number_mapping.items():
            cleaned_text = cleaned_text.replace(eng_num, urdu_num)
        
        # Remove non-Urdu characters
        cleaned_text = re.sub(r'[^\s\u0600-\u06FF]+', '', cleaned_text)
        
        return cleaned_text
