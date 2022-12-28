import asyncio
import json
import math
import re
from typing import List, Optional
from urllib.parse import urljoin

from loguru import logger as log
from scrapfly import ScrapeApiResponse, ScrapeConfig, ScrapflyClient
from typing_extensions import TypedDict

scrapfly = ScrapflyClient(key='scp-live-8b481cd7ca0d4276be0ab7f45d8f1861')


class ReviewData(TypedDict):
    title: str
    text: str
    location_and_date: str
    verified: bool
    rating: float


def parse_reviews(result: ScrapeApiResponse):
    """parse review from single review page"""
    review_boxes = result.selector.css("#cm_cr-review_list div.review")
    parsed = []
    for box in review_boxes:
        parsed.append(
            {
                "text": "".join(box.css("span[data-hook=review-body] ::text").getall()).strip(),
                "title": box.css("*[data-hook=review-title]>span::text").get(),
                "location_and_date": box.css("span[data-hook=review-date] ::text").get(),
                "verified": bool(box.css("span[data-hook=avp-badge] ::text").get()),
                "rating": box.css("*[data-hook*=review-star-rating] ::text").re(r"(\d+\.*\d*) out")[0],
            }
        )
    return parsed


async def scrape_reviews(asin: str, session: ScrapflyClient):
    """scrape all reviews of a given ASIN of an amazon product"""
    # need to change URL for UK ONE
    url = f"https://www.amazon.com/product-reviews/{asin}/"
    log.info(f"scraping review page: {url}")
    # find first page
    first_page_result = await session.async_scrape(ScrapeConfig(url, country="US"))
    total_reviews = first_page_result.selector.css("div[data-hook=cr-filter-info-review-rating-count] ::text").re(
        r"(\d+,*\d*)"
    )[1]
    total_reviews = int(total_reviews.replace(",", ""))
    total_pages = int(math.ceil(total_reviews / 10.0))

    log.info(f"found total {total_reviews} reviews across {total_pages} pages -> scraping")
    _next_page = urljoin(url, first_page_result.selector.css(".a-pagination .a-last>a::attr(href)").get())
    next_page_urls = [_next_page.replace("pageNumber=2", f"pageNumber={i}") for i in range(1, total_pages + 1)]
    assert len(set(next_page_urls)) == len(next_page_urls)

    reviews = parse_reviews(first_page_result)
    async for result in session.concurrent_scrape([ScrapeConfig(url, country="US") for url in next_page_urls]):
        reviews.extend(parse_reviews(result))
    log.info(f"scraped total {len(reviews)} reviews")
    return reviews


async def run():
    with ScrapflyClient(key="scp-live-8b481cd7ca0d4276be0ab7f45d8f1861", max_concurrency=2) as session:
        product_result = await scrape_reviews("B08YY76XRW", session=session)
        print(product_result)
        return



if __name__ == "__main__":
    asyncio.run(run())