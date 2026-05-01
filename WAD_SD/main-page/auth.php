<?php
// ═══════════════════════════════════════════════════════════════
// CozMoz Authentication Handler - PHP
// Handles login, signup, and user session management
// ═══════════════════════════════════════════════════════════════

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Include database connection
include_once 'page2/connect.php';

// Start session
session_start();

// Get request data
$action = $_GET['action'] ?? $_POST['action'] ?? '';
$input = json_decode(file_get_contents('php://input'), true) ?? $_POST;

// ═══════════════════════════════════════════════════════════════
// ROUTE HANDLER
// ═══════════════════════════════════════════════════════════════

switch ($action) {
    case 'login':
        handle_login($input);
        break;
    case 'signup':
        handle_signup($input);
        break;
    case 'logout':
        handle_logout();
        break;
    case 'check-session':
        check_session();
        break;
    case 'get-user':
        get_user_info();
        break;
    default:
        http_response_code(400);
        echo json_encode(['error' => 'Invalid action']);
}

// ═══════════════════════════════════════════════════════════════
// LOGIN HANDLER
// ═══════════════════════════════════════════════════════════════

function handle_login($data) {
    global $conn;
    
    if (!isset($data['username']) || !isset($data['password'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Username and password required']);
        return;
    }
    
    $username = trim($data['username']);
    $password = $data['password'];
    
    // Query database
    $stmt = $conn->prepare("SELECT user_id, username, email, first_name, last_name, password, role FROM `user` WHERE username = ?");
    
    if (!$stmt) {
        http_response_code(500);
        echo json_encode(['error' => 'Database error: ' . $conn->error]);
        return;
    }
    
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        
        // Verify password
        if (password_verify($password, $user['password'])) {
            // Create session
            $_SESSION['user_id'] = $user['user_id'];
            $_SESSION['username'] = $user['username'];
            $_SESSION['email'] = $user['email'];
            $_SESSION['first_name'] = $user['first_name'];
            $_SESSION['last_name'] = $user['last_name'];
            $_SESSION['role'] = $user['role'];
            $_SESSION['logged_in'] = true;
            $_SESSION['login_time'] = time();
            
            // Generate token
            $token = bin2hex(random_bytes(32));
            $_SESSION['token'] = $token;
            
            http_response_code(200);
            echo json_encode([
                'success' => true,
                'message' => 'Login successful',
                'user_id' => $user['user_id'],
                'username' => $user['username'],
                'first_name' => $user['first_name'],
                'last_name' => $user['last_name'],
                'email' => $user['email'],
                'role' => $user['role'],
                'token' => $token
            ]);
            
            // Update last login in database
            $update_stmt = $conn->prepare("UPDATE `user` SET last_login = NOW() WHERE user_id = ?");
            $update_stmt->bind_param("i", $user['user_id']);
            $update_stmt->execute();
            $update_stmt->close();
            
            $stmt->close();
            return;
        }
    }
    
    http_response_code(401);
    echo json_encode(['error' => 'Invalid username or password']);
    $stmt->close();
}

// ═══════════════════════════════════════════════════════════════
// SIGNUP HANDLER
// ═══════════════════════════════════════════════════════════════

function handle_signup($data) {
    global $conn;
    
    // Validate input
    $required = ['username', 'email', 'password', 'first_name', 'last_name'];
    foreach ($required as $field) {
        if (!isset($data[$field]) || empty($data[$field])) {
            http_response_code(400);
            echo json_encode(['error' => ucfirst($field) . ' is required']);
            return;
        }
    }
    
    $username = trim($data['username']);
    $email = trim($data['email']);
    $password = $data['password'];
    $first_name = trim($data['first_name']);
    $last_name = trim($data['last_name']);
    
    // Check if user exists
    $check_stmt = $conn->prepare("SELECT user_id FROM `user` WHERE username = ? OR email = ? LIMIT 1");
    $check_stmt->bind_param("ss", $username, $email);
    $check_stmt->execute();
    $check_result = $check_stmt->get_result();
    
    if ($check_result->num_rows > 0) {
        http_response_code(409);
        echo json_encode(['error' => 'Username or email already exists']);
        $check_stmt->close();
        return;
    }
    $check_stmt->close();
    
    // Hash password
    $hashed_password = password_hash($password, PASSWORD_BCRYPT);
    
    // Insert user
    $stmt = $conn->prepare("INSERT INTO `user` (username, email, password, first_name, last_name, role) VALUES (?, ?, ?, ?, ?, 'user')");
    
    if (!$stmt) {
        http_response_code(500);
        echo json_encode(['error' => 'Database error: ' . $conn->error]);
        return;
    }
    
    $stmt->bind_param("sssss", $username, $email, $hashed_password, $first_name, $last_name);
    
    if ($stmt->execute()) {
        $user_id = $stmt->insert_id;
        
        // Create session
        $_SESSION['user_id'] = $user_id;
        $_SESSION['username'] = $username;
        $_SESSION['email'] = $email;
        $_SESSION['first_name'] = $first_name;
        $_SESSION['last_name'] = $last_name;
        $_SESSION['role'] = 'user';
        $_SESSION['logged_in'] = true;
        $_SESSION['login_time'] = time();
        
        $token = bin2hex(random_bytes(32));
        $_SESSION['token'] = $token;
        
        http_response_code(201);
        echo json_encode([
            'success' => true,
            'message' => 'Account created successfully',
            'user_id' => $user_id,
            'username' => $username,
            'first_name' => $first_name,
            'last_name' => $last_name,
            'email' => $email,
            'token' => $token
        ]);
    } else {
        http_response_code(500);
        echo json_encode(['error' => 'Failed to create account: ' . $stmt->error]);
    }
    
    $stmt->close();
}

// ═══════════════════════════════════════════════════════════════
// LOGOUT HANDLER
// ═══════════════════════════════════════════════════════════════

function handle_logout() {
    session_destroy();
    http_response_code(200);
    echo json_encode(['success' => true, 'message' => 'Logged out successfully']);
}

// ═══════════════════════════════════════════════════════════════
// CHECK SESSION
// ═══════════════════════════════════════════════════════════════

function check_session() {
    if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true) {
        http_response_code(200);
        echo json_encode([
            'logged_in' => true,
            'user_id' => $_SESSION['user_id'] ?? null,
            'username' => $_SESSION['username'] ?? null,
            'first_name' => $_SESSION['first_name'] ?? null,
            'last_name' => $_SESSION['last_name'] ?? null,
            'email' => $_SESSION['email'] ?? null,
            'role' => $_SESSION['role'] ?? 'user'
        ]);
    } else {
        http_response_code(200);
        echo json_encode(['logged_in' => false]);
    }
}

// ═══════════════════════════════════════════════════════════════
// GET USER INFO
// ═══════════════════════════════════════════════════════════════

function get_user_info() {
    if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true) {
        http_response_code(200);
        echo json_encode([
            'user_id' => $_SESSION['user_id'],
            'username' => $_SESSION['username'],
            'first_name' => $_SESSION['first_name'],
            'last_name' => $_SESSION['last_name'],
            'email' => $_SESSION['email'],
            'role' => $_SESSION['role']
        ]);
    } else {
        http_response_code(401);
        echo json_encode(['error' => 'Not logged in']);
    }
}

?>
