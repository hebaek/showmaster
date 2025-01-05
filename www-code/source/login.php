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
        if($clean['username'] == "stale" && $clean['password'] == "stale") {
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
    <meta charset='UTF-8'>
</head>

<body>
    <div id='splash'></div>
    <div id='form'>
        <form name='form1' method='post' action='index.php'>
            <div id='username-div'>
                <div id='username-label'>Brukernavn</div>
                <div id='username-input'><input name='username' type='text' id='username'></div>
            </div>
            <div id='password-div'>
                <div id='password-label'>Passord</div>
                <div id='password-input'><input name='password' type='password' id='password'></div>
            </div>
            <div id='message-div'>
                <div id='message-label'><?php echo $clean['message'] ?></div>
            </div>
            <div id='submit-div'>
                <div id='sublit-label'></div>
                <div id='submit-input'><input type='submit' name='Submit' value='Logg inn'></div>
            </div>
        </form>
    </div>
</body>

</html>
