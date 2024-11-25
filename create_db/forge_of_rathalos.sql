-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Creato il: Nov 25, 2024 alle 19:54
-- Versione del server: 5.7.24
-- Versione PHP: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `forge_of_rathalos`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `category` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `categories`
--

INSERT INTO `categories` (`category_id`, `category`) VALUES
(1, 'Armor'),
(2, 'Weapons'),
(3, 'Accessories'),
(4, 'Pre-Order'),
(5, 'Dog Armor');

-- --------------------------------------------------------

--
-- Struttura della tabella `favorites`
--

CREATE TABLE `favorites` (
  `favorite_id` int(11) NOT NULL,
  `insertion_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `images`
--

CREATE TABLE `images` (
  `image_id` int(11) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `insertion_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `images`
--

INSERT INTO `images` (`image_id`, `image_url`, `insertion_id`) VALUES
(1, 'article.webp', 1),
(2, 'article2.avif', 2),
(5, 'article3.webp', 5),
(6, 'il_794xN.5098286497_24qs.avif', 6),
(7, 'alb.avif', 7),
(8, 'goblin.webp', 8);

-- --------------------------------------------------------

--
-- Struttura della tabella `insertions`
--

CREATE TABLE `insertions` (
  `insertion_id` int(11) NOT NULL,
  `item` varchar(255) DEFAULT NULL,
  `description` text,
  `price` float(7,2) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `insertions`
--

INSERT INTO `insertions` (`insertion_id`, `item`, `description`, `price`, `quantity`, `category_id`) VALUES
(1, 'Saiyan Suit Sailor', 'Attenzione: questo è un articolo per cosplay, non è una replica fedele, e non ha le stesse funzioni del prodotto originale, ovvero non vola, non spara laser e non ha poteri magici.\r\nE un prodotto realizzato su misura e dunque non può essere reso, ma per qualsiasi problema siamo a disposizione per aiutarvi a risolvere qualsiasi problema\r\n\r\nProgetto Mashup nato dall\'idea di unire la Saiyan suit di Dragon Ball con le Guerriere Sailor\r\nRealizzato in evafoam100\r\n\r\nRivestito con FullDip ( vinile Spray )\r\n\r\nDipinto con colori acrilici professionali\r\n\r\nSe avete altre idee di progetti Mashup saremo molto felici di realizzarli!\r\n\r\n', 500.00, 10, 1),
(2, 'Iron Man Armor', 'Attenzione: questo è un articolo per cosplay, non è una replica fedele, e non ha le stesse funzioni del prodotto originale, ovvero non vola, non spara laser e non ha poteri magici.\r\nE un prodotto realizzato su misura e dunque non può essere reso, ma per qualsiasi problema siamo a disposizione per aiutarvi a risolvere qualsiasi problema.\r\n\r\nArmatura ispirato a Ironman Mark\r\n\r\nNO elmo NO guanti\r\n\r\nRealizzato interamente in EvaFoam100 professionale Polypros e rivestito in venile Fulldip\r\n\r\nColori elastici e resistenti\r\n\r\nRealizzato su misura, ma solo taglia S o M\r\n\r\nCon led nel torace\r\n\r\nSe volete alte versioni di Ironman contattateci pure', 800.00, 5, 1),
(5, 'Kayn Sickle', 'Attenzione: questo è un articolo per cosplay, non è una replica fedele, e non ha le stesse funzioni del prodotto originale, ovvero non vola, non spara laser e non ha poteri magici.\r\nE un prodotto realizzato su misura e dunque non può essere reso, ma per qualsiasi problema siamo a disposizione per aiutarvi a risolvere qualsiasi problema\r\n\r\nIspirato alla falce di Kayn di LoL\r\n\r\nRealizzato in foam professionale, e rivestito con plastidip\r\n\r\nVerniciato con l\'aerografo con colori professionali\r\n\r\nColori elastici e impermeabili\r\n\r\nSe volete personalizzazioni sul colore o altre armi di LOL contattateci pure', 500.00, 5, 2),
(6, 'Master Chief Armor ( with led helmet, no rifle )', 'Attenzione: questo è un articolo per cosplay, non è una replica fedele, e non ha le stesse funzioni del prodotto originale, ovvero non vola, non spara laser e non ha poteri magici.\r\nE un prodotto realizzato su misura e dunque non può essere reso, ma per qualsiasi problema siamo a disposizione per aiutarvi a risolvere qualsiasi problema\r\n\r\nArmatura ispirato all\'armatura di Master Chief del gioco Pc e Xbox Halo\r\n\r\nwith led helmet\r\n\r\nno rifle\r\n\r\nRealizzato interamente in Evafoam100 e rivestito in venile Fulldip\r\n\r\ncolori elastici e resistenti\r\n\r\nrealizzato su misura\r\n\r\nse volete alte versioni contattateci pure\r\n\r\n', 1200.00, 5, 1),
(7, 'Albedo Armor (Upgrade 2023)', 'Armatura di Attenzione: questo è un articolo per cosplay, non è una replica fedele, e non ha le stesse funzioni del prodotto originale, ovvero non vola, non spara laser e non ha poteri magici.\r\nE un prodotto realizzato su misura e dunque non può essere reso, ma per qualsiasi problema siamo a disposizione per aiutarvi a risolvere qualsiasi problema.\r\n\r\nArmatura ispirata a quella di Albedo dall\'anime Overlord\r\n\r\nrealizzato in Evafoam100 professionale, e rivestito con plastidip\r\n\r\ncolori estremamente elastici\r\n\r\ntutti i pezzi sono agganciati tra loro tramite cinghie in cuoio, velcro e elastici\r\n\r\nrealizzato su misura\r\n\r\nil set comprende tutta l\'armatura, compreso elmo, copri stivali e ascia', 900.00, 5, 1),
(8, 'Slayer Full Armor Set', 'Attenzione: questo è un articolo per cosplay, non è una replica fedele, e non ha le stesse funzioni del prodotto originale, ovvero non vola, non spara laser e non ha poteri magici.\r\nE un prodotto realizzato su misura e dunque non può essere reso, ma per qualsiasi problema siamo a disposizione per aiutarvi a risolvere qualsiasi problema.\r\n\r\nQuesta è un armatura ispirata a quella dell\'anime Goblin Slayer!\r\n\r\nAttacchi in vero cuoio Made in Italy\r\n\r\nInteramente realizzato in foam Prolyprops\r\n\r\nRivestito con Fulldip\r\n\r\nColori resistenti e elastici\r\n\r\nIl set comprende:\r\n\r\nArmatura completa\r\n\r\nElmo\r\n\r\nSpada\r\n\r\nScudo\r\n\r\npugnali x4\r\n\r\nPer qualsiasi informazione contattateci pure!\r\n\r\nse avete bisogno anche della parte sartoriale vi metterò in contatto con la nostra sarta per un preventivo', 700.00, 5, 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `reviews`
--

CREATE TABLE `reviews` (
  `review_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `text` text,
  `rank` float DEFAULT NULL,
  `insertion_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `name` varchar(150) DEFAULT NULL,
  `surname` varchar(150) DEFAULT NULL,
  `password` text,
  `email` varchar(200) DEFAULT NULL,
  `admin` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `users`
--

INSERT INTO `users` (`user_id`, `name`, `surname`, `password`, `email`, `admin`) VALUES
(1, 'Admin', 'Admin', '$2b$12$ynViBczQfI/xJSBob/KEc.KZhIPZuL5HuGtT19hXhJmOLOju.Xwxe', 'superadmin@for.com', 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `variants`
--

CREATE TABLE `variants` (
  `variant_id` int(11) NOT NULL,
  `variant` varchar(50) DEFAULT NULL,
  `variant_price` float(7,2) DEFAULT NULL,
  `insertion_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `variants`
--

INSERT INTO `variants` (`variant_id`, `variant`, `variant_price`, `insertion_id`) VALUES
(7, 'Gold Paint', 10.00, 1),
(11, 'led', 0.00, 7),
(12, 'silver paint', 0.00, 1),
(13, 'led', 100.00, 2),
(14, 'Shield', 199.99, 8);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indici per le tabelle `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`favorite_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `insertion_id` (`insertion_id`);

--
-- Indici per le tabelle `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `insertion_id` (`insertion_id`);

--
-- Indici per le tabelle `insertions`
--
ALTER TABLE `insertions`
  ADD PRIMARY KEY (`insertion_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indici per le tabelle `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`review_id`),
  ADD KEY `insertion_id` (`insertion_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indici per le tabelle `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indici per le tabelle `variants`
--
ALTER TABLE `variants`
  ADD PRIMARY KEY (`variant_id`),
  ADD KEY `insertion_id` (`insertion_id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT per la tabella `favorites`
--
ALTER TABLE `favorites`
  MODIFY `favorite_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `images`
--
ALTER TABLE `images`
  MODIFY `image_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT per la tabella `insertions`
--
ALTER TABLE `insertions`
  MODIFY `insertion_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT per la tabella `reviews`
--
ALTER TABLE `reviews`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT per la tabella `variants`
--
ALTER TABLE `variants`
  MODIFY `variant_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`insertion_id`) REFERENCES `insertions` (`insertion_id`) ON DELETE CASCADE;

--
-- Limiti per la tabella `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`insertion_id`) REFERENCES `insertions` (`insertion_id`) ON DELETE CASCADE;

--
-- Limiti per la tabella `insertions`
--
ALTER TABLE `insertions`
  ADD CONSTRAINT `insertions_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`);

--
-- Limiti per la tabella `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`insertion_id`) REFERENCES `insertions` (`insertion_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;

--
-- Limiti per la tabella `variants`
--
ALTER TABLE `variants`
  ADD CONSTRAINT `variants_ibfk_1` FOREIGN KEY (`insertion_id`) REFERENCES `insertions` (`insertion_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
