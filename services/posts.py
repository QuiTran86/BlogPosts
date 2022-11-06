from infrastructure.models.posts import Comment, Post


class PostService:

    def __init__(self):
        self._post_model = Post
        self._comment_model = Comment

    def find_post_by_id(self, id):
        return self._post_model.query.filter_by(id=id).first()

    def find_comment_by_id(self, id):
        return self._comment_model.query.filter_by(id=id).first()

    def find_comments_by_post_id(self, id):
        post = self.find_post_by_id(id)
        return post.comments

    def mark_comment_as_disable_state(self, id):
        comment = self.find_comment_by_id(id)
        comment.disabled = True
        comment.save()

    def mark_comment_as_enable_state(self, id):
        comment = self.find_comment_by_id(id)
        comment.disabled = False
        comment.save()
