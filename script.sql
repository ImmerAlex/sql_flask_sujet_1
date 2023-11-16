DROP TABLE IF EXISTS departement;
DROP TABLE IF EXISTS employe;

CREATE TABLE departement (
    id_departement INT AUTO_INCREMENT,
    nomDepartement VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_departement)
);

CREATE TABLE employe (
    id_employe INT AUTO_INCREMENT PRIMARY KEY,
    nom_employe VARCHAR(50) NOT NULL,
    ville_dept VARCHAR(50) NOT NULL,
    date_embauche DATE NOT NULL,
    indice INT NOT NULL,
    salaire INT NOT NULL,
    photo VARCHAR(50) NOT NULL,
    departement_id INT,
    FOREIGN KEY (departement_id) REFERENCES departement(id_departement)  ON DELETE NO ACTION
);


INSERT INTO departement (id_departement, nomDepartement) 
VALUES
(NULL, 'Production'),
(NULL, 'Marketing'),
(NULL, 'Méthode'),
(NULL, 'Recherche et développement');


INSERT INTO employe(id_employe,nom_employe,ville_dept,date_embauche,indice,salaire, photo, departement_id) VALUES
    (NULL,'Gauthier', 'Belfort', '2011-09-06', 395, 2500 ,'employe1.png', 2),
    (NULL,'Peslier', 'Valdois', '2009-02-01', 375, 2800 ,'employe2.png', 1),
    (NULL,'Rousselet', 'Savoyeux', '2010-05-15', 295, 2000 ,'employe3.png', 3),
    (NULL,'Perez', 'Besançon', '2009-02-01', 255, 1500 ,'employe4.png', 1),
    (NULL,'Benatti', 'Pont-de-Planches', '2011-09-06', 285, 1900 ,'employe5.png', 3),
    (NULL,'Thiebaud', 'Frotey', '2011-09-06', 295, 2000,'employe6.png', 1),
    (NULL,'Gauthier', 'Valdoie', '2007-04-02', 285, 1900 ,'employe7.png', 3),
    (NULL,'Lambert', 'Belfort', '2012-03-01', 345, 2200 ,'employe8.png', 2),
    (NULL,'Dupond', 'Besancon', '2011-02-04', 275, 1800 ,'employe9.png', 1),
    (NULL,'Durand', 'Vesoul', '2011-02-04', 205, 1200 ,'no_photo.jpg', 1),
    (NULL,'Lapierre', 'Valdoie', '2012-07-25', 295, 2000 ,'employe10.png', 1),
    (NULL,'Philippe', 'Belfort', '2011-03-21', 345, 2200 ,'employe11.png', 2);