class PostService:
    def __init__(self, db):
        self.db = db

    def get_user_posts(self, users):
        # Violation: N+1 query problem
        posts = []
        for user in users:
            user_posts = self.db.query(f"""
                SELECT * FROM posts 
                WHERE user_id = {user['id']}
            """)
            posts.extend(user_posts)
        return posts

    def build_post_content(self, parts):
        # Violation: Inefficient string concatenation
        content = ""
        for part in parts:
            content += part
        return content

    def process_posts(self, posts):
        # Violation: Unnecessary list creation
        result = []
        for post in posts:
            result.append(self.transform_post(post))
        return result

    def get_all_comments(self, posts):
        # Violation: Multiple queries in loop
        all_comments = []
        for post in posts:
            comments = self.db.query(f"""
                SELECT * FROM comments 
                WHERE post_id = {post['id']}
            """)
            for comment in comments:
                user = self.db.query(f"""
                    SELECT * FROM users 
                    WHERE id = {comment['user_id']}
                """)
                comment['user'] = user
            all_comments.extend(comments)
        return all_comments

    def transform_post(self, post):
        # Dummy implementation
        return post 