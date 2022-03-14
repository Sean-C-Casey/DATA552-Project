from ast import Sub
import praw

from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET


class RedditConnection(object):

    def __init__(self) -> None:
        self._client = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="monitorbot v0.1"
        )
        self._subredit = self._client.subreddit("UkrainianConflict")
    
    def get_top_n(self, n: int) -> list["praw.models.Submission"]:
        submissions = []
        count = 0
        posts = list(self._subredit.hot(limit=2*n))
        index = 0
        while count < n:
            post = posts[index]
            index += 1
            if not post.stickied:
                submissions.append(post)
                count += 1
        return submissions


def test():
    reddit = RedditConnection()

    Submission = praw.models.Submission
    post: Submission
    for post in reddit.get_top_n(3):
        print(post.title, "\n")


if __name__ == "__main__":
    test()