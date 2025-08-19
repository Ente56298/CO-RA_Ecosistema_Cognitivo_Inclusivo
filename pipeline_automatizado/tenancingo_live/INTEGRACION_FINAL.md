# 🎯 Integración Final TenancingoLive

## 📋 Plan de Integración Completo

### **FASE 1: Configuración Base** ⚙️

#### 1.1 Configurar Base de Datos
```sql
-- Ejecutar en phpMyAdmin o consola MySQL
mysql -h sql202.byethost17.com -u b17_38301772 -p b17_38301772_tenancingo < database.sql
```

#### 1.2 Configurar Variables de Entorno
```php
// En config/config.php - Actualizar credenciales reales:
define('DB_PASS', 'tu_password_mysql_real');
define('JWT_SECRET', 'clave_super_secreta_jwt_2024');
define('STRIPE_SECRET_KEY', 'sk_live_tu_clave_stripe');
```

#### 1.3 Configurar Servidor RTMP/HLS
```bash
# Actualizar URLs en config.php:
define('RTMP_SERVER', 'rtmp://tu-servidor-streaming.com:1935/live');
define('HLS_BASE_URL', 'https://tu-servidor-streaming.com:8081/hls');
```

### **FASE 2: Despliegue** 🚀

#### 2.1 Subir Archivos
```bash
# Ejecutar script de despliegue
chmod +x scripts/deploy.sh
FTP_PASSWORD=tu_password_ftp ./scripts/deploy.sh
```

#### 2.2 Verificar Archivos Subidos
- ✅ `config.php` - Configuración central
- ✅ `webhook_pago.php` - Procesamiento de pagos
- ✅ `watch.php` - Página de visualización
- ✅ Archivos HTML existentes (index, dashboard, etc.)

### **FASE 3: Configuración de Pagos** 💳

#### 3.1 Configurar Webhook en Stripe
```
URL del webhook: https://tenancingo.byethost17.com/webhook_pago.php
Eventos a escuchar: checkout.session.completed, payment_intent.succeeded
```

#### 3.2 Probar Webhook
```bash
# Usar Stripe CLI para testing
stripe listen --forward-to https://tenancingo.byethost17.com/webhook_pago.php
```

### **FASE 4: Integración con Archivos Existentes** 🔗

#### 4.1 Actualizar stream_bridge.php
```php
// Añadir al inicio de stream_bridge.php:
require_once 'config.php';

// Reemplazar conexión DB existente con:
$pdo = getDBConnection();
```

#### 4.2 Actualizar streaming_integration.php
```php
// Integrar autenticación JWT:
$token = $_GET['token'] ?? '';
if ($token) {
    $userData = verifyJWT($token);
    if ($userData) {
        // Usuario autenticado - mostrar stream
    }
}
```

#### 4.3 Modificar dashboard.html
```html
<!-- Añadir sección de eventos -->
<div class="events-section">
    <h3>📅 Gestión de Eventos</h3>
    <button onclick="createEvent()">Crear Nuevo Evento</button>
    <div id="events-list"></div>
</div>

<script>
function createEvent() {
    // Formulario para crear eventos
    window.location.href = 'create_event.php';
}
</script>
```

## 🔄 Flujo de Usuario Completo

### **1. Registro/Login** (Archivos existentes)
```
index.html → register.php → verify-account.php → login.php
```

### **2. Selección de Evento** (Nuevo)
```
dashboard.html → Mostrar eventos disponibles → Botón "Comprar"
```

### **3. Proceso de Pago** (Integración)
```
checkout.php → Stripe → webhook_pago.php → Email con token
```

### **4. Acceso al Stream** (Nuevo)
```
watch.php?event=ID&token=JWT → Verificación → Reproductor HLS
```

## 📊 APIs Necesarias

### **API de Estado de Stream**
```php
// api/stream_status.php
<?php
require_once '../config.php';
$eventId = $_GET['event'] ?? '';
$pdo = getDBConnection();
$stmt = $pdo->prepare("SELECT status, viewer_count FROM active_streams WHERE event_id = ?");
$stmt->execute([$eventId]);
echo json_encode($stmt->fetch() ?: ['status' => 'offline', 'viewer_count' => 0]);
?>
```

### **API de Contador de Espectadores**
```php
// api/viewer-count.php
<?php
require_once '../config.php';
$eventId = $_GET['event'] ?? '';
// Lógica para contar espectadores activos
echo json_encode(['count' => rand(50, 200)]); // Placeholder
?>
```

## 🛠️ Comandos de Mantenimiento

### **Limpiar Tokens Expirados**
```sql
-- Ejecutar diariamente
DELETE FROM access_tokens WHERE expires_at < NOW();
```

### **Verificar Streams Activos**
```sql
-- Ver streams en vivo
SELECT e.title, s.viewer_count, s.started_at 
FROM events e 
JOIN active_streams s ON e.id = s.event_id 
WHERE s.status = 'live';
```

### **Log de Actividad**
```sql
-- Ver actividad reciente
SELECT action, details, ip_address, created_at 
FROM activity_log 
ORDER BY created_at DESC 
LIMIT 50;
```

## 🔧 Configuración de Servidor Streaming

### **NGINX RTMP** (Si usas VPS propio)
```nginx
# /etc/nginx/nginx.conf
rtmp {
    server {
        listen 1935;
        application live {
            live on;
            hls on;
            hls_path /var/www/hls;
            hls_fragment 3;
            
            # Autenticación
            on_publish http://tenancingo.byethost17.com/auth_stream.php;
        }
    }
}
```

### **Alternativa: Usar Servicio Externo**
- **Wowza Cloud**: Streaming profesional
- **AWS IVS**: Servicio de Amazon
- **YouTube Live**: API para streaming privado

## 📱 Testing del Sistema

### **1. Test de Registro**
```bash
curl -X POST https://tenancingo.byethost17.com/register.php \
  -d "email=test@example.com&password=123456&name=Test User"
```

### **2. Test de Webhook**
```bash
curl -X POST https://tenancingo.byethost17.com/webhook_pago.php \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","event_id":"2025-08-22-lucha1","amount":7900}'
```

### **3. Test de Acceso**
```bash
# Verificar que la página de evento carga
curl -I https://tenancingo.byethost17.com/watch.php?event=2025-08-22-lucha1
```

## 🚀 Próximos Pasos Inmediatos

### **Hoy**:
1. ✅ Ejecutar `deploy.sh` para subir archivos
2. ✅ Crear base de datos con `database.sql`
3. ✅ Configurar credenciales reales en `config.php`

### **Esta Semana**:
1. 🔧 Configurar webhook de Stripe
2. 🎬 Configurar servidor de streaming
3. 🧪 Probar flujo completo end-to-end

### **Próximo Mes**:
1. 📊 Implementar analytics
2. 💬 Añadir chat en vivo
3. 📱 Optimizar para móviles

---

## ✅ Checklist de Integración

- [ ] Base de datos creada y poblada
- [ ] Archivos PHP subidos al hosting
- [ ] Variables de entorno configuradas
- [ ] Webhook de Stripe configurado
- [ ] Servidor de streaming configurado
- [ ] Flujo de pago probado
- [ ] Reproductor HLS funcionando
- [ ] Emails de acceso enviándose
- [ ] Logs de actividad funcionando
- [ ] Dashboard administrativo actualizado

*Integración final lista para producción* 🎯