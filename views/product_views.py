from flask import Blueprint, request, jsonify
from services.product import (
    create_product,
    publish_product,
    disable_product,
    get_all_products,
    update_product
)
from services.quiz import (
    create_restriction,
    remove_restriction_by_id,
    get_product_restrictions
)

product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/product', methods=['POST'])
def create_product_endpoint():
    """
    curl -X POST http://127.0.0.1:5000/api/product -H "Content-Type: application/json" -d '{"name": "New Product", "description": "Description of the product"}'

    Endpoint to create a new product.
    Expects a JSON payload: { "name": "product name", "description": "product description" }
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Product name is required"}), 400

    create_product(name, description)
    return jsonify({"message": "Product created successfully"}), 201


@product_blueprint.route('/product/<int:product_id>/publish', methods=['POST'])
def publish_product_endpoint(product_id):
    """
    curl -X POST http://127.0.0.1:5000/api/product/1/publish

    Endpoint to publish a product.
    """
    try:
        publish_product(product_id)
        return jsonify({"message": "Product published successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_blueprint.route('/product/<int:product_id>/disable', methods=['POST'])
def disable_product_endpoint(product_id):
    """
    curl -X POST http://127.0.0.1:5000/api/product/1/disable

    Endpoint to disable a product.
    """
    try:
        disable_product(product_id)
        return jsonify({"message": "Product disabled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_blueprint.route('/product/products', methods=['GET'])
def get_all_products_endpoint():
    """
    curl -X GET http://127.0.0.1:5000/api/product/products

    Endpoint to get all products.
    """
    try:
        result = get_all_products()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_blueprint.route('/product/<int:product_id>', methods=['PUT'])
def update_product_endpoint(product_id):
    """
    curl -X PUT http://127.0.0.1:5000/api/product/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "Updated Product Name", "description": "Updated Product Description", "status": "published"}'

    Endpoint to update a product.
    Expects JSON payload: { "name": "product name", "description": "product description", "status": "draft" }
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    status = data.get('status')

    if not name or not status:
        return jsonify({"error": "Name and status are required"}), 400

    try:
        update_product(product_id, name, description, status)
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- New Product Restriction Endpoints ---

@product_blueprint.route('/restriction', methods=['POST'])
def add_product_restriction():
    """
    Adds a new product restriction (disallow) based on answer and product IDs.
    Expects a JSON body with "answer_id" and "product_id".
    """
    data = request.get_json()

    answer_id = data.get('answer_id')
    product_id = data.get('product_id')

    if not answer_id or not product_id:
        return jsonify({"error": "answer_id and product_id are required"}), 400

    try:
        create_restriction(answer_id, product_id)
        return jsonify({"message": "Product restriction created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_blueprint.route('/restriction/<int:restriction_id>', methods=['DELETE'])
def delete_product_restriction(restriction_id):
    """
    Deletes a product restriction by its ID.
    """
    try:
        remove_restriction_by_id(restriction_id)
        return jsonify({"message": f"Product restriction with ID {restriction_id} removed successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_blueprint.route('/product_restrictions/<int:answer_id>', methods=['GET'])
def get_restrictions(answer_id):
    """
    Fetches all product restrictions for a given answer_id.
    """
    try:
        restrictions = get_product_restrictions(answer_id)
        return jsonify(restrictions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
