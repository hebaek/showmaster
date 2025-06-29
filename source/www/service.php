<?php require '../php/authenticate.php'; ?>
<?php


// Check if the user is logged in
if (!isset($_SESSION['username'])) {
    header('HTTP/1.1 403 Forbidden');
    echo "Access denied: Please log in to access this resource.";
    exit;
}

// Database connection details
$host = 'localhost';
$dbname = 'showmaster'; // Replace with your database name
$dbuser = 'showmaster'; // Replace with your database username
$dbpass = 'showmaster'; // Replace with your database password

try {
    // Connect to the database
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $dbuser, $dbpass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    header('HTTP/1.1 500 Internal Server Error');
    echo "Database connection failed: " . htmlspecialchars($e->getMessage());
    exit;
}

// Clean GET and POST inputs
$request = array_merge($_GET, $_POST);



// Resource handler
$action  = filter_var($request['action']  ?? null, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
$content = filter_var($request['content'] ?? null, FILTER_SANITIZE_FULL_SPECIAL_CHARS);



if ($action == 'load') {
    switch ($content) {
        case 'manus':
            $revision = filter_var($request['revision'] ?? null, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
            try {
                if ($revision) {
                    $stmt = $pdo->prepare("SELECT json FROM manus WHERE revision = :revision");
                    $stmt->execute(['revision' => $revision]);
                } else {
                    $stmt = $pdo->prepare("SELECT json FROM manus ORDER BY manus_id DESC LIMIT 1");
                    $stmt->execute();
                }
                $data = $stmt->fetch(PDO::FETCH_ASSOC);
                if ($data) {
                    header('Content-Type: application/json');
                    echo $data['json'];
                    exit;
                } else {
                    header('HTTP/1.1 404 Not Found');
                    echo "Resource not found.";
                    exit;
                }
            } catch (PDOException $e) {
                header('HTTP/1.1 500 Internal Server Error');
                echo "Error fetching data: " . htmlspecialchars($e->getMessage());
                exit;
            }
            break;

        case 'cues':
            $revision = filter_var($request['revision'] ?? null, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
            try {
                if ($revision) {
                    $stmt = $pdo->prepare("SELECT json FROM cues WHERE revision = :revision");
                    $stmt->execute(['revision' => $revision]);
                } else {
                    $stmt = $pdo->prepare("SELECT json FROM cues ORDER BY cues_id DESC LIMIT 1");
                    $stmt->execute();
                }
                $data = $stmt->fetch(PDO::FETCH_ASSOC);
                if ($data) {
                    header('Content-Type: application/json');
                    echo $data['json'];
                    exit;
                } else {
                    header('HTTP/1.1 404 Not Found');
                    echo "Resource not found.";
                    exit;
                }
            } catch (PDOException $e) {
                header('HTTP/1.1 500 Internal Server Error');
                echo "Error fetching data: " . htmlspecialchars($e->getMessage());
                exit;
            }
            break;

        default: // Handle unsupported actions
            header('HTTP/1.1 400 Bad Request');
            echo "Invalid action. ($action) Supported actions: 'get_data', 'serve_file'.";
            exit;
    }
}



else if ($action == 'save') {
    switch ($content) {
        case 'cues':
            $revision = filter_var($request['revision'] ?? null, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
            $json = $request['json'];

            if (empty($json) || json_decode($json) === null) {
                header('HTTP/1.1 400 Bad Request');
                echo json_encode(['error' => 'Invalid or empty JSON data.', 'json' => $json ]);
                exit;
            }

            try {
                $stmt = $pdo->prepare("INSERT INTO `cues` (`revision`, `json`) VALUES (:revision, :json)");
                $stmt->execute(['revision' => $revision, 'json' => $json]);

                if ($stmt->rowCount() > 0) {
                    header('Content-Type: application/json');
                    echo json_encode(['success' => true]);
                    exit;
                } else {
                    header('HTTP/1.1 500 Internal Server Error');
                    echo json_encode(['error' => 'Insert failed.']);
                    exit;
                }
            } catch (PDOException $e) {
                header('HTTP/1.1 500 Internal Server Error');
                echo json_encode(['error' => htmlspecialchars($e->getMessage())]);
                exit;
            }
            break;


        default: // Handle unsupported actions
            header('HTTP/1.1 400 Bad Request');
            echo "Invalid action. ($action) Supported actions: 'get_data', 'serve_file'.";
            exit;
    }
}



?>
