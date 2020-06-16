Async_test

Testing asynchronous requests.
Program will count tags on github repos in 2 ways: using requests library and aiohttp.

Program counts tags on github repos.
There are 5 params:
1. `--query` - Query for repos search.
2. `--pages-count` - Pages count where tags will be counted. Default = 1.
3. `--top` - How many top tags to show. Default = 1.
4. `--timeout` - Timeout for cases when status code != 200. Default = 1.
5. `--retries-count` - Retries count for cases when status code != 200. Default = 1.

Sometimes for big values of `--pages-count` sync and async approaches can show different results. The reason of that is GutHub.com defence versus abuse.