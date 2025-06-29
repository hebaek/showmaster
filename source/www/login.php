<?php require '../php/login.php'; ?>
<!DOCTYPE html>
<html lang='no_NB'>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Showmaster - logg inn</title>

    <link rel='stylesheet' href='css/reset.css' />
    <link rel='stylesheet' href='css/login.css' />
</head>

<body>
    <img src="img/logo.png" alt="Logo"> <!-- Replace 'logo.png' with the path to your logo -->
    <div class="login-container">
        <h1>Logg inn</h1>

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
