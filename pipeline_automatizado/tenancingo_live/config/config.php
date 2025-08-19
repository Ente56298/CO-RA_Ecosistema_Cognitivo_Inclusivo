<?php
/**
 * Configuración central TenancingoLive
 * Integración final para producción
 */

// Base de datos
define('DB_HOST', 'sql202.byethost17.com');
define('DB_NAME', 'b17_38301772_tenancingo');
define('DB_USER', 'b17_38301772');
define('DB_PASS', getenv('DB_PASSWORD') ?: 'tu_password_aqui');

// URLs del sistema
define('BASE_URL', 'https://tenancingo.byethost17.com');
define('RTMP_SERVER', 'rtmp://tu-servidor.com:1935/live');
define('HLS_BASE_URL', 'https://tu-servidor.com:8081/hls');

// JWT y tokens
define('JWT_SECRET', getenv('JWT_SECRET') ?: 'cambiar_en_produccion');
define('TOKEN_EXPIRY', 6 * 3600);

// Pagos
define('PAYMENT_PROVIDER', 'stripe');
define('STRIPE_SECRET_KEY', getenv('STRIPE_SECRET_KEY') ?: '');

// Conexión DB
function getDBConnection() {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4";
        $pdo = new PDO($dsn, DB_USER, DB_PASS, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]);
    }
    return $pdo;
}

// JWT functions
function generateJWT($payload) {
    $header = json_encode(['typ' => 'JWT', 'alg' => 'HS256']);
    $payload = json_encode($payload);
    $base64Header = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($header));
    $base64Payload = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($payload));
    $signature = hash_hmac('sha256', $base64Header . "." . $base64Payload, JWT_SECRET, true);
    $base64Signature = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($signature));
    return $base64Header . "." . $base64Payload . "." . $base64Signature;
}

function verifyJWT($token) {
    $parts = explode('.', $token);
    if (count($parts) !== 3) return false;
    $expectedSignature = str_replace(['+', '/', '='], ['-', '_', ''], 
        base64_encode(hash_hmac('sha256', $parts[0] . "." . $parts[1], JWT_SECRET, true)));
    if ($parts[2] !== $expectedSignature) return false;
    $payload = json_decode(base64_decode(str_replace(['-', '_'], ['+', '/'], $parts[1])), true);
    return ($payload['exp'] > time()) ? $payload : false;
}

session_start();
?>