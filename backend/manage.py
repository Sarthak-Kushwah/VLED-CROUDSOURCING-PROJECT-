"""
CLI management commands for FAQFusion AI.

Provides administrative commands for tasks that should not be
exposed through REST APIs (e.g., creating the first admin user).

Usage:
    $ python -m backend.manage create-admin
    $ python -m backend.manage seed-faqs
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.app import create_app
from database.db import db
from backend.models.admin import Admin
from backend.models.faq import FAQ


def create_admin():
    """Interactively create a new admin user."""
    app = create_app()
    with app.app_context():
        print('\n=== Create Admin User ===\n')
        username = input('Username: ').strip()
        email = input('Email: ').strip().lower()
        password = input('Password: ').strip()
        role = input('Role (super_admin / moderator) [moderator]: ').strip() or 'moderator'

        if Admin.query.filter(
            (Admin.username == username) | (Admin.email == email)
        ).first():
            print('Error: An admin with this username or email already exists.')
            sys.exit(1)

        admin = Admin(username=username, email=email, role=role)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f'\nAdmin "{username}" created successfully (id={admin.id}).\n')


def seed_faqs():
    """Seed the FAQ repository with sample entries for development."""
    app = create_app()
    with app.app_context():
        sample_faqs = [
            {
                'question': 'How do I reset my password?',
                'answer': (
                    'Click the "Forgot Password" link on the login page, '
                    'enter your email address, and follow the instructions '
                    'sent to your inbox.'
                ),
                'category': 'Account',
            },
            {
                'question': 'What payment methods do you accept?',
                'answer': (
                    'We accept Visa, MasterCard, American Express, PayPal, '
                    'and bank transfers for annual plans.'
                ),
                'category': 'Billing',
            },
            {
                'question': 'How can I contact customer support?',
                'answer': (
                    'You can reach our support team via email at '
                    'support@faqfusion.ai, through the in-app chat widget, '
                    'or by calling +1-800-FAQ-HELP during business hours.'
                ),
                'category': 'Support',
            },
            {
                'question': 'How do I delete my account?',
                'answer': (
                    'Navigate to Settings → Account → Delete Account. '
                    'Please note that this action is irreversible and all '
                    'your data will be permanently removed after 30 days.'
                ),
                'category': 'Account',
            },
            {
                'question': 'Is my data secure?',
                'answer': (
                    'Yes. We use industry-standard AES-256 encryption for '
                    'data at rest and TLS 1.3 for data in transit. Our '
                    'infrastructure is SOC 2 Type II certified.'
                ),
                'category': 'Security',
            },
        ]

        added = 0
        for faq_data in sample_faqs:
            existing = FAQ.query.filter_by(question=faq_data['question']).first()
            if not existing:
                faq = FAQ(**faq_data)
                db.session.add(faq)
                added += 1

        db.session.commit()
        print(f'\nSeeded {added} FAQs ({len(sample_faqs) - added} already existed).\n')


if __name__ == '__main__':
    commands = {
        'create-admin': create_admin,
        'seed-faqs': seed_faqs,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(f'Usage: python -m backend.manage <command>')
        print(f'Available commands: {", ".join(commands.keys())}')
        sys.exit(1)

    commands[sys.argv[1]]()
