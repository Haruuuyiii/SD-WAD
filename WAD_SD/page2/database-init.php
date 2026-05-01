<?php
// ═══════════════════════════════════════════════════════════════
// SD-WAD MAIN DATABASE INITIALIZATION
// PHP-Based Database Setup
// Purpose: Initialize all tables for the CozMoz event system
// ═══════════════════════════════════════════════════════════════

// Start output buffering to handle any warnings
ob_start();

// Include database connection
include 'connect.php';

// Set error reporting
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Color codes for output
$success = "\033[92m"; // Green
$error = "\033[91m";   // Red
$info = "\033[94m";    // Blue
$reset = "\033[0m";    // Reset

// ───────────────────────────────────────────────────────────────
// DISPLAY HEADER
// ───────────────────────────────────────────────────────────────

echo "\n";
echo "═══════════════════════════════════════════════════════════════\n";
echo "  CozMoz Event Management System - Database Initialization\n";
echo "═══════════════════════════════════════════════════════════════\n\n";

// ───────────────────────────────────────────────────────────────
// STEP 1: CREATE USERS TABLE
// ───────────────────────────────────────────────────────────────

echo "[1] Creating USERS table...\n";

$sql_users = "
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
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
";

if ($conn->multi_query($sql_users)) {
    echo "{$success}✓ USERS table created successfully{$reset}\n";
    // Clear results
    while ($conn->next_result()) {
        if ($result = $conn->store_result()) {
            $result->free();
        }
    }
} else {
    echo "{$error}✗ Error creating USERS table: " . $conn->error . "{$reset}\n";
}

// ───────────────────────────────────────────────────────────────
// STEP 2: CREATE EVENTS TABLE
// ───────────────────────────────────────────────────────────────

echo "[2] Creating EVENTS table...\n";

$sql_events = "
DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `event_id` INT AUTO_INCREMENT PRIMARY KEY,
  `event_name` VARCHAR(100) NOT NULL,
  `event_description` TEXT,
  `event_start` DATETIME NOT NULL,
  `event_end` DATETIME NOT NULL,
  `location` VARCHAR(100),
  `max_capacity` INT DEFAULT 100,
  `ticket_price` DECIMAL(10, 2) DEFAULT 0.00,
  `event_color` VARCHAR(7) DEFAULT '#6366f1',
  `status` ENUM('draft', 'published', 'ongoing', 'completed', 'cancelled') DEFAULT 'draft',
  `created_by` INT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`created_by`) REFERENCES `user`(`user_id`),
  INDEX `idx_event_start` (`event_start`),
  INDEX `idx_event_end` (`event_end`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
";

if ($conn->query($sql_events)) {
    echo "{$success}✓ EVENTS table created successfully{$reset}\n";
} else {
    echo "{$error}✗ Error creating EVENTS table: " . $conn->error . "{$reset}\n";
}

// ───────────────────────────────────────────────────────────────
// STEP 3: CREATE REGISTRATIONS TABLE
// ───────────────────────────────────────────────────────────────

echo "[3] Creating REGISTRATIONS table...\n";

$sql_registrations = "
DROP TABLE IF EXISTS `registrations`;
CREATE TABLE `registrations` (
  `registration_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  `ticket_id` VARCHAR(50),
  `status` ENUM('pending', 'registered', 'checked_in', 'cancelled') DEFAULT 'registered',
  `checked_in` BOOLEAN DEFAULT FALSE,
  `check_in_time` DATETIME,
  `amount_paid` DECIMAL(10, 2) DEFAULT 0.00,
  `payment_status` ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'completed',
  `last_login` DATETIME,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`event_id`) REFERENCES `events`(`event_id`) ON DELETE CASCADE,
  UNIQUE KEY `unique_user_event` (`user_id`, `event_id`),
  INDEX `idx_status` (`status`),
  INDEX `idx_checked_in` (`checked_in`),
  INDEX `idx_payment_status` (`payment_status`),
  INDEX `idx_event_id` (`event_id`),
  INDEX `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
";

if ($conn->query($sql_registrations)) {
    echo "{$success}✓ REGISTRATIONS table created successfully{$reset}\n";
} else {
    echo "{$error}✗ Error creating REGISTRATIONS table: " . $conn->error . "{$reset}\n";
}

// ───────────────────────────────────────────────────────────────
// STEP 4: CREATE TICKETS TABLE
// ───────────────────────────────────────────────────────────────

echo "[4] Creating TICKETS table...\n";

$sql_tickets = "
DROP TABLE IF EXISTS `tickets`;
CREATE TABLE `tickets` (
  `ticket_id` INT AUTO_INCREMENT PRIMARY KEY,
  `ticket_code` VARCHAR(50) UNIQUE NOT NULL,
  `registration_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `status` ENUM('available', 'used', 'cancelled') DEFAULT 'available',
  `purchase_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `used_date` DATETIME,
  `price` DECIMAL(10, 2),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`registration_id`) REFERENCES `registrations`(`registration_id`) ON DELETE CASCADE,
  FOREIGN KEY (`event_id`) REFERENCES `events`(`event_id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
  INDEX `idx_ticket_code` (`ticket_code`),
  INDEX `idx_status` (`status`),
  INDEX `idx_event_id` (`event_id`),
  INDEX `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
";

if ($conn->query($sql_tickets)) {
    echo "{$success}✓ TICKETS table created successfully{$reset}\n";
} else {
    echo "{$error}✗ Error creating TICKETS table: " . $conn->error . "{$reset}\n";
}

// ───────────────────────────────────────────────────────────────
// STEP 5: CREATE SESSIONS TABLE
// ───────────────────────────────────────────────────────────────

echo "[5] Creating SESSIONS table...\n";

$sql_sessions = "
DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
  `session_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `token` VARCHAR(255) UNIQUE NOT NULL,
  `login_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `last_activity` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ip_address` VARCHAR(45),
  `status` ENUM('active', 'expired', 'logged_out') DEFAULT 'active',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
  INDEX `idx_token` (`token`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
";

if ($conn->query($sql_sessions)) {
    echo "{$success}✓ SESSIONS table created successfully{$reset}\n";
} else {
    echo "{$error}✗ Error creating SESSIONS table: " . $conn->error . "{$reset}\n";
}

// ───────────────────────────────────────────────────────────────
// STEP 6: INSERT DEFAULT ADMIN USER
// ───────────────────────────────────────────────────────────────

echo "[6] Inserting default admin user...\n";

// Password: admin123 (hashed with bcrypt)
$admin_password = password_hash('admin123', PASSWORD_BCRYPT);

$sql_admin = "INSERT INTO `user` (username, email, password, first_name, last_name, role) 
              VALUES ('admin', 'admin@cozmoz.com', ?, 'Admin', 'User', 'admin')";

$stmt = $conn->prepare($sql_admin);
if ($stmt) {
    $stmt->bind_param("s", $admin_password);
    if ($stmt->execute()) {
        echo "{$success}✓ Admin user created successfully{$reset}\n";
        echo "   Username: admin\n";
        echo "   Password: admin123\n";
    } else {
        echo "{$error}✗ Error inserting admin user: " . $stmt->error . "{$reset}\n";
    }
    $stmt->close();
} else {
    echo "{$error}✗ Error preparing admin statement: " . $conn->error . "{$reset}\n";
}

// ───────────────────────────────────────────────────────────────
// STEP 7: INSERT SAMPLE EVENTS
// ───────────────────────────────────────────────────────────────

echo "[7] Inserting sample events...\n";

$events = array(
    array(
        'name' => 'Tech Conference 2025',
        'description' => 'Annual technology conference featuring industry leaders',
        'start' => date('Y-m-d H:i:s', strtotime('+30 days')),
        'end' => date('Y-m-d H:i:s', strtotime('+31 days')),
        'location' => 'Manila Convention Center',
        'capacity' => 500,
        'price' => 1500.00,
        'color' => '#3b82f6'
    ),
    array(
        'name' => 'Web Development Workshop',
        'description' => 'Learn modern web development practices and frameworks',
        'start' => date('Y-m-d H:i:s', strtotime('+14 days')),
        'end' => date('Y-m-d H:i:s', strtotime('+14 days 8 hours')),
        'location' => 'Tech Hub Manila',
        'capacity' => 50,
        'price' => 500.00,
        'color' => '#f97316'
    ),
    array(
        'name' => 'AI & Machine Learning Summit',
        'description' => 'Explore the future of AI and machine learning applications',
        'start' => date('Y-m-d H:i:s', strtotime('+60 days')),
        'end' => date('Y-m-d H:i:s', strtotime('+61 days')),
        'location' => 'Makati CBD',
        'capacity' => 300,
        'price' => 2000.00,
        'color' => '#06b6d4'
    )
);

$sql_events_insert = "INSERT INTO `events` (event_name, event_description, event_start, event_end, location, max_capacity, ticket_price, event_color, status, created_by) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'published', 1)";

$stmt = $conn->prepare($sql_events_insert);
if ($stmt) {
    foreach ($events as $event) {
        $stmt->bind_param("sssssiis", 
            $event['name'],
            $event['description'],
            $event['start'],
            $event['end'],
            $event['location'],
            $event['capacity'],
            $event['price'],
            $event['color']
        );
        
        if ($stmt->execute()) {
            echo "{$success}✓ Event created: " . $event['name'] . "{$reset}\n";
        } else {
            echo "{$error}✗ Error creating event: " . $stmt->error . "{$reset}\n";
        }
    }
    $stmt->close();
} else {
    echo "{$error}✗ Error preparing events statement: " . $conn->error . "{$reset}\n";
}

// ───────────────────────────────────────────────────────────────
// COMPLETION MESSAGE
// ───────────────────────────────────────────────────────────────

echo "\n";
echo "═══════════════════════════════════════════════════════════════\n";
echo "{$success}  DATABASE INITIALIZATION COMPLETE!{$reset}\n";
echo "═══════════════════════════════════════════════════════════════\n";
echo "\n";
echo "Created Tables:\n";
echo "  • user (with admin account)\n";
echo "  • events (with 3 sample events)\n";
echo "  • registrations\n";
echo "  • tickets\n";
echo "  • sessions\n";
echo "\n";
echo "Default Admin Credentials:\n";
echo "  • Username: admin\n";
echo "  • Password: admin123\n";
echo "\n";
echo "Database: " . $_SERVER['DB'] . "\n";
echo "Host: " . $_SERVER['HOST'] . "\n";
echo "\n";

// Close connection
$conn->close();

echo "{$info}✓ Database connection closed{$reset}\n";
echo "\n";

?>
