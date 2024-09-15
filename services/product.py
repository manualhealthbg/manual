import mysql.connector
from mysql.connector import Error
from services.db_config import DB_CONFIG


def create_product(name: str, description: str = None):
    """
    Inserts a new product into the products table.

    :param name: Name of the product
    :param description: Description of the product (optional)
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = """
            INSERT INTO products (name, description, status)
            VALUES (%s, %s, 'draft')
        """
        cursor.execute(query, (name, description))

        connection.commit()

        print("Product created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def publish_product(product_id: int):
    """
    Publishes a product by setting its status to 'published' only if the current status is 'draft'.

    :param product_id: The ID of the product to publish
    :raises: Exception if the product is not in 'draft' status
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        select_query = "SELECT status FROM products WHERE id = %s"
        cursor.execute(select_query, (product_id,))
        result = cursor.fetchone()

        if result is None:
            print("Product not found.")
            return

        current_status = result[0]

        if current_status == 'draft':
            update_query = "UPDATE products SET status = 'published' WHERE id = %s"
            cursor.execute(update_query, (product_id,))
            connection.commit()
            print("Product published successfully.")
        else:
            print(f"Cannot publish product. Current status is '{current_status}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def disable_product(product_id: int):
    """
    Disables a product by setting its status to 'disabled' only if the current status is 'published'.

    :param product_id: The ID of the product to disable
    :raises: Exception if the product is not in 'published' status
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        select_query = "SELECT status FROM products WHERE id = %s"
        cursor.execute(select_query, (product_id,))
        result = cursor.fetchone()

        if result is None:
            print("Product not found.")
            return

        current_status = result[0]

        if current_status == 'published':
            update_query = "UPDATE products SET status = 'disabled' WHERE id = %s"
            cursor.execute(update_query, (product_id,))
            connection.commit()
            print("Product disabled successfully.")
        else:
            print(f"Cannot disable product. Current status is '{current_status}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def get_all_products():
    """Fetch all products."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT id, name, description, status FROM products"
        cursor.execute(query)
        rows = cursor.fetchall()

        return rows

    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_product(product_id, name, description, status):
    """Update product details."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = """
        UPDATE products
        SET name = %s, description = %s, status = %s
        WHERE id = %s
        """
        cursor.execute(query, (name, description, status, product_id))
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
