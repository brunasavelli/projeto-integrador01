CREATE DATABASE hospital_db;
USE hospital_db;

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100) NOT NULL
);

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE chamados (
    id_chamado INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,

    descricao TEXT NOT NULL,
    urgencia INT NOT NULL,
    prioridade VARCHAR(10),
    
    status VARCHAR(20) DEFAULT 'Em Espera',
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);

INSERT INTO medicos VALUES (1000, 'Fábio Silva', 'Cardiologia');

INSERT INTO pacientes VALUES (2000, 'Maria Oliveira', '1985-07-15', '11987654321', 'maria.oliveira@email.com');

INSERT INTO chamados (id_chamado, id_paciente, id_medico, descricao, urgencia, prioridade, status, data_abertura) VALUES 
(3000, 2000, 1000, 'Paciente apresenta sintomas de dor no peito e falta de ar.', 5, 'Alta', 'Em Espera', CURRENT_TIMESTAMP);
