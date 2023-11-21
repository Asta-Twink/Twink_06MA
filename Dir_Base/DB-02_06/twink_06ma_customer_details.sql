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
-- Table structure for table `customer_details`
--

DROP TABLE IF EXISTS `customer_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_details` (
  `UID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Company_Name` varchar(500) DEFAULT NULL,
  `GSTIN` varchar(30) DEFAULT NULL,
  `Company_Address` varchar(500) DEFAULT NULL,
  `Phone_No` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_details`
--

LOCK TABLES `customer_details` WRITE;
/*!40000 ALTER TABLE `customer_details` DISABLE KEYS */;
INSERT INTO `customer_details` VALUES (1,'Lakshmi Life Science private limited unit 1','33AAACQ1986A1ZS','SF NO. 113/2 Annur Road,\nArasur Village,Sulur Taluk,\nCoimbatore 641407','04227108600'),(2,'Kumaraguru College of Technology','33AAATR3640M1ZG','Chinavedampatty, \nCoimbatore 641049',' '),(3,'Shree Harie Steel & Alloys Unit I','33AAZFS6274P1Z1','461/1A Kerakavundam Palayam,\nAnnur(PO), Coimbatore 641697',' '),(4,'Shree Harie Steels & Alloys Unit II','33AAZFS6274P1Z1','494/1, Peranaicken Pudur Road,\nPuliampatti, Erode 638459',' '),(5,'THE MALABAR CO-OPERATIVE TEXTILES LIMITED','32AACAT0124H1Z3','Karthala Chungam, Athavanad Post,\nKuttipuram via, Mallapuram Dist\nKerala 676310','0494 2608832'),(7,'SUSIN TECHNOLOGIES [P] LTD','33AALCS8975Q1Z7','NO, 43A12 Vadakku thottom pakuthi, idikari,coimbatore - 641022',' '),(8,'PSG College of Technology','aaa','Peelamedu, \nCoimbatore 641004','422 2572177'),(9,'TAMIL NADU AGRICULTURAL UNIVERSITY','//','Department of food process engineering\ncoimbatore - 641003','0422-6611272'),(10,'Shree guhan patters And Castings','33AECFS8424E1Z7','Sf  No406/2 masaranakovil\nnear sanjeevani hospital\nAnnur - 641653','9566673314'),(11,'SHRILL ENGINEERS','33ABSPN5107E1ZR','no 31 premier industrial eastate \navarampalyam road kr puram\ncoimbatore 6','0422-2568433'),(12,'MSV ENTERPRISES','33ALVPY7788D1Z3','39, PARK STREET\nKATTOOR\nCOIMBATORE-641009','9791716251'),(14,'Lakshmi Life Sciences Private Limited,Unit-II','33AAACQ1986A1ZS','3/245,Sulur Railway Feeder Road\nMuthugoundenpudur (PO)\nCoimbatore-641406,Tamilnadu,India','      '),(15,'ELGI ULTRA PRIVATE LIMITED(POLYTEX)','33AEECE8310N1ZL','Avinasi Road,Arasur post\nThennampalayam,Coimbatore-641407','9791901267'),(16,'ROOTS INDUSTRIES INDIA LTD','33AABCR0314E1Z6','R.K.G INDUSTRIAL ESTATE\nGANAPATHY\nCOIMBATORE-641006','7373883385'),(17,'LAKSHMI PRECISION TECHNOLOGIES LIMITED','33AAACL3522H1ZZ','ARASUR \nCOIMBATORE -641407','04226173500');
/*!40000 ALTER TABLE `customer_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-02 21:20:51
