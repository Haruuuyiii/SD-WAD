<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);
include 'connect.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['register'])) {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';

    if ($username === '' || $password === '') {
        $_SESSION['reg_error'] = "Please fill all fields.";
        $_SESSION['show_tab'] = 'register'; // <- keep user on registration panel
        header("Location: page2.html");
        exit;
    }

    // check existing username
    $stmt = $conn->prepare("SELECT id FROM `users` WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->store_result();
    if ($stmt->num_rows > 0) {
        $_SESSION['reg_error'] = "Username Already Registered.";
        $_SESSION['show_tab'] = 'register'; // <- keep user on registration panel
        $stmt->close();
        header("Location: page2.html");
        exit;
    }
    $stmt->close();

    // store hashed password
    $hash = password_hash($password, PASSWORD_DEFAULT);
    $stmt = $conn->prepare("INSERT INTO `users` (username, password) VALUES (?, ?)");
    $stmt->bind_param("ss", $username, $hash);
    if ($stmt->execute()) {
        $_SESSION['reg_success'] = "Account created successfully.";
        $_SESSION['show_tab'] = 'register';
        header("Location: page2.html"); 
    } else {
        $_SESSION['reg_error'] = "Registration failed: " . $stmt->error;
        $_SESSION['show_tab'] = 'register';
        header("Location: page2.html");
        exit;
    }
}
header("Location: page2.html");
exit;
?>