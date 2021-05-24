
import uuid


from flask_injector import inject

from services.elasticsearch import ElasticSearchIndex


class Post(object):
    @inject(indexer=ElasticSearchIndex)
    def post(self, indexer: ElasticSearchIndex, post: dict) -> dict:
        """
        This wil return a location, kind of 'Camden, London'.
        We need to have some data like lat/lon for that input.
        """
        if indexer.exists_by_url(post['url']):
            # 409 HTTP Conflict
            return post, 409

        # Generates a unique ID for the room
        post['id'] = str(uuid.uuid4())

        if not indexer.index(post):
            return {"error": "Post not saved"}, 400

        return post, 201


class_instance = Post()
