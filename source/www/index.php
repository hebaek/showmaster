<?php require '../php/authenticate.php'; ?>
<!DOCTYPE html>
<html lang='no_NB'>

<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Showmaster</title>

    <link rel='apple-touch-icon'      sizes='180x180' href='img/favicon/apple-touch-icon.png'>
    <link rel='icon' type='image/png' sizes='32x32'   href='img/favicon/favicon-32x32.png'>
    <link rel='icon' type='image/png' sizes='16x16'   href='img/favicon/favicon-16x16.png'>
    <link rel='manifest'                              href='img/favicon/site.webmanifest'>

    <link rel='stylesheet' href='css/reset.css' />
    <link rel='stylesheet' href='css/main.css' />

    <script src='js/external/pdf-3.9.179.min.js'></script>
    <script src='js/external/jquery-3.7.1.min.js'></script>
    <script src='js/external/jquery-ui-1.13.2.min.js'></script>

    <script src='js/modules/main.js' type='module'></script>
<!--    <script src='js/showmaster.js' type='module'></script> -->

    <script type='module'>
        import { smlib } from '/js/modules/smlib.js'
        smlib.pdfjsLib = pdfjsLib
    </script>
</head>

<body></body>

</html>
