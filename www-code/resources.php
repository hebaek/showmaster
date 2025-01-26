<?php
    session_start();

    if ($_SESSION['username'] != 'svgs') {
        header('location:login.php');
        exit;
    }

    if (isset($_GET['file'])) {
        $userDir = __DIR__ . '/../data/pdf/';
        $filePath = $userDir . '/' . basename($_GET['file']);

        if (file_exists($filePath)) {
            header('Content-Description: File Transfer');
            header('Content-Type: application/octet-stream');
            header('Content-Disposition: attachment; filename="' . basename($filePath) . '"');
            header('Content-Length: ' . filesize($filePath));
            readfile($filePath);
            exit;
        } else {
            exit;
        }
    } else {
    }
?>
