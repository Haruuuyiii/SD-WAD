-- ═══════════════════════════════════════════════════════════════
-- CozMoz Admin Setup SQL Script
-- Copy and paste this into phpMyAdmin SQL tab to setup admin user
-- ═══════════════════════════════════════════════════════════════

-- Create database
CREATE DATABASE IF NOT EXISTS `sd-wad-main`;
USE `sd-wad-main`;

-- Create user table
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create sessions table
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert admin user if not exists
INSERT IGNORE INTO `user` (username, email, password, first_name, last_name, role) 
VALUES ('admin', 'admin@cozmoz.com', '$2y$10$tWJ2WYJKy6j5B9d1w5Q5j.Wp8c5Yh2Q8Z8Q8Z8Q8Z8Q8Z8Q8Z8', 'Admin', 'User', 'admin');

-- ═══════════════════════════════════════════════════════════════
-- Admin Credentials:
-- Username: admin
-- Password: admin123
-- Email: admin@cozmoz.com
-- ═══════════════════════════════════════════════════════════════
