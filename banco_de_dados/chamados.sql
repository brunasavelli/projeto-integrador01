USE hospital_db;

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