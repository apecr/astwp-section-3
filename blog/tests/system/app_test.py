from unittest import TestCase
from unittest.mock import patch
import app
from blog import Blog
from post import Post
import unittest


class AppTest(TestCase):
    def test_print_blogs(self):
        blog = Blog('Test', 'Test Author')
        app.blogs = {'Test': blog}
        with patch('builtins.print') as mocked_print:
            app.print_blogs()
            mocked_print.assert_called_with('- Test by Test Author (0 posts)')

    @unittest.skip
    def test_menu_print_prompts(self):
        with patch('builtins.input') as mocked_input:
            app.menu()
            mocked_input.assert_called_with(app.MENU_PROMPT)

    def test_ask_create_blogs(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Author')
            app.ask_create_blog()
            self.assertIsNotNone(app.blogs.get('Test'))

    def test_ask_read_blog(self):
        blog = Blog('Test', 'Test Author')
        app.blogs = {'Test': blog}
        with patch('builtins.input', return_value='Test'):
            with patch('app.print_posts') as mocked_print_posts:
                app.ask_read_blog()

                mocked_print_posts.assert_called_with(blog)

    def test_print_posts(self):
        blog = Blog('Test', 'Test Author')
        blog.create_post('Test Post', 'Test content')
        app.blogs = {'Test': blog}
        with patch('app.print_post') as mocked_print_post:
            app.print_posts(blog)

            mocked_print_post.assert_called_with(blog.posts[0])

    def test_print_post(self):
        post = Post('Post Title', 'Post content')
        expected_print = app.POST_TEMPLATE.format('Post Title', 'Post content')
        with patch('builtins.print') as mocked_print:
            app.print_post(post)

            mocked_print.assert_called_with(expected_print)

    def test_ask_create_post(self):
        blog = Blog('Test', 'Test Author')
        app.blogs = {'Test': blog}
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Title', 'Test Content')

            app.ask_create_post()

            self.assertEqual(blog.posts[0].title, 'Test Title')
            self.assertEqual(blog.posts[0].content, 'Test Content')

    def test_menu_calls_create_blog(self):
        with patch('builtins.input') as mocked_input:
            with patch('app.ask_create_blog') as mock_ask_create_blog:
                mocked_input.side_effect = ('c', 'q')

                app.menu()
                mock_ask_create_blog.assert_called()

    def test_menu_calls_create_blog_real(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('c', 'Test Create Blog', 'Test Author', 'q')

            app.menu()
            self.assertIsNotNone(app.blogs['Test Create Blog'])

    def test_menu_calls_print_blogs(self):
        with patch('builtins.input') as mocked_input:
            with patch('app.print_blogs') as mock_print_blogs:
                mocked_input.side_effect = ('l', 'q')

                app.menu()
                mock_print_blogs.assert_called()

    def test_menu_calls_ask_read_blog(self):
        with patch('builtins.input') as mocked_input:
            with patch('app.ask_read_blog') as mock_ask_read_blog:
                mocked_input.side_effect = ('r', 'q')

                app.menu()
                mock_ask_read_blog.assert_called()

    def test_menu_calls_ask_create_post(self):
        with patch('builtins.input') as mocked_input:
            with patch('app.ask_create_post') as mock_ask_create_post:
                mocked_input.side_effect = ('p', 'q')

                app.menu()
                mock_ask_create_post.assert_called()