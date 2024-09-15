import unittest
from unittest.mock import patch, MagicMock
from services.product import create_product, publish_product, disable_product, get_all_products, update_product


class TestProductService(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_create_product_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        create_product("Test Product", "This is a test product")

        mock_cursor.execute.assert_called_once_with("\n            INSERT INTO products (name, description, status)\n            VALUES (%s, %s, 'draft')\n        ", ('Test Product', 'This is a test product'))
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_publish_product_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ('draft',)

        publish_product(1)

        mock_cursor.execute.assert_any_call(
            "SELECT status FROM products WHERE id = %s", (1,)
        )
        mock_cursor.execute.assert_any_call(
            "UPDATE products SET status = 'published' WHERE id = %s", (1,)
        )
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_publish_product_invalid_status(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ('published',)

        publish_product(1)

        mock_cursor.execute.assert_called_once_with(
            "SELECT status FROM products WHERE id = %s", (1,)
        )
        mock_conn.commit.assert_not_called()

    @patch('mysql.connector.connect')
    def test_disable_product_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ('published',)

        disable_product(1)

        mock_cursor.execute.assert_any_call(
            "SELECT status FROM products WHERE id = %s", (1,)
        )
        mock_cursor.execute.assert_any_call(
            "UPDATE products SET status = 'disabled' WHERE id = %s", (1,)
        )
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_get_all_products(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "Product 1", "description": "Desc 1", "status": "draft"},
            {"id": 2, "name": "Product 2", "description": "Desc 2", "status": "published"}
        ]

        products = get_all_products()

        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name, description, status FROM products"
        )
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]["name"], "Product 1")
        self.assertEqual(products[1]["status"], "published")

    @patch('mysql.connector.connect')
    def test_update_product(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        update_product(1, "Updated Product", "Updated Desc", "draft")

        mock_cursor.execute.assert_called_once_with('\n        UPDATE products\n        SET name = %s, description = %s, status = %s\n        WHERE id = %s\n        ', ('Updated Product', 'Updated Desc', 'draft', 1))

        mock_conn.commit.assert_called_once()
