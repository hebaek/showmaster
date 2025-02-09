<?php
    session_start();

    if ($_SESSION['username'] != 'svgs' and $_SESSION['username'] != 'master') {
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
            <button class='settings' id='view'><img src='img/view.svg' alt='oppsett'></button>
            <button class='settings' id='print'><img src='img/paper.svg' alt='pdf'></button>
            <button class='settings' id='help'><img src='img/help.svg' alt='help'></button>

            <button class='settings disabled' id='read'>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentcolor" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 12V19M12 19L9.75 16.6667M12 19L14.25 16.6667M6.6 17.8333C4.61178 17.8333 3 16.1917 3 14.1667C3 12.498 4.09438 11.0897 5.59198 10.6457C5.65562 10.6268 5.7 10.5675 5.7 10.5C5.7 7.46243 8.11766 5 11.1 5C14.0823 5 16.5 7.46243 16.5 10.5C16.5 10.5582 16.5536 10.6014 16.6094 10.5887C16.8638 10.5306 17.1284 10.5 17.4 10.5C19.3882 10.5 21 12.1416 21 14.1667C21 16.1917 19.3882 17.8333 17.4 17.8333" />
                </svg>
            </button>
            <button class='settings disabled' id='write'>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentcolor" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 12V19M12 12L9.75 14.6667M12 12L14.25 14.6667M6.6 17.8333C4.61178 17.8333 3 16.1917 3 14.1667C3 12.498 4.09438 11.0897 5.59198 10.6457C5.65562 10.6268 5.7 10.5675 5.7 10.5C5.7 7.46243 8.11766 5 11.1 5C14.0823 5 16.5 7.46243 16.5 10.5C16.5 10.5582 16.5536 10.6014 16.6094 10.5887C16.8638 10.5306 17.1284 10.5 17.4 10.5C19.3882 10.5 21 12.1416 21 14.1667C21 16.1917 19.3882 17.8333 17.4 17.8333" />
                </svg>
            </button>

            <div class='shortcuts view'></div>
            <div class='shortcuts print'></div>
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
            <div class='buttons pages'>
                <div class='shortcuts pages'></div>
                <div class='heading'>Sider</div>
                <button class='content'></button>
                <button class='prev'>forrige</button>
                <button class='next'>neste</button>
            </div>
        </div>
    </div>

    <div id='pdf'>
        <canvas id='pdf-canvas'></canvas>
    </div>
<!--    <iframe id='pdf-viewer'></iframe>       -->

    <div id='infobar'>
        <div class='miclist' id='miclist'></div>
    </div>
</body>

</html>
