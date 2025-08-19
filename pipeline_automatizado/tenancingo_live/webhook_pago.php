<?php
/**
 * Webhook de pagos - TenancingoLive
 * Procesa pagos y genera tokens de acceso
 */

require_once 'config/config.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit(json_encode(['error' => 'Method not allowed']));
}

$input = file_get_contents('php://input');
$data = json_decode($input, true);

// Verificar webhook según proveedor
$verified = false;
switch (PAYMENT_PROVIDER) {
    case 'stripe':
        $verified = verifyStripeWebhook($input, $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '');
        break;
    case 'conekta':
        $verified = verifyConektaWebhook($data);
        break;
    case 'mercadopago':
        $verified = verifyMercadoPagoWebhook($data);
        break;
}

if (!$verified) {
    http_response_code(400);
    exit(json_encode(['error' => 'Invalid webhook']));
}

// Extraer datos del pago
$email = $data['email'] ?? $data['customer']['email'] ?? '';
$eventId = $data['metadata']['event_id'] ?? '';
$paymentId = $data['id'] ?? '';
$amount = $data['amount'] ?? 0;

if (!$email || !$eventId) {
    http_response_code(400);
    exit(json_encode(['error' => 'Missing required data']));
}

try {
    $pdo = getDBConnection();
    
    // Verificar que el evento existe
    $stmt = $pdo->prepare("SELECT * FROM events WHERE id = ? AND active = 1");
    $stmt->execute([$eventId]);
    $event = $stmt->fetch();
    
    if (!$event) {
        throw new Exception('Event not found');
    }
    
    // Generar token de acceso
    $tokenPayload = [
        'email' => $email,
        'event_id' => $eventId,
        'payment_id' => $paymentId,
        'iat' => time(),
        'exp' => time() + TOKEN_EXPIRY
    ];
    
    $accessToken = generateJWT($tokenPayload);
    
    // Guardar token en base de datos
    $stmt = $pdo->prepare("
        INSERT INTO access_tokens (token, email, event_id, payment_id, amount, expires_at, created_at) 
        VALUES (?, ?, ?, ?, ?, FROM_UNIXTIME(?), NOW())
    ");
    $stmt->execute([
        $accessToken, 
        $email, 
        $eventId, 
        $paymentId, 
        $amount, 
        $tokenPayload['exp']
    ]);
    
    // Generar link de acceso
    $accessLink = BASE_URL . "/watch.php?event={$eventId}&token={$accessToken}";
    
    // Enviar email con acceso
    sendAccessEmail($email, $event, $accessLink);
    
    // Log de actividad
    logActivity('payment_processed', [
        'email' => $email,
        'event_id' => $eventId,
        'payment_id' => $paymentId,
        'amount' => $amount
    ]);
    
    echo json_encode([
        'success' => true,
        'access_link' => $accessLink,
        'token' => $accessToken
    ]);
    
} catch (Exception $e) {
    error_log("Error procesando pago: " . $e->getMessage());
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error']);
}

function verifyStripeWebhook($payload, $signature) {
    if (!STRIPE_WEBHOOK_SECRET) return true; // Skip en desarrollo
    
    $elements = explode(',', $signature);
    $signatureHash = '';
    
    foreach ($elements as $element) {
        if (strpos($element, 'v1=') === 0) {
            $signatureHash = substr($element, 3);
        }
    }
    
    $expectedSignature = hash_hmac('sha256', $payload, STRIPE_WEBHOOK_SECRET);
    return hash_equals($expectedSignature, $signatureHash);
}

function verifyConektaWebhook($data) {
    return isset($data['type']) && $data['type'] === 'order.paid';
}

function verifyMercadoPagoWebhook($data) {
    return isset($data['action']) && $data['action'] === 'payment.created';
}

function sendAccessEmail($email, $event, $accessLink) {
    $subject = "Acceso a {$event['title']} - TenancingoLive";
    $message = "
        <h2>¡Tu acceso está listo!</h2>
        <p>Gracias por tu compra. Ya puedes ver <strong>{$event['title']}</strong></p>
        <p><a href='{$accessLink}' style='background: #007cba; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Ver Evento</a></p>
        <p><small>Este enlace es válido por 6 horas desde la compra.</small></p>
    ";
    
    $headers = [
        'MIME-Version: 1.0',
        'Content-type: text/html; charset=UTF-8',
        'From: ' . FROM_EMAIL,
        'Reply-To: ' . FROM_EMAIL
    ];
    
    mail($email, $subject, $message, implode("\r\n", $headers));
}
?>