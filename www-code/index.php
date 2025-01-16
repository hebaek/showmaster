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
    <div id="toolbar">
        <div class='display'>
            <div class='button' id='pdf-original'>Manus: Originalmanus</div>
            <div class='button' id='pdf-mics'>Manus: Med mikrofoner</div>
        </div>

        <div class="navigation scenes">
            <div class="shortcuts"></div>
            <button class="content"></button>
            <button class="prev">forrige</button>
            <button class="next">neste</button>
        </div>
        <div class="navigation music">
            <div class="shortcuts"></div>
            <button class="content"></button>
            <button class="prev">forrige</button>
            <button class="next">neste</button>
        </div>
        <div class="navigation pages">
            <div class="shortcuts"></div>
            <button class="content"></button>
            <button class="prev">forrige</button>
            <button class="next">neste</button>
        </div>
    </div>

    <div id='pdf-viewer'>
        <canvas id='pdf-canvas'></canvas>
    </div>

    <div id='infobar'>
        <div id='miclist'></div>
    </div>
</body>

</html>
