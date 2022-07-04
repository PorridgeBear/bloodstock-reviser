import scrapy


class BandsSpider(scrapy.Spider):
    name = "bands"
    base_url = 'https://www.bloodstock.uk.com'
    start_urls = [
        f'{base_url}/events/boa-2022/stages',
    ]

    def parse(self, response):
        band_links = response.css('.line_up__bands a::attr(href)').getall()
        for band_link in band_links:
            yield scrapy.Request(f'{self.base_url}/{band_link}', callback=self.parse_band)

    def parse_band(self, response):
        name = response.css('h3.band__name::text').get().strip()
        playing_and_stage = response.css('.band__summary p::text').getall()
        playing = playing_and_stage[1].strip()
        stage = playing_and_stage[3].strip()

        yield {
            'name': name,
            'playing': playing,
            'stage': stage,
        }