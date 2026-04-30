<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);
include 'page2/connect.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login'])) {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';

    if ($username === '' || $password === '') {
        $_SESSION['login_error'] = "Please fill all fields.";
        $_SESSION['show_tab'] = 'login';
        header("Location: index.html");
        exit;
    }

    $stmt = $conn->prepare("SELECT id, username, password FROM `user` WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        if (password_verify($password, $row['password'])) {
            $_SESSION['username'] = $row['username'];
            unset($_SESSION['login_error'], $_SESSION['reg_error'], $_SESSION['show_tab']);
            header("Location: index.html");
            exit;
        }
    }

    $_SESSION['login_error'] = "Invalid Username or Password.";
    $_SESSION['show_tab'] = 'login';
    $stmt->close();
    header("Location: index.html");
    exit;
}

// fallback
header("Location: index.html");
exit;
?>