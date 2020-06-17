import logging
import asyncio
import time
from collections import Counter

import asyncclick as click
from codetiming import Timer

from utils import get_tags_list, get_tags_list_async

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s',
    level='INFO'
)


@click.command()
@click.option('--query', type=str, help='Query on GitHub.com')
@click.option('--pages-count', type=int, help='Pages count for analysis', default=1)
@click.option('--top', type=int, default=1)
@click.option('--timeout', type=int, default=1)
@click.option('--retries-count', type=int, default=1)
async def main(query, pages_count, top, timeout, retries_count):

    url = 'https://github.com/search'

    logger.info('Sync approach')
    with Timer(text="\nTotal elapsed time: {:.1f}s"):
        tags_list = get_tags_list(url, query, pages_count, retries_count)
        tags_counter = Counter(tags_list)
        logger.info('--- Results ---')
        logger.info(f'Total tags count: {len(tags_list)}')
        for top_tag in tags_counter.most_common(top):
            logger.info(f'Tag {top_tag[0]} has {top_tag[1]} usages')

    sleep_time = timeout * (1 + (pages_count // 60) + (retries_count*timeout // 60))
    logger.info(f'Some sleep for {sleep_time}s before async approach')
    time.sleep(sleep_time)

    logger.info('Async approach')
    with Timer(text="\nTotal elapsed time: {:.1f}s"):
        tags_list = await get_tags_list_async(url, query, pages_count, timeout, retries_count)
        tags_counter = Counter(tags_list)
        logger.info('--- Results ---')
        logger.info(f'Total tags count: {len(tags_list)}')
        for top_tag in tags_counter.most_common(top):
            logger.info(f'Tag {top_tag[0]} has {top_tag[1]} usages')


if __name__ == '__main__':
    asyncio.run(main(_anyio_backend="asyncio"))
