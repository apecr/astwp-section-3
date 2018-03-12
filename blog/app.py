from blog import Blog
MENU_PROMPT = 'Enter "c" to create a blog, "l" to list blogs, "r" to read one, "p" to create a post, or "q" to quit: '
POST_TEMPLATE = '''
    --- {} ---

    {}

    '''

blogs = dict()

def menu():
    # Show the user the available blogs
    # Let the user make a choice
    # Do something with that choice
    # Eventually exist
    print_blogs()
    selection = input(MENU_PROMPT)
    while selection != 'q':
        if selection == 'c':
            ask_create_blog()
        elif selection == 'l':
            print_blogs()
        elif selection == 'r':
            ask_read_blog()
        elif selection == 'p':
            ask_create_post()
        selection = input(MENU_PROMPT)

def print_blogs():
    for key, blog in blogs.items():
        print('- {}'.format(blog))

def ask_create_blog():
    title = input('Enter your blog title: ') 
    author = input('Enter your author name: ')
    blogs[title] = Blog(title, author)

def ask_read_blog():
    # // ask blog title
    title = input('What blog do you want to read: ')
    print_posts(blogs[title])

def print_posts(blog):
    for post in blog.posts:
        print_post(post)

def print_post(post):
    print(POST_TEMPLATE.format(post.title, post.content))

def ask_create_post():
    # // Title, content
    pass