<?php

session_start();

// Check if the user is logged in
if (!isset($_SESSION['username'])) {
    // Redirect to the login page if not authenticated
    header('Location: login.php?error=authfailure');
    exit;
}

?>
