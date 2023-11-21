-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: twink_06ma
-- ------------------------------------------------------
-- Server version	5.6.51-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `wage_db_push`
--

DROP TABLE IF EXISTS `wage_db_push`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wage_db_push` (
  `wage_type` varchar(45) NOT NULL,
  `g_date` varchar(45) DEFAULT NULL,
  `mm_yyyy` varchar(20) NOT NULL,
  `EmpCode` varchar(100) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `F_S_Name` varchar(100) DEFAULT NULL,
  `Team` varchar(100) DEFAULT NULL,
  `Days_Present` varchar(10) DEFAULT NULL,
  `S1` varchar(100) DEFAULT NULL,
  `S2` varchar(100) DEFAULT NULL,
  `S3` varchar(100) DEFAULT NULL,
  `PD_Wage` varchar(100) DEFAULT NULL,
  `Wage` float DEFAULT NULL,
  `OT` float DEFAULT NULL,
  `OT_Wages` float DEFAULT NULL,
  `Incentive` float DEFAULT NULL,
  `Gross_Wages` float DEFAULT NULL,
  `PF` float DEFAULT NULL,
  `ESI` float DEFAULT NULL,
  `Adv` float DEFAULT NULL,
  `Canteen` float DEFAULT NULL,
  `Net_Wages` float DEFAULT NULL,
  PRIMARY KEY (`wage_type`,`mm_yyyy`,`EmpCode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wage_db_push`
--

LOCK TABLES `wage_db_push` WRITE;
/*!40000 ALTER TABLE `wage_db_push` DISABLE KEYS */;
/*!40000 ALTER TABLE `wage_db_push` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-02 21:20:52
