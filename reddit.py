import asyncpraw
import asyncio
import re

from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET


class RedditConnection(object):
    # Static factory method
    @classmethod
    async def get_connection(cls) -> "RedditConnection":
        connection = cls()
        connection._subreddit = await connection._client.subreddit("UkrainianConflict")
        return connection

    # Constructor
    def __init__(self) -> None:
        self._client = asyncpraw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="monitorbot v0.1"
        )
        # self._subredit = self._client.subreddit("UkrainianConflict")
        self._subreddit = None
    
    # For avoiding aiohttp "Unclosed client session" errors
    async def dispose(self):
        await self._client.close()
    
    async def get_top_n(self, n: int, skip_twitter: bool = True) -> list["asyncpraw.models.Submission"]:
        submissions = list()
        count = 0
        query_limit = max(6, 3 * n)
        posts = [post async for post in self._subreddit.hot(limit=query_limit)]
        index = 0
        while count < n and index < query_limit:
            post = posts[index]
            index += 1

            if skip_twitter and self.is_twitter(post):
                continue

            if not post.stickied:
                submissions.append(post)
                count += 1

        try_n = n
        while len(submissions) == 0:
            try_n *= 3
            submissions = await self.get_top_n(try_n)

        return submissions[:n]
    
    @staticmethod
    def is_twitter(submission: "asyncpraw.models.Submission") -> bool:
        regex = "^https?:\/\/(.*\.[a-z]*)\/.*$"
        url = submission.url
        matches = re.match(regex, url)
        try:
            base_url = matches[1]
            return "twitter" in base_url.lower()
        except IndexError:
            return False


async def test():
    reddit = await RedditConnection.get_connection()
    for post in await reddit.get_top_n(3):
        print(post.url, "\n")
    await reddit.dispose()


if __name__ == "__main__":
    asyncio.run(test())