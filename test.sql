-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 01, 2019 at 02:45 PM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`` PROCEDURE `AddGeometryColumn` (`catalog` VARCHAR(64), `t_schema` VARCHAR(64), `t_name` VARCHAR(64), `geometry_column` VARCHAR(64), `t_srid` INT)  begin
  set @qwe= concat('ALTER TABLE ', t_schema, '.', t_name, ' ADD ', geometry_column,' GEOMETRY REF_SYSTEM_ID=', t_srid); PREPARE ls from @qwe; execute ls; deallocate prepare ls; end$$

CREATE DEFINER=`` PROCEDURE `DropGeometryColumn` (`catalog` VARCHAR(64), `t_schema` VARCHAR(64), `t_name` VARCHAR(64), `geometry_column` VARCHAR(64))  begin
  set @qwe= concat('ALTER TABLE ', t_schema, '.', t_name, ' DROP ', geometry_column); PREPARE ls from @qwe; execute ls; deallocate prepare ls; end$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `number` int(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`id`, `name`, `email`, `number`, `city`, `password`) VALUES
(9, 'sulabh', 'sulabh@gmail.com', 2147483647, 'saab', '7eab8a78aa430f921da0f9ac5ba324b1aca4d3cb221ead23c9bb79f6cea5f2eb'),
(10, 'abhilash', 'abhilasj@gmail.com', 566549674, 'saab', 'f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b'),
(11, 'Johny', 'johny@gmail.com', 857585758, 'saab', '2b1b370c3baa4ad73cc84d40740834901e691ad9c718246aaa9953da488d99bf'),
(13, 'Ishendra', 'ishendrapratap@gmail.com', 854123697, 'volvo', '4058e0beba03b9f281ecd7272094a801cf2d8dd165644d4ea67148c1b52bb0ae'),
(14, 'Raghav', 'raghav@gmail.com', 2147483647, 'volvo', 'cd16a2d9bb256dfbb5456c3e49613d20f13ec509b344bd2da1475551969d018b'),
(15, 'Sanjay', 'sanjay@gmail.com', 2147483647, 'volvo', '021fb044d1c216bc015a04fce9067ffb109253369c8c0a82ffe5941aa4ed7fa7'),
(16, 'sapna', 'sapna@gmail.com', 6879797, 'volvo', 'bc9f2d2d1015ff656536b14d71414a8225392bc0946a3f07f5d93f5b33b4f312');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `registration`
--
ALTER TABLE `registration`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
