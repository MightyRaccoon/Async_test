"""
File with some custom functions for async programs tests
"""
import logging
import requests
from typing import List, Text
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

from aiohttp_retry import RetryClient
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def get_tags_list(url: str, query: str, pages_count: int, retries_count: int) -> List[str]:
    """
    Return tags list from `url` with `query`
    :param url: URL for `query`
    :param query: Query for repos search
    :param pages_count: Pages count for tags list creation
    :param retries_count: retries count in case of status code != 200
    :return: List with tags
    """
    tags_list = []
    retry = Retry(total=retries_count, backoff_factor=2, raise_on_status=True, status_forcelist=[429])
    with requests.Session() as session:
        adapter = HTTPAdapter(max_retries=retry)
        session.mount(prefix='https://', adapter=adapter)
        for page_num in range(1, pages_count + 1):
            logger.debug(f'Page №{page_num} request')
            params = {
                'p': page_num,
                'q': query,
                'type': 'Repositories',
                's': 'stars'
            }
            request_result = session.get(url=url, params=params)
            logger.debug(f'Page №{page_num} processing')
            soup = BeautifulSoup(request_result.content, 'lxml')
            for tag in soup.find_all('a', attrs={'class': 'topic-tag topic-tag-link f6 px-2 mx-0'}):
                tags_list.append(tag.text.strip())
            logger.debug(f'Tags count after Page №{page_num} processing: {len(tags_list)}')
    return tags_list


async def fetch(client: RetryClient, query_string: str, timeout: int, retries_count: int) -> Text:
    """
    Fetch result of query
    :param client: Client with retry mechanism
    :param query_string: Full query string for repos getting
    :param timeout: timeout between retries in case of status code != 200
    :param retries_count: retries count in case of status code != 200
    :return:
    """
    async with client.get(
            url=query_string,
            retry_attempts=retries_count,
            retry_start_timeout=timeout,
            retry_factor=2,
            retry_max_timeout=timeout*(2**retries_count),
            retry_for_statuses=[429]) as response:
        return await response.text()


async def get_tags_list_async(url: str, query: str, pages_count: int, timeout, retries_count) -> List[str]:
    """
    Return tags list from `url` with `query`. Works asynchronous.
    :param url: URL for `query`
    :param query: Query for repos search
    :param pages_count: Pages count for tags list creation
    :param timeout: timeout between retries in case of status code != 200
    :param retries_count: retries count in case of status code != 200
    :return: List with tags
    """
    tags_list = []
    async with RetryClient() as client:
        for page_num in range(1, pages_count + 1):
            logger.debug(f'Page №{page_num} request')
            query_string = url + '?p=' + str(page_num) + '&q=' + query + '&type=Repositories&s=stars'
            request_result = await fetch(client, query_string, timeout, retries_count)
            logger.debug(f'Page №{page_num} processing')
            soup = BeautifulSoup(request_result, 'lxml')
            for tag in soup.find_all('a', attrs={'class': 'topic-tag topic-tag-link f6 px-2 mx-0'}):
                tags_list.append(tag.text.strip())
            logger.debug(f'Tags count after Page №{page_num} processing: {len(tags_list)}')
    return tags_list
