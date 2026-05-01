<?php
// ═══════════════════════════════════════════════════════════════
// CozMoz Admin Dashboard API - PHP Version
// Provides JSON API endpoints for admin dashboard
// ═══════════════════════════════════════════════════════════════

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Include database connection
include 'connect.php';

// Get request method and path
$method = $_SERVER['REQUEST_METHOD'];
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$path = str_replace('/api/', '', $path);

// ═══════════════════════════════════════════════════════════════
// ROUTE HANDLER
// ═══════════════════════════════════════════════════════════════

// Parse input
$input = json_decode(file_get_contents('php://input'), true);

// Route requests
if ($path === 'health' && $method === 'GET') {
    health_check();
} elseif ($path === 'admin/login' && $method === 'POST') {
    admin_login($input);
} elseif ($path === 'register' && $method === 'POST') {
    register_user($input);
} elseif ($path === 'login' && $method === 'POST') {
    user_login($input);
} elseif ($path === 'dashboard/stats' && $method === 'GET') {
    get_dashboard_stats();
} elseif ($path === 'dashboard/registrations-by-event' && $method === 'GET') {
    get_registrations_by_event();
} elseif ($path === 'dashboard/user-distribution' && $method === 'GET') {
    get_user_distribution();
} elseif ($path === 'dashboard/recent-registrations' && $method === 'GET') {
    get_recent_registrations();
} elseif ($path === 'dashboard/events' && $method === 'GET') {
    get_all_events();
} elseif ($path === 'dashboard/registrations' && $method === 'GET') {
    get_all_registrations();
} elseif ($path === 'dashboard/attendance' && $method === 'GET') {
    get_attendance();
} elseif ($path === 'buy-ticket' && $method === 'POST') {
    buy_ticket($input);
} elseif ($path === 'register-event' && $method === 'POST') {
    register_for_event($input);
} elseif ($path === 'check-in' && $method === 'POST') {
    check_in_user($input);
} elseif ($path === 'events' && $method === 'GET') {
    get_available_events();
} else {
    http_response_code(404);
    echo json_encode(['error' => 'Endpoint not found']);
}

// ═══════════════════════════════════════════════════════════════
// HEALTH CHECK
// ═══════════════════════════════════════════════════════════════

function health_check() {
    global $conn;
    
    if ($conn->ping()) {
        http_response_code(200);
        echo json_encode([
            'service' => 'admin',
            'status' => 'ok',
            'database' => 'connected'
        ]);
    } else {
        http_response_code(500);
        echo json_encode([
            'service' => 'admin',
            'status' => 'error',
            'database' => 'disconnected'
        ]);
    }
}

// ═══════════════════════════════════════════════════════════════
// AUTHENTICATION ENDPOINTS
// ═══════════════════════════════════════════════════════════════

function admin_login($data) {
    global $conn;
    
    if (!isset($data['username']) || !isset($data['password'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Username and password required']);
        return;
    }
    
    $username = $conn->real_escape_string($data['username']);
    $password = $data['password'];
    
    $result = $conn->query("SELECT user_id, username, first_name, password, role FROM `user` WHERE username = '$username' AND role = 'admin' LIMIT 1");
    
    if ($result && $result->num_rows > 0) {
        $user = $result->fetch_assoc();
        
        if (password_verify($password, $user['password'])) {
            $token = bin2hex(random_bytes(32));
            
            $stmt = $conn->prepare("INSERT INTO sessions (user_id, token, ip_address, status) VALUES (?, ?, ?, 'active')");
            $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
            $stmt->bind_param("iss", $user['user_id'], $token, $ip);
            $stmt->execute();
            $stmt->close();
            
            http_response_code(200);
            echo json_encode([
                'message' => 'Welcome ' . $user['first_name'] . '!',
                'token' => $token,
                'username' => $user['username'],
                'user_id' => $user['user_id'],
                'role' => 'admin'
            ]);
            return;
        }
    }
    
    http_response_code(401);
    echo json_encode(['error' => 'Invalid credentials']);
}

function user_login($data) {
    global $conn;
    
    if (!isset($data['username']) || !isset($data['password'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Username and password required']);
        return;
    }
    
    $username = $conn->real_escape_string($data['username']);
    $password = $data['password'];
    
    $result = $conn->query("SELECT user_id, username, first_name, last_name, email, password, role FROM `user` WHERE username = '$username' AND role = 'user' LIMIT 1");
    
    if ($result && $result->num_rows > 0) {
        $user = $result->fetch_assoc();
        
        if (password_verify($password, $user['password'])) {
            $token = bin2hex(random_bytes(32));
            
            $stmt = $conn->prepare("INSERT INTO sessions (user_id, token, ip_address, status) VALUES (?, ?, ?, 'active')");
            $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
            $stmt->bind_param("iss", $user['user_id'], $token, $ip);
            $stmt->execute();
            $stmt->close();
            
            http_response_code(200);
            echo json_encode([
                'message' => 'Welcome ' . $user['first_name'] . '!',
                'token' => $token,
                'user_id' => $user['user_id'],
                'username' => $user['username'],
                'first_name' => $user['first_name'],
                'last_name' => $user['last_name'],
                'email' => $user['email']
            ]);
            return;
        }
    }
    
    http_response_code(401);
    echo json_encode(['error' => 'Invalid credentials']);
}

function register_user($data) {
    global $conn;
    
    $required = ['username', 'email', 'password', 'first_name', 'last_name'];
    foreach ($required as $field) {
        if (!isset($data[$field]) || empty($data[$field])) {
            http_response_code(400);
            echo json_encode(['error' => 'All fields are required']);
            return;
        }
    }
    
    $username = $conn->real_escape_string(trim($data['username']));
    $email = $conn->real_escape_string(trim($data['email']));
    $password = password_hash($data['password'], PASSWORD_BCRYPT);
    $first_name = $conn->real_escape_string(trim($data['first_name']));
    $last_name = $conn->real_escape_string(trim($data['last_name']));
    
    // Check if user exists
    $check = $conn->query("SELECT user_id FROM `user` WHERE username = '$username' OR email = '$email' LIMIT 1");
    if ($check && $check->num_rows > 0) {
        http_response_code(409);
        echo json_encode(['error' => 'Username or email already exists']);
        return;
    }
    
    // Insert user
    $stmt = $conn->prepare("INSERT INTO `user` (username, email, password, first_name, last_name, role) VALUES (?, ?, ?, ?, ?, 'user')");
    $stmt->bind_param("sssss", $username, $email, $password, $first_name, $last_name);
    
    if ($stmt->execute()) {
        $user_id = $stmt->insert_id;
        http_response_code(201);
        echo json_encode([
            'message' => 'Account created successfully! Welcome ' . $first_name . '!',
            'user_id' => $user_id,
            'username' => $username
        ]);
    } else {
        http_response_code(500);
        echo json_encode(['error' => $stmt->error]);
    }
    $stmt->close();
}

// ═══════════════════════════════════════════════════════════════
// DASHBOARD ENDPOINTS
// ═══════════════════════════════════════════════════════════════

function get_dashboard_stats() {
    global $conn;
    
    $stats = [];
    
    // Total Events
    $result = $conn->query("SELECT COUNT(*) as count FROM events");
    $stats['totalEvents'] = $result->fetch_assoc()['count'] ?? 0;
    
    // Total Registrations
    $result = $conn->query("SELECT COUNT(*) as count FROM registrations");
    $stats['totalRegistrations'] = $result->fetch_assoc()['count'] ?? 0;
    
    // Active Events
    $result = $conn->query("SELECT COUNT(*) as count FROM events WHERE event_end > NOW()");
    $stats['activeEvents'] = $result->fetch_assoc()['count'] ?? 0;
    
    // Tickets Bought
    $result = $conn->query("SELECT COUNT(*) as count FROM registrations WHERE checked_in = 1");
    $stats['ticketsBought'] = $result->fetch_assoc()['count'] ?? 0;
    
    // Logged In Users
    $result = $conn->query("SELECT COUNT(*) as count FROM sessions WHERE status = 'active' AND last_activity > DATE_SUB(NOW(), INTERVAL 1 HOUR)");
    $stats['loggedInUsers'] = $result->fetch_assoc()['count'] ?? 0;
    
    // Total Users
    $result = $conn->query("SELECT COUNT(*) as count FROM `user` WHERE role = 'user'");
    $stats['totalUsers'] = $result->fetch_assoc()['count'] ?? 0;
    
    http_response_code(200);
    echo json_encode($stats);
}

function get_registrations_by_event() {
    global $conn;
    
    $query = "
        SELECT 
            e.event_id,
            e.event_name,
            COUNT(r.registration_id) as registrations,
            COALESCE(e.event_color, '#6366f1') as color
        FROM events e
        LEFT JOIN registrations r ON e.event_id = r.event_id
        GROUP BY e.event_id, e.event_name, e.event_color
        ORDER BY registrations DESC
        LIMIT 5
    ";
    
    $result = $conn->query($query);
    $events = [];
    $colors = ['#3b82f6', '#f97316', '#06b6d4', '#8b5cf6', '#ec4899'];
    $idx = 0;
    
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $events[] = [
                'name' => $row['event_name'],
                'registrations' => (int)$row['registrations'],
                'color' => $row['color'] ?: $colors[$idx % count($colors)]
            ];
            $idx++;
        }
    }
    
    http_response_code(200);
    echo json_encode(['eventRegistrations' => $events]);
}

function get_user_distribution() {
    global $conn;
    
    $query = "
        SELECT 
            SUM(CASE WHEN status = 'registered' THEN 1 ELSE 0 END) as registered,
            SUM(CASE WHEN checked_in = 1 THEN 1 ELSE 0 END) as attended,
            SUM(CASE WHEN checked_in = 0 AND status = 'registered' THEN 1 ELSE 0 END) as pending
        FROM registrations
    ";
    
    $result = $conn->query($query);
    $data = $result->fetch_assoc();
    
    http_response_code(200);
    echo json_encode([
        'userDistribution' => [
            'registered' => (int)($data['registered'] ?? 0),
            'attended' => (int)($data['attended'] ?? 0),
            'pending' => (int)($data['pending'] ?? 0)
        ]
    ]);
}

function get_recent_registrations() {
    global $conn;
    
    $query = "
        SELECT 
            r.registration_id,
            u.first_name,
            u.last_name,
            u.email,
            e.event_name,
            r.created_at,
            r.checked_in,
            r.status
        FROM registrations r
        JOIN `user` u ON r.user_id = u.user_id
        JOIN events e ON r.event_id = e.event_id
        ORDER BY r.created_at DESC
        LIMIT 5
    ";
    
    $result = $conn->query($query);
    $registrations = [];
    
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $created_time = strtotime($row['created_at']);
            $time_diff = time() - $created_time;
            
            if ($time_diff < 60) {
                $time_ago = 'Just now';
            } elseif ($time_diff < 3600) {
                $minutes = floor($time_diff / 60);
                $time_ago = $minutes . ' minute' . ($minutes > 1 ? 's' : '') . ' ago';
            } elseif ($time_diff < 86400) {
                $hours = floor($time_diff / 3600);
                $time_ago = $hours . ' hour' . ($hours > 1 ? 's' : '') . ' ago';
            } else {
                $days = floor($time_diff / 86400);
                $time_ago = $days . ' day' . ($days > 1 ? 's' : '') . ' ago';
            }
            
            $badge = $row['checked_in'] ? 'verified' : 'pending';
            $badge_text = $row['checked_in'] ? 'Verified' : 'Pending';
            
            $registrations[] = [
                'name' => $row['first_name'] . ' ' . $row['last_name'],
                'initials' => strtoupper($row['first_name'][0] . $row['last_name'][0]),
                'event' => $row['event_name'],
                'time' => $time_ago,
                'badge' => $badge,
                'badge_text' => $badge_text
            ];
        }
    }
    
    http_response_code(200);
    echo json_encode(['recentRegistrations' => $registrations]);
}

function get_all_events() {
    global $conn;
    
    $query = "
        SELECT 
            e.event_id,
            e.event_name,
            e.event_description,
            e.event_start,
            e.event_end,
            e.location,
            COUNT(r.registration_id) as total_registrations
        FROM events e
        LEFT JOIN registrations r ON e.event_id = r.event_id
        GROUP BY e.event_id
        ORDER BY e.event_start DESC
    ";
    
    $result = $conn->query($query);
    $events = [];
    
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $events[] = $row;
        }
    }
    
    http_response_code(200);
    echo json_encode(['events' => $events]);
}

function get_all_registrations() {
    global $conn;
    
    $query = "
        SELECT 
            r.registration_id,
            u.user_id,
            u.first_name,
            u.last_name,
            u.email,
            e.event_name,
            r.created_at,
            r.checked_in,
            r.status
        FROM registrations r
        JOIN `user` u ON r.user_id = u.user_id
        JOIN events e ON r.event_id = e.event_id
        ORDER BY r.created_at DESC
    ";
    
    $result = $conn->query($query);
    $registrations = [];
    
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $registrations[] = $row;
        }
    }
    
    http_response_code(200);
    echo json_encode(['registrations' => $registrations]);
}

function get_attendance() {
    global $conn;
    
    $query = "
        SELECT 
            e.event_name,
            COUNT(r.registration_id) as total_registered,
            SUM(CASE WHEN r.checked_in = 1 THEN 1 ELSE 0 END) as attended,
            ROUND(100.0 * SUM(CASE WHEN r.checked_in = 1 THEN 1 ELSE 0 END) / COUNT(r.registration_id), 2) as attendance_rate
        FROM events e
        LEFT JOIN registrations r ON e.event_id = r.event_id
        GROUP BY e.event_id, e.event_name
        ORDER BY e.event_start DESC
    ";
    
    $result = $conn->query($query);
    $attendance = [];
    
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $attendance[] = $row;
        }
    }
    
    http_response_code(200);
    echo json_encode(['attendance' => $attendance]);
}

// ═══════════════════════════════════════════════════════════════
// TICKET & REGISTRATION ENDPOINTS
// ═══════════════════════════════════════════════════════════════

function get_available_events() {
    global $conn;
    
    $query = "
        SELECT 
            event_id,
            event_name,
            event_description,
            event_start,
            event_end,
            location,
            ticket_price,
            max_capacity,
            COUNT(r.registration_id) as registered_count,
            (max_capacity - COUNT(r.registration_id)) as spots_available
        FROM events e
        LEFT JOIN registrations r ON e.event_id = r.event_id AND r.status = 'registered'
        WHERE e.status = 'published' AND e.event_start > NOW()
        GROUP BY e.event_id
        ORDER BY e.event_start ASC
    ";
    
    $result = $conn->query($query);
    $events = [];
    
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $events[] = $row;
        }
    }
    
    http_response_code(200);
    echo json_encode(['events' => $events]);
}

function buy_ticket($data) {
    global $conn;
    
    if (!isset($data['user_id']) || !isset($data['event_id'])) {
        http_response_code(400);
        echo json_encode(['error' => 'User ID and Event ID required']);
        return;
    }
    
    $user_id = (int)$data['user_id'];
    $event_id = (int)$data['event_id'];
    
    // Get event details
    $event_result = $conn->query("SELECT event_id, event_name, ticket_price FROM events WHERE event_id = $event_id LIMIT 1");
    if (!$event_result || $event_result->num_rows === 0) {
        http_response_code(404);
        echo json_encode(['error' => 'Event not found']);
        return;
    }
    $event = $event_result->fetch_assoc();
    
    // Check if already registered
    $check = $conn->query("SELECT registration_id FROM registrations WHERE user_id = $user_id AND event_id = $event_id AND status = 'registered' LIMIT 1");
    if ($check && $check->num_rows > 0) {
        http_response_code(409);
        echo json_encode(['error' => 'Ticket already purchased']);
        return;
    }
    
    // Create registration
    $stmt = $conn->prepare("INSERT INTO registrations (user_id, event_id, status, amount_paid, payment_status) VALUES (?, ?, 'registered', ?, 'completed')");
    $price = $event['ticket_price'];
    $stmt->bind_param("iid", $user_id, $event_id, $price);
    
    if ($stmt->execute()) {
        $registration_id = $stmt->insert_id;
        
        // Generate ticket code
        $ticket_code = strtoupper(substr(md5($user_id . $event_id . $registration_id), 0, 12));
        
        // Insert ticket
        $ticket_stmt = $conn->prepare("INSERT INTO tickets (ticket_code, registration_id, event_id, user_id, status, price) VALUES (?, ?, ?, ?, 'available', ?)");
        $ticket_stmt->bind_param("siiii", $ticket_code, $registration_id, $event_id, $user_id, $price);
        $ticket_stmt->execute();
        $ticket_stmt->close();
        
        http_response_code(201);
        echo json_encode([
            'message' => 'Ticket purchased successfully for ' . $event['event_name'] . '!',
            'ticket_code' => $ticket_code,
            'event_name' => $event['event_name'],
            'price' => $event['ticket_price'],
            'registration_id' => $registration_id
        ]);
    } else {
        http_response_code(500);
        echo json_encode(['error' => $stmt->error]);
    }
    $stmt->close();
}

function register_for_event($data) {
    global $conn;
    
    if (!isset($data['user_id']) || !isset($data['event_id'])) {
        http_response_code(400);
        echo json_encode(['error' => 'User ID and Event ID required']);
        return;
    }
    
    $user_id = (int)$data['user_id'];
    $event_id = (int)$data['event_id'];
    $amount_paid = isset($data['amount_paid']) ? (float)$data['amount_paid'] : 0;
    
    // Check if already registered
    $check = $conn->query("SELECT registration_id FROM registrations WHERE user_id = $user_id AND event_id = $event_id LIMIT 1");
    if ($check && $check->num_rows > 0) {
        http_response_code(409);
        echo json_encode(['error' => 'User already registered for this event']);
        return;
    }
    
    // Get event details
    $event_result = $conn->query("SELECT event_name, ticket_price FROM events WHERE event_id = $event_id LIMIT 1");
    if (!$event_result || $event_result->num_rows === 0) {
        http_response_code(404);
        echo json_encode(['error' => 'Event not found']);
        return;
    }
    $event = $event_result->fetch_assoc();
    
    $price = $amount_paid ?: $event['ticket_price'];
    
    // Create registration
    $stmt = $conn->prepare("INSERT INTO registrations (user_id, event_id, status, amount_paid, payment_status) VALUES (?, ?, 'registered', ?, 'completed')");
    $stmt->bind_param("iid", $user_id, $event_id, $price);
    
    if ($stmt->execute()) {
        $registration_id = $stmt->insert_id;
        
        // Generate ticket
        $ticket_code = strtoupper(substr(md5($user_id . $event_id . $registration_id), 0, 12));
        
        $ticket_stmt = $conn->prepare("INSERT INTO tickets (ticket_code, registration_id, event_id, user_id, status, price) VALUES (?, ?, ?, ?, 'available', ?)");
        $ticket_stmt->bind_param("siiii", $ticket_code, $registration_id, $event_id, $user_id, $price);
        $ticket_stmt->execute();
        $ticket_stmt->close();
        
        http_response_code(201);
        echo json_encode([
            'message' => 'Successfully registered for ' . $event['event_name'] . '!',
            'registration_id' => $registration_id,
            'ticket_code' => $ticket_code,
            'amount_paid' => $price
        ]);
    } else {
        http_response_code(500);
        echo json_encode(['error' => $stmt->error]);
    }
    $stmt->close();
}

function check_in_user($data) {
    global $conn;
    
    if (!isset($data['ticket_code'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Ticket code required']);
        return;
    }
    
    $ticket_code = $conn->real_escape_string(strtoupper($data['ticket_code']));
    
    // Find ticket
    $query = "
        SELECT t.ticket_id, t.registration_id, r.user_id, r.event_id, r.checked_in,
               u.first_name, u.last_name, e.event_name
        FROM tickets t
        JOIN registrations r ON t.registration_id = r.registration_id
        JOIN `user` u ON r.user_id = u.user_id
        JOIN events e ON r.event_id = e.event_id
        WHERE t.ticket_code = '$ticket_code' AND t.status = 'available'
        LIMIT 1
    ";
    
    $result = $conn->query($query);
    
    if (!$result || $result->num_rows === 0) {
        http_response_code(404);
        echo json_encode(['error' => 'Invalid or already used ticket']);
        return;
    }
    
    $ticket = $result->fetch_assoc();
    
    if ($ticket['checked_in']) {
        http_response_code(400);
        echo json_encode(['error' => 'Already checked in']);
        return;
    }
    
    // Update registration
    $conn->query("UPDATE registrations SET checked_in = 1, check_in_time = NOW(), status = 'checked_in' WHERE registration_id = " . (int)$ticket['registration_id']);
    
    // Update ticket
    $conn->query("UPDATE tickets SET status = 'used', used_date = NOW() WHERE ticket_id = " . (int)$ticket['ticket_id']);
    
    http_response_code(200);
    echo json_encode([
        'message' => 'Successfully checked in ' . $ticket['first_name'] . ' ' . $ticket['last_name'] . '!',
        'attendee_name' => $ticket['first_name'] . ' ' . $ticket['last_name'],
        'event_name' => $ticket['event_name'],
        'check_in_time' => date('Y-m-d H:i:s')
    ]);
}

?>
