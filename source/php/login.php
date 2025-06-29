<?php

session_start();

$clean = Array();
$clean['error']    = filter_input(INPUT_GET,  'error');
$clean['username'] = filter_input(INPUT_POST, 'username');
$clean['password'] = filter_input(INPUT_POST, 'password');
$clean['message']  = '';

$_SESSION = array();
unset($_SESSION);

session_destroy();
session_start();



// Database connection details
$host = 'localhost';
$dbname = 'showmaster'; // Replace with your database name
$dbuser = 'showmaster'; // Replace with your database username
$dbpass = 'showmaster'; // Replace with your database password

try {
    // Connect to the database
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $dbuser, $dbpass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    header('location:login.php?error=dbfailure');
    exit;
}

// Check if the username and password exist in the database
if (isset($clean['username'])) {
    $stmt = $pdo->prepare('SELECT password FROM users WHERE username = :username');
    $stmt->execute(['username' => $clean['username']]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && password_verify($clean['password'], $user['password'])) {
        // Login successful
        $_SESSION['username'] = $clean['username'];
        header('location:index.php');
        exit;
    } else {
        // Invalid credentials
        header('location:login.php?error=badcredentials');
        exit;
    }
}



if (isset($clean['error'])) {
    switch ($clean['error']) {
        case 'badcredentials':  $clean['message'] = 'Feil brukernavn eller passord';  break;
        case 'authfailure':     $clean['message'] = 'Feil i autentisering';           break;
        case 'dbfailure':       $clean['message'] = 'Feil i tilkobling til database'; break;
        case 'timedout':        $clean['message'] = 'Logget ut pga inaktivitet';      break;
        default:                $clean['message'] = 'En ukjent feil oppsto';          break;
    }
}

?>
