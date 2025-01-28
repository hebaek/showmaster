<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the new page number from the request
    $newPage = intval($_POST['page']);

    // Validate the page number (e.g., ensure it's positive)
    if ($newPage > 0) {
        // Write the new page number to the file
        file_put_contents('currentpage.txt', $newPage);
        echo "Page updated successfully.";
    } else {
        echo "Invalid page number.";
    }
} else {
    echo "Invalid request method.";
}
?>
