CREATE DATABASE IF NOT EXISTS aire_db;
USE aire_db;

CREATE TABLE stazioni (
    id_amat INT PRIMARY KEY,
    nome VARCHAR(100),
    id_arpa VARCHAR(20),
    inizio_operativita DATE,
    fine_operativita DATE,
    longitudine DECIMAL(10,7),
    latitudine DECIMAL(10,7)
);


CREATE TABLE inquinanti (
    id_inquinante INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) UNIQUE
);

CREATE TABLE stazioni_inquinanti (
    id_amat INT,
    id_inquinante INT,
    PRIMARY KEY (id_amat, id_inquinante),
    FOREIGN KEY (id_amat) REFERENCES stazioni(id_amat),
    FOREIGN KEY (id_inquinante) REFERENCES inquinanti(id_inquinante)
);

CREATE TABLE misurazioni (
    id_misurazione INT AUTO_INCREMENT PRIMARY KEY,
    stazione_id INT,
    data DATE,
    inquinante_id INT,
    valore DECIMAL(10,2),
    FOREIGN KEY (stazione_id) REFERENCES stazioni(id_amat),
    FOREIGN KEY (inquinante_id) REFERENCES inquinanti(id_inquinante)
);

-- Import tabelle dati puliti
SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE 'C:/Users/mario/Desktop/GenerationVisual/stazioni_mysql.csv'
INTO TABLE stazioni
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_amat, nome, id_arpa, inizio_operativita, fine_operativita, longitudine, latitudine);


LOAD DATA LOCAL INFILE 'C:/Users/mario/Desktop/GenerationVisual/inquinanti_mysql.csv'
INTO TABLE inquinanti
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_inquinante, nome);


LOAD DATA LOCAL INFILE 'C:/Users/mario/Desktop/GenerationVisual/stazioni_inquinanti_mysql.csv'
INTO TABLE stazioni_inquinanti
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_amat, id_inquinante);


LOAD DATA LOCAL INFILE 'C:/Users/mario/Desktop/GenerationVisual/misurazioni_mysql.csv'
INTO TABLE misurazioni
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(stazione_id, data, inquinante_id, valore);



-- QUERY DI PROVA
SELECT *
FROM misurazioni
WHERE stazione_id = 2
ORDER BY data;

SELECT *
FROM misurazioni
WHERE stazione_id = 2
ORDER BY data;

SELECT *
FROM misurazioni
WHERE data BETWEEN '2025-11-01' AND '2025-11-30'
ORDER BY data;

