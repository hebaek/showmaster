<?php
    session_start();

    if ($_SESSION['username'] != 'svgs') {
        header('location:login.php');
    }
?>
<!DOCTYPE html>
<html lang='no_NB'>

<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Showmaster</title>

    <link rel='stylesheet' href='css/reset.css' />
    <link rel='stylesheet' href='css/showmaster.css' />

    <script src='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.9.179/pdf.min.js'></script>
    <script src='https://code.jquery.com/jquery-3.7.1.min.js'></script>

    <script src='js/showmaster.js'></script>
</head>

<body>
    <div id='toolbar'>
        <div id='menu'>
            <button class='settings' id='logout'><img src='img/logout.svg' alt='logg ut'></button>
            <button class='settings' id='settings'><img src='img/view.svg' alt='oppsett'></button>
            <button class='settings' id='print'><img src='img/paper.svg' alt='pdf'></button>
            <div class='shortcuts settings'></div>
            <div class='shortcuts print'></div>
        </div>

        <div class='navigation'>
            <div class='buttons scenes'>
                <div class='shortcuts scenes'></div>
                <button class='content'></button>
                <button class='prev'>forrige</button>
                <button class='next'>neste</button>
            </div>
            <div class='buttons music'>
                <div class='shortcuts music'></div>
                <button class='content'></button>
                <button class='prev'>forrige</button>
                <button class='next'>neste</button>
            </div>
            <div class='buttons pages'>
                <div class='shortcuts pages'></div>
                <button class='content'></button>
                <button class='prev'>forrige</button>
                <button class='next'>neste</button>
            </div>
        </div>
    </div>

    <div id='pdf'>
        <canvas id='pdf-canvas'></canvas>
    </div>

    <div id='infobar'>
        <div id='miclist'></div>
    </div>
</body>

</html>
