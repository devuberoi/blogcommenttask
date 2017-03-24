from tools import Postgres
from tools.Toolkit import get_timestamp
from uuid import uuid4

class Blog:
    exists = False
    __TABLE_BLOG = 'blogs'
    __TABLE_COMMENT = 'comments'
    __FIELDS_BLOG = ['blog_id', 'title', 'body', 'timestamp']
    __FIELDS_COMMENT = ['blog_id', 'section_id', 'comment', 'timestamp']

    def __init__(self, blog_id=None):
        for a_field in self.__FIELDS_BLOG:
            setattr(self, a_field, None)
        if blog_id is not None:
            b = self.fetch_one(blog_id)
            if b is not None:
                self.exists = True
                for each_attr in b:
                    setattr(self, each_attr, b[each_attr])
                self.fetch_comments()

    def update_attr(self, data):
        for each_attr in data:
            setattr(self, each_attr, data[each_attr])

    def fetch_one(self, blog_id):
        try:
            db = Postgres.init()
            cursor = Postgres.get_cursor(db, 'realdict')
            query = "SELECT " + ', '.join(self.__FIELDS_BLOG) + " FROM " + self.__TABLE_BLOG + " WHERE blog_id = %(blog_id)s"
            query_dict = {
                            'blog_id': blog_id
                         }
            cursor.execute(query, query_dict)
            result = cursor.fetchone()
            return result
        except Exception, e:
            print 'model fetch one error :: ', e
            return False

    def fetch_all(self, page, items):
        try:
            db = Postgres.init()
            cursor = Postgres.get_cursor(db, 'realdict')
            query = "SELECT " + ', '.join(self.__FIELDS_BLOG) + " FROM " + self.__TABLE_BLOG + " ORDER BY timestamp desc LIMIT %(limit)s OFFSET %(offset)s"
            query_dict = {
                            'offset': (page-1)*items,
                            'limit': items,
                        }
            cursor.execute(query, query_dict)
            result = cursor.fetchall()
            db.close()
            return result
        except Exception, e:
            print 'model fetch all blogs error :: ', e
            return False

    def fetch_comments(self):
        try:
            db = Postgres.init()
            cursor = Postgres.get_cursor(db, 'realdict')
            query = "SELECT array_agg(comment ORDER BY timestamp asc) AS comments, section_id FROM comments WHERE blog_id = %(blog_id)s GROUP BY section_id"
            query_dict = {'blog_id': self.blog_id}
            cursor.execute(query, query_dict)
            result = cursor.fetchall()
            self.comments = {row['section_id']: row['comments'] for row in result}
            db.close()
            return True
        except Exception, e:
            print 'model fetch comments error :: ', e
            db.close()
            return False

    def create(self, data):
        try:
            db = Postgres.init()
            cursor = Postgres.get_cursor(db, 'realdict')
            field_str = ",".join(self.__FIELDS_BLOG)
            query = "INSERT INTO " + self.__TABLE_BLOG + " (" + field_str + ") VALUES ( %(" + ")s, %(".join(self.__FIELDS_BLOG)+")s ) RETURNING " + field_str
            data['blog_id'] = str(uuid4())
            data['timestamp'] = get_timestamp()
            cursor.execute(query, data)
            db.commit()
            result = cursor.fetchone()
            db.close()
            self.update_attr(result)
            return True
        except Exception, e:
            print 'model create blog error :: ', e
            db.rollback()
            db.close()
            return False

    def comment(self, data):
        try:
            db = Postgres.init()
            cursor = Postgres.get_cursor(db, 'realdict')
            field_str = ",".join(self.__FIELDS_COMMENT)
            query = "INSERT INTO " + self.__TABLE_COMMENT + " (" + field_str + ") VALUES ( %(" + ")s, %(".join(self.__FIELDS_COMMENT)+")s ) RETURNING " + field_str
            data['timestamp'] = get_timestamp()
            cursor.execute(query, data)
            db.commit()
            result = cursor.fetchone()
            db.close()
            return result
        except Exception, e:
            print 'model create comment error :: ', e
            db.rollback()
            db.close()
            return False
