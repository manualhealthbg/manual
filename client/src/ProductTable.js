import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProductTable = () => {
  const [products, setProducts] = useState([]);
  const [editing, setEditing] = useState(null);
  const [newProduct, setNewProduct] = useState({ name: '', description: '' });

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/product/products');
        setProducts(response.data);
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };

    fetchProducts();
  }, []);

  const handleChange = (e, field, productId) => {
    const { value } = e.target;
    setProducts(products.map(product =>
      product.id === productId ? { ...product, [field]: value } : product
    ));
  };

  const handleSave = async (productId) => {
    const product = products.find(p => p.id === productId);
    try {
      await axios.put(`http://127.0.0.1:5000/api/product/${productId}`, product);
      setEditing(null);
    } catch (error) {
      console.error('Error updating product:', error);
    }
  };

  const handleNewProductChange = (e) => {
    const { name, value } = e.target;
    setNewProduct(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleCreateProduct = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/api/product', newProduct);
      setNewProduct({ name: '', description: '' }); // Clear the form after submission
      const response = await axios.get('http://127.0.0.1:5000/api/product/products');
      setProducts(response.data); // Fetch the updated list of products
    } catch (error) {
      console.error('Error creating product:', error);
    }
  };

  return (
    <div>
      <h1>Product List</h1>

      {/* New Product Form */}
      <h2>Create New Product</h2>
      <div>
        <input
          type="text"
          name="name"
          placeholder="Product Name"
          value={newProduct.name}
          onChange={handleNewProductChange}
        />
        <input
          type="text"
          name="description"
          placeholder="Product Description"
          value={newProduct.description}
          onChange={handleNewProductChange}
        />
        <button onClick={handleCreateProduct}>Create Product</button>
      </div>

      {/* Product Table */}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map(product => (
            <tr key={product.id}>
              <td>{product.id}</td>
              <td>
                {editing === product.id ? (
                  <input
                    type="text"
                    value={product.name}
                    onChange={(e) => handleChange(e, 'name', product.id)}
                  />
                ) : (
                  product.name
                )}
              </td>
              <td>
                {editing === product.id ? (
                  <input
                    type="text"
                    value={product.description}
                    onChange={(e) => handleChange(e, 'description', product.id)}
                  />
                ) : (
                  product.description
                )}
              </td>
              <td>
                {editing === product.id ? (
                  <select
                    value={product.status}
                    onChange={(e) => handleChange(e, 'status', product.id)}
                  >
                    <option value="draft">Draft</option>
                    <option value="published">Published</option>
                    <option value="disabled">Disabled</option>
                  </select>
                ) : (
                  product.status
                )}
              </td>
              <td>
                {editing === product.id ? (
                  <button onClick={() => handleSave(product.id)}>Save</button>
                ) : (
                  <button onClick={() => setEditing(product.id)}>Edit</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProductTable;
