CREATE DATABASE IF NOT EXISTS faqfusion_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE faqfusion_db;

-- =============================================================
-- ADMINS
-- =============================================================
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,

    role ENUM('super_admin','admin','moderator')
        NOT NULL DEFAULT 'moderator',

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_admin_username (username),
    INDEX idx_admin_email (email)
) ENGINE=InnoDB;


-- =============================================================
-- USERS
-- =============================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    last_login DATETIME NULL,
    
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_user_username (username),
    INDEX idx_user_email (email)
) ENGINE=InnoDB;


-- =============================================================
-- FAQ CATEGORIES
-- =============================================================
CREATE TABLE faq_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


-- =============================================================
-- FAQS
-- =============================================================
CREATE TABLE faqs (
    id INT AUTO_INCREMENT PRIMARY KEY,

    question TEXT NOT NULL,
    answer TEXT NOT NULL,

    category_id INT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    view_count INT NOT NULL DEFAULT 0,

    created_by INT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    deleted_at DATETIME NULL,

    FULLTEXT(question, answer),

    CONSTRAINT fk_faq_category
        FOREIGN KEY (category_id)
        REFERENCES faq_categories(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_faq_created_by
        FOREIGN KEY (created_by)
        REFERENCES admins(id)
        ON DELETE SET NULL
) ENGINE=InnoDB;


-- =============================================================
-- FAQ ALIASES
-- Similar questions for matching/search
-- =============================================================
CREATE TABLE faq_aliases (
    id INT AUTO_INCREMENT PRIMARY KEY,

    faq_id INT NOT NULL,

    alias_question TEXT NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_alias_faq
        FOREIGN KEY (faq_id)
        REFERENCES faqs(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;


-- =============================================================
-- USER QUESTIONS
-- =============================================================
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    question_text TEXT NOT NULL,

    answer_text TEXT NULL,

    status ENUM(
        'pending',
        'answered',
        'rejected'
    ) NOT NULL DEFAULT 'pending',

    similarity_score DECIMAL(4,2) NULL,

    matched_faq_id INT NULL,

    resolved_by_admin INT NULL,

    resolved_at DATETIME NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_question_status (status),

    CONSTRAINT fk_question_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_question_faq
        FOREIGN KEY (matched_faq_id)
        REFERENCES faqs(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_question_admin
        FOREIGN KEY (resolved_by_admin)
        REFERENCES admins(id)
        ON DELETE SET NULL
) ENGINE=InnoDB;


-- =============================================================
-- QUESTION FEEDBACK
-- =============================================================
CREATE TABLE question_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,

    question_id INT NOT NULL,
    user_id INT NOT NULL,

    is_helpful BOOLEAN NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_feedback_question
        FOREIGN KEY (question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_feedback_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    
    UNIQUE KEY uq_feedback (question_id , user_id)
) ENGINE=InnoDB;


-- =============================================================
-- AUDIT LOGS
-- =============================================================
CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,

    admin_id INT NULL,

    action VARCHAR(100) NOT NULL,

    entity_type VARCHAR(50) NOT NULL,

    entity_id INT NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_admin
        FOREIGN KEY (admin_id)
        REFERENCES admins(id)
        ON DELETE SET NULL
) ENGINE=InnoDB;
-- =============================================================
-- FAQ EMBEDDINGS
-- =============================================================
CREATE TABLE faq_embeddings (
    id INT AUTO_INCREMENT PRIMARY KEY,

    faq_id INT NOT NULL,

    embedding JSON NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (faq_id)
    REFERENCES faqs(id)
    ON DELETE CASCADE
);
