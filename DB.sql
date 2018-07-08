-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               10.1.19-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for rat
CREATE DATABASE IF NOT EXISTS `rat` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `rat`;

-- Dumping structure for table rat.clients
CREATE TABLE IF NOT EXISTS `clients` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'DataBase Client ID',
  `Connected` int(11) DEFAULT '0' COMMENT 'Client Connection State Bool',
  `UUID` varchar(30) DEFAULT NULL COMMENT 'Unique Client Random ID',
  `Name` varchar(50) DEFAULT NULL COMMENT 'PC Client Name',
  `Info` text,
  `CMD` varchar(9999) DEFAULT '{''Status'': 0, ''Command'': ''cd''}' COMMENT 'User Command & Execution State',
  `CMDOutput` mediumtext COMMENT 'Client Response',
  `Last Connection` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Time Last Connection',
  `Time Added` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Time First Connection',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `UUID` (`UUID`)
) ENGINE=InnoDB AUTO_INCREMENT=208 DEFAULT CHARSET=latin1;

-- Dumping data for table rat.clients: ~2 rows (approximately)
DELETE FROM `clients`;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;

-- Dumping structure for table rat.panel
CREATE TABLE IF NOT EXISTS `panel` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(50) DEFAULT NULL,
  `Password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Dumping data for table rat.panel: ~0 rows (approximately)
DELETE FROM `panel`;
/*!40000 ALTER TABLE `panel` DISABLE KEYS */;
INSERT INTO `panel` (`ID`, `UserName`, `Password`) VALUES
	(1, 'TEST', '12345678');
/*!40000 ALTER TABLE `panel` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
