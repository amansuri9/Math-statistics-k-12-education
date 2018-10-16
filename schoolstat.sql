-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 27, 2018 at 12:55 PM
-- Server version: 5.7.22-0ubuntu0.16.04.1
-- PHP Version: 7.0.28-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `schoolstat`
--
CREATE DATABASE IF NOT EXISTS schoolstat;


/* Make a database user called schoolstat. */
GRANT SELECT, UPDATE on schoolstat to 'schoolstat'@'localhost';
USE schoolstat;
-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` text NOT NULL,
  `current_file` text NOT NULL,
  `last_login` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `current_file`, `last_login`) VALUES
(1, 'test', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', 'newdata2018-04-0116-32-50.csv', '2018-04-08 01:16:03'),
(2, 'cristian', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', '', '2018-04-04 21:10:35'),
(3, 'kim', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', '', '2018-04-04 21:10:35'),
(4, 'ari', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', '', '2018-04-04 21:10:35'),
(5, 'ryan', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', '', '2018-04-04 21:10:35'),
(6, 'sam', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', '', '2018-04-04 21:10:35'),
(7, 'jhaines', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', '', '2018-04-04 21:10:35');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
