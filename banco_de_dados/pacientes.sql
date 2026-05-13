USE hospital_db;


CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE
);