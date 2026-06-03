USE hospital_db;

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    crm VARCHAR(10) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100) NOT NULL
);