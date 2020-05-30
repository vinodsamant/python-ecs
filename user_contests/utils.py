import json
import os

import requests
from twython import Twython

from user_contests.constants import (FACEBOOK_BASE_URL, POST_FEED_URL, CLIENT_ID,
                                     LIMIT, LIMIT_MAX, POST_COMMENT_URL, REACTION_TYPE_URL)


class c_twitter:
    """
    This class is used to perform every kind of operations like post message on wall,
    Get list of friends and followers.
    Get count of likes.
    Get details of post on the basis of post ID.
    """

    def __init__(self):
        """
        This is the init method used to call initially to set value as global within the class.
        """
        self.twitter = Twython(
            os.getenv('TWITTER_CONSUMER_KEY'),
            os.getenv('TWITTER_CONSUMER_SECRET'),
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        )

    def create_status(self, message):
        """
        This method is used to post status on wall.
        :param message: This is the message to be posted on the wall.
        :return: It will return the object with post ID.
        """
        return self.twitter.update_status(status=message)

    def get_post_details(self, status_id):
        """
        This method is used to get details of posted status.
        :param status_id: This is the id to fetch details of specific status.
        :return: It will return the object with post ID.
        """
        return self.twitter.show_status(id=status_id)

    def get_followers_list(self):
        """
        This method is used to get list of followers.
        :return: It will return list of followers.
        """
        return self.twitter.get_followers_list()

    def get_re_tweets(self, status_id):
        """
        This method is used to get details of re_tweets.
        :param status_id: This is the id to fetch details of specific status.
        :return: It will return list of re_tweets.
        """
        return self.twitter.get_retweets(status_id)


class c_facebook:

    def get_latest_post(self, facebook_id, access_token, user_id=None):
        """
        This method is used to get the latest post from the facebook wall using post id.
        :param facebook_id: This is the facebook id.
        :param user_id: This is the user id.
        :return: Details of post.
        """
        # obj = UserContestsModel.objects.filter(user_id=user_id)
        # if obj:
        # access_token = obj.access_token
        # facebook_id = "2856354727749695"
        url = (FACEBOOK_BASE_URL + facebook_id + POST_FEED_URL
               + "?access_token=" + access_token
               + "&client_id=" + CLIENT_ID
               + "&limit=" + LIMIT)
        result = requests.request("GET", url)
        if result:
            json_result = json.loads(result.text)
            feed_id = json_result['data'][0]['id']

            return feed_id

    def get_likes_count(self, feed_id, access_token):
        """
        This method is used to get total likes count on particular feed.
        :param feed_id: This is the feed id.
        :return: Total Likes Count of feed.
        """
        # obj = UserContestsModel.objects.filter(feed_id=feed_id)
        # if not obj:
        url = (FACEBOOK_BASE_URL + feed_id
               + "?access_token=" + access_token
               + "&limit=" + LIMIT_MAX
               + "&fields=" + REACTION_TYPE_URL)
        result = requests.request("GET", url)
        if result:
            json_result = json.loads(result.text)
            count = json_result['summary']['total_count']
            return count

    def get_comments_count(self, feed_id, access_token):
        """
        This method is used to get total comments count on particular feed.
        :param feed_id: This is the feed id.
        :return: Total Comments Count of feed.
        """
        # obj = UserContestsModel.objects.filter(feed_id=feed_id)
        # if obj:
        url = (FACEBOOK_BASE_URL + feed_id + POST_COMMENT_URL
               + "?access_token=" + access_token
               + "&limit=" + LIMIT_MAX
               + "&summary=total_count")
        result = requests.request("GET", url)
        if result:
            json_result = json.loads(result.text)
            count = json_result['summary']['total_count']
            return count
