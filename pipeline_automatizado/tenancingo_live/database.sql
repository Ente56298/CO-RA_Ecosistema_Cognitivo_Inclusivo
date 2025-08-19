-- Base de datos TenancingoLive
-- Tablas necesarias para el sistema completo

-- Tabla de eventos
CREATE TABLE IF NOT EXISTS events (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    duration_minutes INT DEFAULT 120,
    price_mxn DECIMAL(10,2) NOT NULL,
    stream_key VARCHAR(100) UNIQUE NOT NULL,
    trailer_url VARCHAR(500),
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de tokens de acceso
CREATE TABLE IF NOT EXISTS access_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token TEXT NOT NULL,
    email VARCHAR(255) NOT NULL,
    event_id VARCHAR(50) NOT NULL,
    payment_id VARCHAR(100),
    amount DECIMAL(10,2),
    expires_at DATETIME NOT NULL,
    used_at DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    INDEX idx_token_event (event_id),
    INDEX idx_token_email (email),
    INDEX idx_token_expires (expires_at)
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(255),
    phone VARCHAR(20),
    verified BOOLEAN DEFAULT 0,
    verification_token VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de log de actividad
CREATE TABLE IF NOT EXISTS activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    details JSON,
    ip_address VARCHAR(45),
    user_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_action (action),
    INDEX idx_created (created_at)
);

-- Tabla de streams activos
CREATE TABLE IF NOT EXISTS active_streams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(50) NOT NULL,
    stream_key VARCHAR(100) NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    viewer_count INT DEFAULT 0,
    status ENUM('starting', 'live', 'ended') DEFAULT 'starting',
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    INDEX idx_stream_key (stream_key),
    INDEX idx_status (status)
);

-- Insertar evento de ejemplo
INSERT IGNORE INTO events (id, title, description, start_time, price_mxn, stream_key) VALUES 
('2025-08-22-lucha1', 'Gran Cartelera Tenancingo', 'Evento piloto de lucha libre', '2025-08-22 20:00:00', 79.00, 'lucha1_live');

-- Crear usuario admin por defecto
INSERT IGNORE INTO users (email, password_hash, name, verified) VALUES 
('admin@tenancingo.live', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Administrador', 1);