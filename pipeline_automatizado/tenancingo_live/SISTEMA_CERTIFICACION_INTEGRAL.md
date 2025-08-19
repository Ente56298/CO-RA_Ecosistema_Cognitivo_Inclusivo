# 🔒 Sistema Integral de Certificación TenancingoLive

## 🎯 Protocolo de Certificación por Etapas

**Objetivo**: Validar que TenancingoLive esté 100% listo antes del lanzamiento público mediante un protocolo medible y trazable.

---

## 📋 **ETAPA 1: Certificación Técnica**

### **Objetivo**: Plataforma estable, segura y rápida

#### **Criterios de Aprobación**:
- [ ] **Dominio y SSL** - Certificado válido, sin contenido mixto
- [ ] **Navegación multiplataforma** - Android, iOS, Windows, Mac
- [ ] **Formularios operativos** - Envío, recepción, validaciones
- [ ] **Rendimiento < 3s** - Carga en 4G con compresión activa
- [ ] **Consola limpia** - Sin errores JavaScript críticos
- [ ] **Prueba de estrés** - 50+ usuarios concurrentes sin caída
- [ ] **Backups probados** - Restauración verificada

#### **Comandos de Validación**:
```bash
# Validación automática
./scripts/validate_production.sh

# Prueba de carga
ab -n 1000 -c 50 https://tenancingo.byethost17.com/

# Verificar SSL
openssl s_client -connect tenancingo.byethost17.com:443 -servername tenancingo.byethost17.com
```

#### **Evidencias Requeridas**:
- Screenshot de PageSpeed Insights (>90)
- Log de prueba de carga exitosa
- Certificado SSL válido por 90+ días
- Video de navegación en móvil/desktop

---

## 🛡️ **ETAPA 2: Certificación de Seguridad**

### **Objetivo**: Protección de datos y acceso restringido

#### **Criterios de Aprobación**:
- [ ] **Admin protegido** - URL no pública, 2FA activo
- [ ] **Credenciales cifradas** - Claves fuera del webroot
- [ ] **Permisos correctos** - Archivos 644, carpetas 755
- [ ] **Headers de seguridad** - HSTS, X-Frame-Options activos
- [ ] **Anti-inyecciones** - Sanitización SQL/XSS verificada
- [ ] **Logs seguros** - Acceso restringido, rotación activa

#### **Comandos de Validación**:
```bash
# Verificar headers de seguridad
curl -I https://tenancingo.byethost17.com/ | grep -E "X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security"

# Verificar permisos
find . -type f -exec ls -la {} \; | grep -v "644\|600"
find . -type d -exec ls -la {} \; | grep -v "755\|750"

# Test de inyección básica
curl -X POST "https://tenancingo.byethost17.com/login.php" -d "email=test'OR'1'='1&password=test"
```

#### **Evidencias Requeridas**:
- Reporte de escaneo de seguridad (OWASP ZAP)
- Screenshot de admin con 2FA activo
- Log de intentos de acceso bloqueados
- Certificado de permisos de archivos

---

## 🗂️ **ETAPA 3: Certificación de Contenido**

### **Objetivo**: Contenido real, actualizado y coherente

#### **Criterios de Aprobación**:
- [ ] **Textos reales** - Sin lorem ipsum, ortografía correcta
- [ ] **Identidad visual** - Logos, colores coherentes
- [ ] **Eventos actualizados** - Fechas y estados correctos
- [ ] **Documentos funcionales** - Descargas operativas
- [ ] **Páginas legales** - Privacidad, términos publicados

#### **Comandos de Validación**:
```bash
# Buscar contenido placeholder
curl -s https://tenancingo.byethost17.com/ | grep -i "lorem\|placeholder\|ejemplo\|test"

# Verificar páginas legales
curl -I https://tenancingo.byethost17.com/privacidad
curl -I https://tenancingo.byethost17.com/terminos
```

#### **Evidencias Requeridas**:
- Screenshot de cada página principal
- Lista de eventos con fechas verificadas
- Documentos PDF descargables probados
- Revisión ortográfica completada

---

## 🔗 **ETAPA 4: Certificación de Integración**

### **Objetivo**: Sistemas conectados y funcionando

#### **Criterios de Aprobación**:
- [ ] **Tablero Estratégico** - Datos reales cargando
- [ ] **Reportes COPLADEMUN** - Visibles/descargables
- [ ] **Núcleo evaluativo** - Sincronizado con SyConGob
- [ ] **Media embebida** - Videos/imágenes funcionando
- [ ] **Enlaces externos** - Normatividad Gobernova activa

#### **Comandos de Validación**:
```bash
# Verificar integraciones
curl -s https://tenancingo.byethost17.com/api/tablero | jq .
curl -I https://tenancingo.byethost17.com/reportes/coplademun.pdf
curl -I https://tenancingo.byethost17.com/videos/presentacion.mp4
```

#### **Evidencias Requeridas**:
- Screenshot de tablero con datos reales
- Lista de reportes descargables verificados
- Video de integración funcionando
- Enlaces externos probados

---

## 📢 **ETAPA 5: Certificación de Comunicación**

### **Objetivo**: Público entiende y puede interactuar

#### **Criterios de Aprobación**:
- [ ] **Mensaje claro** - Propósito del portal evidente
- [ ] **Video presentación** - Integrado y funcional
- [ ] **Canales contacto** - Correo, redes, formulario verificados
- [ ] **Respuesta < 24h** - Prueba de atención al usuario
- [ ] **Plan de lanzamiento** - Publicaciones y nota preparadas

#### **Comandos de Validación**:
```bash
# Probar formulario de contacto
curl -X POST https://tenancingo.byethost17.com/contacto.php -d "nombre=Test&email=test@example.com&mensaje=Prueba"

# Verificar redes sociales
curl -I https://facebook.com/tenancingolive
curl -I https://twitter.com/tenancingolive
```

#### **Evidencias Requeridas**:
- Screenshot de portada con mensaje claro
- Video de presentación reproducible
- Email de prueba recibido y respondido
- Plan de lanzamiento documentado

---

## 📊 **ETAPA 6: Acta de Certificación**

### **Documento Final de Aprobación**

#### **Contenido del Acta**:
```
ACTA DE CERTIFICACIÓN TENANCINGLIVE
===================================

Fecha: [YYYY-MM-DD HH:MM:SS]
Responsable: [Nombre del certificador]
Versión: [v1.0.0]

ETAPAS CERTIFICADAS:
✅ Técnica - Aprobada el [fecha]
✅ Seguridad - Aprobada el [fecha]  
✅ Contenido - Aprobada el [fecha]
✅ Integración - Aprobada el [fecha]
✅ Comunicación - Aprobada el [fecha]

EVIDENCIAS ADJUNTAS:
- Screenshots de validación
- Reportes de rendimiento
- Logs de seguridad
- Videos de prueba

FIRMA DE APROBACIÓN:
[Firma digital/hash]

AUTORIZACIÓN DE LANZAMIENTO:
✅ APROBADO PARA PRODUCCIÓN
```

---

## 🔧 **Implementación del Sistema**

### **Checklist Interactivo** (admin/certificacion.php):

```php
<?php
require_once 'config.php';

$etapas = [
    'tecnica' => [
        'nombre' => 'Certificación Técnica',
        'items' => [
            'ssl_valido' => 'Dominio y SSL activos',
            'navegacion_multi' => 'Navegación multiplataforma',
            'formularios_ok' => 'Formularios operativos',
            'rendimiento_3s' => 'Carga < 3 segundos',
            'consola_limpia' => 'Sin errores en consola',
            'prueba_estres' => 'Prueba de 50+ usuarios',
            'backups_ok' => 'Backups probados'
        ]
    ],
    'seguridad' => [
        'nombre' => 'Certificación de Seguridad',
        'items' => [
            'admin_protegido' => 'Admin con 2FA',
            'credenciales_cifradas' => 'Credenciales seguras',
            'permisos_correctos' => 'Permisos 644/755',
            'headers_seguridad' => 'Headers de seguridad',
            'anti_inyecciones' => 'Protección XSS/SQL',
            'logs_seguros' => 'Logs protegidos'
        ]
    ],
    'contenido' => [
        'nombre' => 'Certificación de Contenido',
        'items' => [
            'textos_reales' => 'Sin lorem ipsum',
            'identidad_visual' => 'Logos coherentes',
            'eventos_actualizados' => 'Fechas correctas',
            'documentos_funcionales' => 'Descargas OK',
            'paginas_legales' => 'Privacidad/términos'
        ]
    ],
    'integracion' => [
        'nombre' => 'Certificación de Integración',
        'items' => [
            'tablero_datos' => 'Tablero con datos reales',
            'reportes_coplademun' => 'Reportes descargables',
            'nucleo_evaluativo' => 'Sync con SyConGob',
            'media_embebida' => 'Videos funcionando',
            'enlaces_externos' => 'Links Gobernova activos'
        ]
    ],
    'comunicacion' => [
        'nombre' => 'Certificación de Comunicación',
        'items' => [
            'mensaje_claro' => 'Propósito evidente',
            'video_presentacion' => 'Video integrado',
            'canales_contacto' => 'Contacto verificado',
            'respuesta_24h' => 'Atención < 24h',
            'plan_lanzamiento' => 'Publicaciones listas'
        ]
    ]
];

// Obtener estado actual
$pdo = getDBConnection();
$stmt = $pdo->prepare("SELECT * FROM certificacion_estado ORDER BY updated_at DESC LIMIT 1");
$stmt->execute();
$estado = $stmt->fetch() ?: [];

?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Certificación - TenancingoLive</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .etapa { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .etapa.completada { background: #d4edda; border-color: #c3e6cb; }
        .item { margin: 10px 0; padding: 8px; }
        .item.completado { background: #d1ecf1; }
        .btn { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .btn.success { background: #28a745; }
        .progress { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }
        .progress-bar { height: 100%; background: #28a745; transition: width 0.3s; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Sistema Integral de Certificación</h1>
        <p><strong>Estado:</strong> <span id="estado-general">En proceso</span></p>
        
        <div class="progress">
            <div class="progress-bar" id="progress-bar" style="width: 0%"></div>
        </div>
        
        <?php foreach ($etapas as $etapa_id => $etapa): ?>
        <div class="etapa" id="etapa-<?= $etapa_id ?>">
            <h3><?= $etapa['nombre'] ?></h3>
            
            <?php foreach ($etapa['items'] as $item_id => $item_nombre): ?>
            <div class="item" id="item-<?= $item_id ?>">
                <label>
                    <input type="checkbox" name="<?= $item_id ?>" 
                           <?= isset($estado[$item_id]) && $estado[$item_id] ? 'checked' : '' ?>>
                    <?= $item_nombre ?>
                </label>
                <button class="btn" onclick="subirEvidencia('<?= $item_id ?>')">📎 Evidencia</button>
            </div>
            <?php endforeach; ?>
        </div>
        <?php endforeach; ?>
        
        <div style="text-align: center; margin: 30px 0;">
            <button class="btn success" onclick="generarActa()" id="btn-acta" disabled>
                📋 Generar Acta de Certificación
            </button>
        </div>
    </div>
    
    <script>
        function actualizarProgreso() {
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            const total = checkboxes.length;
            const completados = document.querySelectorAll('input[type="checkbox"]:checked').length;
            const porcentaje = Math.round((completados / total) * 100);
            
            document.getElementById('progress-bar').style.width = porcentaje + '%';
            document.getElementById('estado-general').textContent = 
                porcentaje === 100 ? '✅ CERTIFICADO' : `${porcentaje}% Completado`;
            
            document.getElementById('btn-acta').disabled = porcentaje < 100;
        }
        
        function subirEvidencia(itemId) {
            // Implementar subida de evidencias
            alert('Subir evidencia para: ' + itemId);
        }
        
        function generarActa() {
            if (confirm('¿Generar Acta de Certificación final?')) {
                window.location.href = 'generar_acta.php';
            }
        }
        
        // Event listeners
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                // Guardar estado
                fetch('guardar_certificacion.php', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        item: this.name,
                        completado: this.checked
                    })
                });
                
                actualizarProgreso();
            });
        });
        
        // Inicializar
        actualizarProgreso();
    </script>
</body>
</html>
```

### **Base de Datos para Certificación**:

```sql
-- Tabla para estado de certificación
CREATE TABLE IF NOT EXISTS certificacion_estado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id VARCHAR(50) NOT NULL,
    completado BOOLEAN DEFAULT FALSE,
    evidencia_url VARCHAR(500),
    responsable VARCHAR(100),
    fecha_completado DATETIME,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_item (item_id)
);

-- Tabla para actas de certificación
CREATE TABLE IF NOT EXISTS actas_certificacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version VARCHAR(20) NOT NULL,
    fecha_certificacion DATETIME NOT NULL,
    responsable VARCHAR(100) NOT NULL,
    hash_evidencias VARCHAR(64),
    estado ENUM('borrador', 'aprobada', 'rechazada') DEFAULT 'borrador',
    archivo_pdf VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 **Comandos de Certificación**

### **Ejecutar Certificación Completa**:
```bash
# 1. Validación automática
./scripts/validate_production.sh

# 2. Acceder al panel de certificación
https://tenancingo.byethost17.com/admin/certificacion.php

# 3. Completar checklist interactivo
# 4. Subir evidencias por cada item
# 5. Generar acta final
```

### **Verificar Estado**:
```bash
# Ver progreso actual
curl -s https://tenancingo.byethost17.com/api/certificacion/estado

# Descargar acta PDF
curl -O https://tenancingo.byethost17.com/actas/certificacion_v1.0.0.pdf
```

---

## ✅ **Criterios de Aprobación Final**

**Para declarar "CERTIFICADO AL 100%":**

1. ✅ **Todas las etapas completadas** (30/30 items)
2. ✅ **Evidencias subidas** para cada criterio crítico
3. ✅ **Validación automática** sin errores
4. ✅ **Acta firmada digitalmente** generada
5. ✅ **Respaldo completo** antes del lanzamiento

**Solo entonces se puede afirmar:**

> 🔒 **"TenancingoLive está CERTIFICADO AL 100% para lanzamiento público"**

---

*Sistema integral de certificación con trazabilidad completa* 🔒