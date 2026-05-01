<?php
// ═══════════════════════════════════════════════════════════════
// CozMoz API Client Helper - For PHP
// Simplifies integration with admin dashboard
// ═══════════════════════════════════════════════════════════════

/**
 * API Configuration
 * Choose which backend to use: 'php' or 'python'
 */
define('COZMOZ_API_MODE', 'php');  // Change to 'python' to use Python service
define('COZMOZ_PHP_API_URL', 'http://localhost/path/to/page2/api.php');
define('COZMOZ_PYTHON_API_URL', 'http://localhost:3003');

/**
 * Get the appropriate API URL based on mode
 */
function get_api_url($endpoint = '') {
    if (COZMOZ_API_MODE === 'python') {
        return COZMOZ_PYTHON_API_URL . '/' . ltrim($endpoint, '/');
    } else {
        // PHP mode - use api.php with action parameter
        $action = ltrim($endpoint, '/');
        return COZMOZ_PHP_API_URL . '?action=' . urlencode($action);
    }
}

/**
 * Make API call from PHP backend
 */
function make_api_call($endpoint, $method = 'GET', $data = null) {
    $url = get_api_url($endpoint);
    
    $options = [
        'http' => [
            'method' => $method,
            'header' => 'Content-Type: application/json',
            'timeout' => 10
        ]
    ];
    
    if ($method === 'POST' && $data) {
        $options['http']['content'] = json_encode($data);
    }
    
    $context = stream_context_create($options);
    $response = @file_get_contents($url, false, $context);
    
    if ($response === false) {
        return [
            'error' => 'API call failed',
            'endpoint' => $endpoint,
            'url' => $url
        ];
    }
    
    return json_decode($response, true);
}

/**
 * Get Dashboard Statistics
 */
function get_dashboard_stats() {
    return make_api_call('dashboard/stats', 'GET');
}

/**
 * Get Event Registrations
 */
function get_event_registrations() {
    return make_api_call('dashboard/registrations-by-event', 'GET');
}

/**
 * Get User Distribution
 */
function get_user_distribution() {
    return make_api_call('dashboard/user-distribution', 'GET');
}

/**
 * Get Recent Registrations
 */
function get_recent_registrations() {
    return make_api_call('dashboard/recent-registrations', 'GET');
}

/**
 * Register New User
 */
function register_user($username, $email, $password, $first_name, $last_name) {
    return make_api_call('register', 'POST', [
        'username' => $username,
        'email' => $email,
        'password' => $password,
        'first_name' => $first_name,
        'last_name' => $last_name
    ]);
}

/**
 * Admin Login
 */
function admin_login($username, $password) {
    return make_api_call('admin/login', 'POST', [
        'username' => $username,
        'password' => $password
    ]);
}

/**
 * User Login
 */
function user_login($username, $password) {
    return make_api_call('login', 'POST', [
        'username' => $username,
        'password' => $password
    ]);
}

/**
 * Buy Ticket
 */
function buy_ticket($user_id, $event_id) {
    return make_api_call('buy-ticket', 'POST', [
        'user_id' => $user_id,
        'event_id' => $event_id
    ]);
}

/**
 * Check In User
 */
function check_in_user($ticket_code) {
    return make_api_call('check-in', 'POST', [
        'ticket_code' => $ticket_code
    ]);
}

/**
 * Get Available Events
 */
function get_available_events() {
    return make_api_call('events', 'GET');
}

/**
 * Get All Events (Admin)
 */
function get_all_events() {
    return make_api_call('dashboard/events', 'GET');
}

/**
 * Get All Registrations (Admin)
 */
function get_all_registrations() {
    return make_api_call('dashboard/registrations', 'GET');
}

/**
 * Get Attendance Data
 */
function get_attendance_data() {
    return make_api_call('dashboard/attendance', 'GET');
}

/**
 * Check API Health
 */
function check_api_health() {
    return make_api_call('health', 'GET');
}

?>
