<?php
    session_start();

    $accept_user = false;

    if (isset($_SESSION['username']) && $_SESSION['username'] === "stale") {
        $accept_user = true;
    }
    if (isset($_SESSION['username']) && $_SESSION['username'] === "nicklas") {
        $accept_user = true;
    }

    if (!$accept_user) {
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
        </div>

        <div class='navigation'>
            <div class='buttons scenes'>
                <div class='shortcuts scenes'></div>
                <div class='heading'>Scener</div>
                <button class='content'></button>
                <button class='prev'>forrige</button>
                <button class='next'>neste</button>
            </div>
            <div class='buttons music'>
                <div class='shortcuts music'></div>
                <div class='heading'>Musikk</div>
                <button class='content'></button>
                <button class='prev'>forrige</button>
                <button class='next'>neste</button>
            </div>
        </div>
    </div>

    <div class='manus' id='manus'>
    </div>

    <div class='pdf' id='pdf'>
    </div>

    <div id='contextmenu'>
        <div id='cue_add'>Add cue</div>
        <div id='cue_remove'>Remove cue</div>
    </div>
</body>

</html>
