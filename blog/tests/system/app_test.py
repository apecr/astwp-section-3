from unittest import TestCase
from unittest.mock import patch
import app
from blog import Blog
from post import Post
import unittest


class AppTest(TestCase):
    def setUp(self):
        blog = Blog('Test', 'Test Author')
        app.blogs = {'Test': blog}

    def test_print_blogs(self):
        with patch('builtins.print') as mocked_print:
            app.print_blogs()
            mocked_print.assert_called_with('- Test by Test Author (0 posts)')

    def test_ask_create_blogs(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Author')
            app.ask_create_blog()
            self.assertIsNotNone(app.blogs.get('Test'))

    def test_ask_read_blog(self):
        with patch('builtins.input', return_value='Test'):
            with patch('app.print_posts') as mocked_print_posts:
                app.ask_read_blog()

                mocked_print_posts.assert_called_with(app.blogs['Test'])

    def test_print_posts(self):
        blog = app.blogs['Test']
        blog.create_post('Test Post', 'Test content')
        with patch('app.print_post') as mocked_print_post:
            app.print_posts(app.blogs['Test'])

            mocked_print_post.assert_called_with(app.blogs['Test'].posts[0])

    def test_print_post(self):
        post = Post('Post Title', 'Post content')
        expected_print = app.POST_TEMPLATE.format('Post Title', 'Post content')
        with patch('builtins.print') as mocked_print:
            app.print_post(post)

            mocked_print.assert_called_with(expected_print)

    def test_ask_create_post(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Title', 'Test Content')

            app.ask_create_post()

            self.assertEqual(app.blogs['Test'].posts[0].title, 'Test Title')
            self.assertEqual(app.blogs['Test'].posts[0].content, 'Test Content')

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