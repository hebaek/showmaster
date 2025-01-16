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

    <script src="js/pdf.worker.min.js"></script>
    <script src="js/pdf.min.js"></script>

    <script src='js/jquery-3.7.1.min.js'></script>
    <script src='js/jquery-ui-1.14.0.min.js'></script>

    <script src='js/showmaster.js'></script>
</head>

<body>
    <div class="toolbar">
        <div class='display'>
            <div class='button' id='pdf-original'>Manus: Originalmanus</div>
            <div class='button' id='pdf-mics'>Manus: Med mikrofoner</div>
        </div>

        <div class="scenes">
            <button class="content"></button>
            <button class="prev">forrige</button>
            <button class="next">neste</button>
        </div>
        <div class="music">
            <button class="content"></button>
            <button class="prev">forrige</button>
            <button class="next">neste</button>
        </div>
        <div class="pages">
            <button class="content"></button>
            <button class="prev">forrige</button>
            <button class="next">neste</button>
        </div>
    </div>

    <div class="shortcuts scenes"></div>
    <div class="shortcuts music"></div>
    <div class="shortcuts pages"></div>

    <div class='module' id='pdf-viewer'><canvas id='pdf-canvas'></canvas></div>
    <div class='module' id='details'></div>
</body>

</html>
