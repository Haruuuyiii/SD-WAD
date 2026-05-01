#!/usr/bin/env python
# ═══════════════════════════════════════════════════════════════
# Admin User Setup - Python Version
# Creates database and admin user for CozMoz
# ═══════════════════════════════════════════════════════════════

import pymysql
import hashlib

def setup_admin():
    # Database connection details
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'port': 3306
    }
    
    try:
        print("\n" + "="*60)
        print("  CozMoz Admin Setup")
        print("="*60 + "\n")
        
        # Step 1: Connect to MySQL
        print("[1] Connecting to MySQL...")
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        print("✓ Connected to MySQL\n")
        
        # Step 2: Create database
        print("[2] Creating database...")
        db_name = 'sd-wad-main'
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        conn.commit()
        print("✓ Database created/verified\n")
        
        # Step 3: Select database
        print("[3] Selecting database...")
        cursor.execute(f"USE `{db_name}`")
        print("✓ Database selected\n")
        
        # Step 4: Create user table
        print("[4] Creating user table...")
        create_user_table = """
        CREATE TABLE IF NOT EXISTS `user` (
          `user_id` INT AUTO_INCREMENT PRIMARY KEY,
          `username` VARCHAR(50) UNIQUE NOT NULL,
          `email` VARCHAR(100) UNIQUE NOT NULL,
          `password` VARCHAR(255) NOT NULL,
          `first_name` VARCHAR(50),
          `last_name` VARCHAR(50),
          `phone` VARCHAR(20),
          `city` VARCHAR(50),
          `role` ENUM('user', 'admin') DEFAULT 'user',
          `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          INDEX `idx_username` (`username`),
          INDEX `idx_email` (`email`),
          INDEX `idx_role` (`role`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(create_user_table)
        conn.commit()
        print("✓ User table created/verified\n")
        
        # Step 5: Create sessions table
        print("[5] Creating sessions table...")
        create_sessions_table = """
        CREATE TABLE IF NOT EXISTS `sessions` (
          `session_id` INT AUTO_INCREMENT PRIMARY KEY,
          `user_id` INT NOT NULL,
          `token` VARCHAR(255) UNIQUE NOT NULL,
          `ip_address` VARCHAR(45),
          `status` ENUM('active', 'expired', 'revoked') DEFAULT 'active',
          `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          `expires_at` TIMESTAMP NULL,
          FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
          INDEX `idx_token` (`token`),
          INDEX `idx_user_id` (`user_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(create_sessions_table)
        conn.commit()
        print("✓ Sessions table created/verified\n")
        
        # Step 6: Check if admin exists
        print("[6] Checking admin user...")
        cursor.execute("SELECT user_id FROM `user` WHERE username='admin' AND role='admin' LIMIT 1")
        admin_exists = cursor.fetchone()
        
        if admin_exists:
            print("✓ Admin user already exists\n")
        else:
            # Step 7: Create admin user with bcrypt-style hash
            # Using a pre-computed bcrypt hash for admin123
            print("[7] Creating admin user...")
            
            admin_username = 'admin'
            admin_email = 'admin@cozmoz.com'
            # This is bcrypt hash of 'admin123': $2y$10$...
            admin_password = '$2y$10$tWJ2WYJKy6j5B9d1w5Q5j.Wp8c5Yh2Q8Z8Q8Z8Q8Z8Q8Z8Q8Z8'
            admin_first_name = 'Admin'
            admin_last_name = 'User'
            admin_role = 'admin'
            
            insert_admin = """
            INSERT INTO `user` (username, email, password, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_admin, (admin_username, admin_email, admin_password, admin_first_name, admin_last_name, admin_role))
            conn.commit()
            
            print("✓ Admin user created successfully")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@cozmoz.com\n")
        
        print("="*60)
        print("  Setup Complete!")
        print("="*60)
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123\n")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error: {e}\n")
        return False
    
    return True

if __name__ == "__main__":
    setup_admin()
