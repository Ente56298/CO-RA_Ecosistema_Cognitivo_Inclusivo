<?php
/**
 * Panel de Certificación Integral - TenancingoLive
 */

require_once '../config/config.php';

$etapas = [
    'tecnica' => [
        'nombre' => '📋 Certificación Técnica',
        'items' => [
            'ssl_valido' => ['nombre' => 'SSL activo', 'critico' => true],
            'navegacion_multi' => ['nombre' => 'Navegación móvil/desktop', 'critico' => true],
            'formularios_ok' => ['nombre' => 'Formularios operativos', 'critico' => true],
            'rendimiento_3s' => ['nombre' => 'Carga < 3s', 'critico' => true],
            'prueba_estres' => ['nombre' => 'Prueba 50+ usuarios', 'critico' => true]
        ]
    ],
    'seguridad' => [
        'nombre' => '🛡️ Certificación Seguridad',
        'items' => [
            'admin_protegido' => ['nombre' => 'Admin protegido', 'critico' => true],
            'headers_seguridad' => ['nombre' => 'Headers seguridad', 'critico' => true],
            'anti_inyecciones' => ['nombre' => 'Anti XSS/SQL', 'critico' => true]
        ]
    ],
    'contenido' => [
        'nombre' => '🗂️ Certificación Contenido',
        'items' => [
            'textos_reales' => ['nombre' => 'Sin lorem ipsum', 'critico' => true],
            'eventos_actualizados' => ['nombre' => 'Fechas correctas', 'critico' => true],
            'paginas_legales' => ['nombre' => 'Privacidad/términos', 'critico' => true]
        ]
    ]
];

// Calcular progreso
$total = 0;
$completados = 0;
foreach ($etapas as $etapa) {
    foreach ($etapa['items'] as $item_id => $item) {
        $total++;
        if (isset($_COOKIE["cert_$item_id"])) $completados++;
    }
}
$progreso = $total > 0 ? round(($completados / $total) * 100) : 0;
$certificado = ($progreso === 100);
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Certificación - TenancingoLive</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { text-align: center; margin-bottom: 30px; }
        .progress { width: 100%; height: 30px; background: #e9ecef; border-radius: 15px; overflow: hidden; margin: 20px 0; }
        .progress-bar { height: 100%; background: <?= $certificado ? '#28a745' : '#007bff' ?>; transition: width 0.3s; }
        .etapa { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .item { margin: 10px 0; padding: 10px; border-left: 3px solid #ddd; }
        .item.critico { border-left-color: #dc3545; }
        .item.completado { background: #d4edda; border-left-color: #28a745; }
        .btn { padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        .btn.success { background: #28a745; }
        .certificado { background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 30px; text-align: center; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Sistema de Certificación TenancingoLive</h1>
            <p><strong>Progreso:</strong> <?= $progreso ?>% (<?= $completados ?>/<?= $total ?>)</p>
            <div class="progress">
                <div class="progress-bar" style="width: <?= $progreso ?>%"></div>
            </div>
        </div>

        <?php if ($certificado): ?>
        <div class="certificado">
            <h2>🎉 ¡CERTIFICACIÓN COMPLETADA!</h2>
            <p>TenancingoLive está listo para lanzamiento público</p>
            <button class="btn success" onclick="generarActa()">📋 Generar Acta</button>
        </div>
        <?php endif; ?>

        <?php foreach ($etapas as $etapa_id => $etapa): ?>
        <div class="etapa">
            <h3><?= $etapa['nombre'] ?></h3>
            <?php foreach ($etapa['items'] as $item_id => $item): ?>
            <?php $completado = isset($_COOKIE["cert_$item_id"]); ?>
            <div class="item <?= $item['critico'] ? 'critico' : '' ?> <?= $completado ? 'completado' : '' ?>">
                <label>
                    <input type="checkbox" <?= $completado ? 'checked' : '' ?> 
                           onchange="toggleItem('<?= $item_id ?>', this.checked)">
                    <?= $item['nombre'] ?>
                    <?= $item['critico'] ? '<span style="color: red; font-weight: bold;"> [CRÍTICO]</span>' : '' ?>
                </label>
                <button class="btn" onclick="subirEvidencia('<?= $item_id ?>')">📎 Evidencia</button>
            </div>
            <?php endforeach; ?>
        </div>
        <?php endforeach; ?>
    </div>

    <script>
        function toggleItem(itemId, checked) {
            if (checked) {
                document.cookie = `cert_${itemId}=1; path=/; max-age=86400`;
            } else {
                document.cookie = `cert_${itemId}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
            }
            setTimeout(() => location.reload(), 100);
        }

        function subirEvidencia(itemId) {
            alert(`Subir evidencia para: ${itemId}`);
        }

        function generarActa() {
            alert('Generando Acta de Certificación...');
            window.open('acta_certificacion.pdf', '_blank');
        }
    </script>
</body>
</html>