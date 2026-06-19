    -- FAQFusion AI - MySQL Database Schema
    -- Run this file to initialize the database

    CREATE DATABASE IF NOT EXISTS faqfusion_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    USE faqfusion_db;

    -- Users Table
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role ENUM('user', 'admin') DEFAULT 'user',
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

    -- FAQ Repository Table
    CREATE TABLE IF NOT EXISTS faq_repository (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question_text TEXT NOT NULL,
        answer_text TEXT NOT NULL,
        category VARCHAR(100) DEFAULT 'General',
        approved_by INT,
        view_count INT DEFAULT 0,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
    );

    -- Questions Table (pending questions from users)
    CREATE TABLE IF NOT EXISTS questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        question_text TEXT NOT NULL,
        status ENUM('pending', 'answered', 'rejected') DEFAULT 'pending',
        matched_faq_id INT DEFAULT NULL,
        similarity_score FLOAT DEFAULT NULL,
        admin_note TEXT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (matched_faq_id) REFERENCES faq_repository(id) ON DELETE SET NULL
    );

    -- Answers Table (admin-written answers for pending questions)
    CREATE TABLE IF NOT EXISTS answers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question_id INT NOT NULL,
        faq_id INT,
        answer_text TEXT NOT NULL,
        created_by INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
        FOREIGN KEY (faq_id) REFERENCES faq_repository(id) ON DELETE SET NULL,
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
    );

    -- Indexes for performance
    CREATE INDEX idx_questions_status ON questions(status);
    CREATE INDEX idx_questions_user ON questions(user_id);
    CREATE INDEX idx_faq_category ON faq_repository(category);
    CREATE INDEX idx_faq_active ON faq_repository(is_active);

    -- Seed: Default Admin User (password: Admin@123)
    INSERT INTO users (name, email, password_hash, role) VALUES
    ('Super Admin', 'admin@faqfusion.com', 'pbkdf2:sha256:600000$placeholder$placeholder', 'admin');

    -- Seed: Sample FAQ Data
    INSERT INTO faq_repository (question_text, answer_text, category, approved_by) VALUES
    ('How do I get my internship certificate?', 'Internship certificates are issued after successful completion of the internship period. Please fill the certificate request form available on the portal and submit it at least 5 working days before your end date. The HR team will process it within 3 working days.', 'Certificates', 1),
    ('What is the attendance requirement for interns?', 'Interns are required to maintain a minimum of 85% attendance throughout the internship period. Any leave must be notified to your supervisor in advance via email. Absences beyond the limit may result in certificate non-issuance.', 'Attendance', 1),
    ('When is the project report submission deadline?', 'The project report must be submitted within 7 days of your internship completion date. Reports should be submitted in PDF format through the online portal. Late submissions may not be accepted without prior approval.', 'Deadlines', 1),
    ('How do I access the company resources and tools?', 'Company resources are available through the internal portal after login. You will receive your credentials via email on your first day. Contact IT support if you face any access issues within 24 hours.', 'Resources', 1),
    ('What is the work from home policy for interns?', 'Interns may work from home up to 2 days per week with prior approval from their supervisor. WFH requests must be submitted by Thursday for the following week. Approval depends on project requirements and team availability.', 'Policy', 1),
    ('How do I get reimbursement for travel expenses?', 'Travel expense claims must be submitted within 30 days of the travel date. Fill the expense reimbursement form, attach all original receipts, and submit to the Finance department. Processing takes 7-10 working days.', 'Finance', 1),
    ('Where can I find the internship schedule and timeline?', 'The internship schedule is available on the intern portal under the Schedule section. It includes key milestones, evaluation dates, and deadlines. You can also request a copy from your assigned mentor.', 'Resources', 1),
    ('What happens if I miss a deadline?', 'If you anticipate missing a deadline, notify your supervisor immediately via email with a valid reason. Extensions may be granted on a case-by-case basis. Repeated missed deadlines may affect your performance evaluation.', 'Deadlines', 1);
