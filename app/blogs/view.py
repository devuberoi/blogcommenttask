from model import Blog

def create_blog(parameters):
    response = {'http_status': 400}
    data = {}
    title = parameters.get('title', False)

    if not title or title == "":
        response['error'] = 'Title is required'
        return response

    data['title'] = title
    data['body'] = parameters.get('body', '')
    blog = Blog()
    result = blog.create(data)

    if not result:
        response['error'] = 'could not create blog post'
        return response

    response.update(blog.__dict__)
    response['http_status'] = 201
    return response

def get_blog(parameters, blog_id):
    response = {'http_status': 404}
    blog = Blog(blog_id)
    if not blog.exists:
        return response
    response.update(blog.__dict__)
    response['http_status'] == 200
    return response

def list_blogs(parameters):
    response = {'http_status': 404}
    try:
        page = int(parameters.get('page', 1))
        items = int(parameters.get('items', 5))
    except TypeError, e:
        print e
        respone['error'] = 'integer expectd for page and items'
        return response
    blog = Blog()
    all_blogs = blog.fetch_all(page, items)

    if not all_blogs:
        return response

    response['blogs'] = all_blogs
    response['page'] = page
    response['items'] = items
    response['http_status'] = 200
    return response

def create_comment(parameters, blog_id):
    response = {'http_status': 400}
    data = {}
    blog = Blog(blog_id)
    data['comment'] = parameters.get('comment', False)
    data['section_id'] = parameters.get('section_id', False)

    if not blog.exists:
        response['error'] = 'blog does not exist!'
        return response

    if not data['comment'] or not data['section_id'] or data['comment'] == "" or data['section_id'] == "":
        response['error'] = 'missing information'
        return response
    data['blog_id'] = blog_id
    result = blog.comment(data)
    if not result:
        response['error'] = 'comment not created'
        return response

    response.update(data)
    response['http_status'] = 201
    return response
