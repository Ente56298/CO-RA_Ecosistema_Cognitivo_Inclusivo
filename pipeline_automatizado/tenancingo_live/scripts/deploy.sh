#!/bin/bash
# Script de despliegue FTP para TenancingoLive

set -e

FTP_HOST="ftpupload.net"
FTP_USER="b17_38301772"
FTP_PASS="${FTP_PASSWORD:-tu_password_ftp}"
REMOTE_DIR="/htdocs"

echo "🚀 Desplegando TenancingoLive..."

# Crear comandos FTP
cat > ftp_commands.txt << EOF
open $FTP_HOST
user $FTP_USER $FTP_PASS
binary
cd $REMOTE_DIR
put config/config.php config.php
put webhook_pago.php webhook_pago.php
put watch.php watch.php
quit
EOF

# Ejecutar FTP
ftp -n < ftp_commands.txt
rm ftp_commands.txt

echo "✅ Despliegue completado"
echo "🌐 https://tenancingo.byethost17.com"