CREATE DATABASE IF NOT EXISTS filmes_series;

USE filmes_series;


CREATE TABLE IF NOT EXISTS series (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tvmaze_id INT NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    tipo VARCHAR(50),
    idioma VARCHAR(50),
    estado VARCHAR(50),
    data_estreia DATE NULL,
    data_fim DATE NULL,
    duracao INT NULL,
    classificacao DECIMAL(3,1) NULL,
    canal VARCHAR(100) NULL,
    resumo TEXT NULL,
    imagem VARCHAR(500) NULL
);


CREATE TABLE IF NOT EXISTS generos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS series_generos (
    serie_id INT NOT NULL,
    genero_id INT NOT NULL,

    PRIMARY KEY (serie_id, genero_id),

    FOREIGN KEY (serie_id)
        REFERENCES series(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (genero_id)
        REFERENCES generos(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);