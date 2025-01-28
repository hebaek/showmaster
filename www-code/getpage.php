<?php
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Read the current page number from the file
    $currentPage = intval(file_get_contents('currentpage.txt'));
    echo $currentPage;
} else {
    echo "Invalid request method.";
}
?>
