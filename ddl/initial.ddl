CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(1000) NOT NULL,
    status ENUM('draft', 'published', 'disabled') DEFAULT 'draft'
);

CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    text VARCHAR(1000) NOT NULL,
    status ENUM('draft', 'published', 'disabled') DEFAULT 'draft',
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    status ENUM('draft', 'published', 'disabled') DEFAULT 'draft'
);

CREATE TABLE question_transitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    answer_id INT NOT NULL,
    next_question_id INT NULL,
    product_id int NULL,
    FOREIGN KEY (answer_id) REFERENCES answers(id) ON DELETE CASCADE,
    FOREIGN KEY (next_question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE product_restrictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    answer_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (answer_id) REFERENCES answers(id) ON DELETE CASCADE
);


