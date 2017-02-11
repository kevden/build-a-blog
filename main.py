import os
import jinja2
import webapp2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Post(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
    	self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
    	t = jinja_env.get_template(template)
	return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
    	self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
    	t = jinja_env.get_template(template)
	return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

class PostHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
    	self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
    	t = jinja_env.get_template(template)
	return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        post = Post.get_by_id(int(id))
        if post:
            t = jinja_env.get_template('full_post.html')
            content = t.render(Post=post)
        else:
            content = '404'

        self.response.write(content)

class MainPage(MainHandler):
    def render_main(self, title="", body="", error=""):
        posts = db.GqlQuery("select * from Post order by created DESC limit 5")
        self.render("main.html", title = title, body = body, error = error, posts = posts)

    def get(self):
        self.render_main()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            p = Post(title = title, body = body)
            p.put()

            self.redirect("/")
        else:
            error = "We need title and a body"
            self.render_main(title, body, error)
	
class BlogPage(BlogHandler):

    def render_blog(self, title="", body=""):
        posts = db.GqlQuery("select * from Post order by created DESC limit 5")
        self.render("blog.html", title = title, body = body, posts = posts)

    def get(self):
        self.render_blog()

class NewPostPage(PostHandler):
    
    def render_main(self, title="", body="", error=""):
        self.render("posts.html", title = title, body = body, error = error)

    def get(self):
        self.render_main()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            p = Post(title = title, body = body)
            p.put()
            redirect = "/blog/" + str(p.key().id())

            self.redirect(redirect)
        else:
            error = "We need title and a body"
            self.render_main(title, body, error)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', BlogPage),
    ('/newpost', NewPostPage),
    (webapp2.Route('/blog/<id:\d+>', ViewPostHandler))
], debug=True)
