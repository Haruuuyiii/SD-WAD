<?php
// ═══════════════════════════════════════════════════════════════
// Admin User Setup Script
// Creates database and admin user for CozMoz
// ═══════════════════════════════════════════════════════════════

$host = "localhost";
$username = "root";
$password = "";

// Connect to MySQL without database
$conn = new mysqli($host, $username, $password);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "\n═══════════════════════════════════════════════════════════════\n";
echo "  CozMoz Admin Setup\n";
echo "═══════════════════════════════════════════════════════════════\n\n";

// Step 1: Create database
echo "[1] Creating database...\n";
$db_name = "sd-wad-main";

if ($conn->query("CREATE DATABASE IF NOT EXISTS `$db_name`")) {
    echo "✓ Database created/verified\n\n";
} else {
    echo "✗ Error creating database: " . $conn->error . "\n";
    exit(1);
}

// Step 2: Select database
if (!$conn->select_db($db_name)) {
    echo "✗ Error selecting database: " . $conn->error . "\n";
    exit(1);
}

// Step 3: Create user table
echo "[2] Creating user table...\n";

$create_table = "CREATE TABLE IF NOT EXISTS `user` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;";

if ($conn->query($create_table)) {
    echo "✓ User table created/verified\n\n";
} else {
    echo "✗ Error creating user table: " . $conn->error . "\n";
    exit(1);
}

// Step 4: Create sessions table
echo "[3] Creating sessions table...\n";

$create_sessions = "CREATE TABLE IF NOT EXISTS `sessions` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;";

if ($conn->query($create_sessions)) {
    echo "✓ Sessions table created/verified\n\n";
} else {
    echo "✗ Error creating sessions table: " . $conn->error . "\n";
}

// Step 5: Check if admin user exists
echo "[4] Checking admin user...\n";

$check_admin = $conn->query("SELECT user_id FROM `user` WHERE username='admin' AND role='admin' LIMIT 1");

if ($check_admin && $check_admin->num_rows > 0) {
    echo "✓ Admin user already exists\n\n";
} else {
    // Step 6: Create admin user
    echo "[5] Creating admin user...\n";
    
    $admin_password = password_hash('admin123', PASSWORD_BCRYPT);
    
    $stmt = $conn->prepare("INSERT INTO `user` (username, email, password, first_name, last_name, role) 
                           VALUES (?, ?, ?, ?, ?, ?)");
    
    if (!$stmt) {
        echo "✗ Error preparing statement: " . $conn->error . "\n";
        exit(1);
    }
    
    $role = 'admin';
    $stmt->bind_param("ssssss", $username_val, $email_val, $admin_password, $first_name_val, $last_name_val, $role);
    
    $username_val = 'admin';
    $email_val = 'admin@cozmoz.com';
    $first_name_val = 'Admin';
    $last_name_val = 'User';
    
    if ($stmt->execute()) {
        echo "✓ Admin user created successfully\n";
        echo "  Username: admin\n";
        echo "  Password: admin123\n";
        echo "  Email: admin@cozmoz.com\n\n";
    } else {
        echo "✗ Error creating admin user: " . $stmt->error . "\n";
        exit(1);
    }
    
    $stmt->close();
}

echo "═══════════════════════════════════════════════════════════════\n";
echo "  Setup Complete!\n";
echo "═══════════════════════════════════════════════════════════════\n\n";
echo "You can now login with:\n";
echo "  Username: admin\n";
echo "  Password: admin123\n\n";

$conn->close();
?>
