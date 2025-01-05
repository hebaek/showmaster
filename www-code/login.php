<?php
    session_start();

    $clean = Array();
    $clean['error']    = filter_input(INPUT_GET,  'error');
    $clean['username'] = filter_input(INPUT_POST, 'username');
    $clean['password'] = filter_input(INPUT_POST, 'password');
    $clean['message']  = '';

    $_SESSION = array();
    unset($_SESSION);

    session_destroy();
    session_start();

    if (isset($clean['username'])) {
        if($clean['username'] === "stale" && $clean['password'] === "stale") {
            $_SESSION['username'] = $clean['username'];
            header('location:index.php');
        }
        else {
            header('location:login.php?error=badcredentials');
        }
    }

    if (isset($clean['error'])) {
        switch ($clean['error']) {
            case 'badcredentials':  $clean['message'] = 'Feil brukernavn eller passord';  break;
            case 'authfailure':     $clean['message'] = 'Feil i autentisering';           break;
            case 'dbfailure':       $clean['message'] = 'Feil i tilkobling til database'; break;
            case 'timedout':        $clean['message'] = 'Logget ut pga inaktivitet';      break;
            default:                $clean['message'] = 'En ukjent feil oppsto';          break;
        }
    }
?>
<!DOCTYPE html>
<html lang='no_NB'>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Showmaster</title>

    <link rel='stylesheet' href='css/reset.css' />
    <link rel='stylesheet' href='css/login.css' />
</head>

<body>
    <div class="login-container">
        <img src="img/logo.png" alt="Logo"> <!-- Replace 'logo.png' with the path to your logo -->
        <h1>Login</h1>

        <form name='form' method='post' action='login.php'>
            <input type="text" name="username" placeholder="brukernavn" required>
            <input type="password" name="password" placeholder="passord" required>
            <button type="submit">Logg inn</button>
        </form>

        <div id='message-div'>
            <div id='message-label'><?php echo $clean['message'] ?></div>
        </div>
    </div>
</body>

</html>
