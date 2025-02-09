<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Read the current page number from the file
    $currentPage = intval(file_get_contents('currentpage-' . $_SESSION['username'] . '.txt'));
    echo $currentPage;
} else {
    echo "Invalid request method.";
}
?>
