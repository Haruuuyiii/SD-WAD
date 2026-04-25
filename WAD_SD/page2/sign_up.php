<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);
include 'connect.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['register'])) {
    $username = trim($_POST['username'] ?? '');
    $email    = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';

    if ($username === '' || $email === '' || $password === '') {
        $_SESSION['reg_error'] = "Please fill all fields.";
        $_SESSION['show_tab'] = 'register'; // <- keep user on registration panel
        header("Location: index.php");
        exit;
    }

    // check existing email or username (single query)
    $stmt = $conn->prepare("SELECT id FROM `user` WHERE email = ? OR username = ?");
    $stmt->bind_param("ss", $email, $username);
    $stmt->execute();
    $stmt->store_result();
    if ($stmt->num_rows > 0) {
        $_SESSION['reg_error'] = "Email or Username Already Registered.";
        $_SESSION['show_tab'] = 'register'; // <- keep user on registration panel
        $stmt->close();
        header("Location: index.php");
        exit;
    }
    $stmt->close();

    // store hashed password
    $hash = password_hash($password, PASSWORD_DEFAULT);
    $stmt = $conn->prepare("INSERT INTO `user` (username, email, password) VALUES (?, ?, ?)");
    $stmt->bind_param("sss", $username, $email, $hash);
    if ($stmt->execute()) {
        $_SESSION['reg_success'] = "Account created successfully.";
        $_SESSION['show_tab'] = 'register';
        header("Location: index.php"); 
    } else {
        $_SESSION['reg_error'] = "Registration failed: " . $stmt->error;
        $_SESSION['show_tab'] = 'register';
        header("Location: index.php");
        exit;
    }
}
header("Location: index.php");
exit;
?>