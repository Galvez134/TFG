-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: baseDeDatosTFG
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

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
-- Table structure for table `Projects`
--

DROP TABLE IF EXISTS `Projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Projects` (
  `Project_id` varchar(60) NOT NULL,
  `Username` varchar(45) NOT NULL,
  `ProjectName` varchar(45) NOT NULL,
  `Nodes` longtext,
  `Links` longtext,
  PRIMARY KEY (`Project_id`),
  UNIQUE KEY `Project_id_UNIQUE` (`Project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Projects`
--

LOCK TABLES `Projects` WRITE;
/*!40000 ALTER TABLE `Projects` DISABLE KEYS */;
INSERT INTO `Projects` VALUES ('5826b740-7820-41fd-8005-cddc24976906','Manuel Gálvez Gómez','a','[{\'name\': \'EMPIRICAL-RESEARCH\'}, {\'name\': \'STRATEGY-AND-MOTIVATION\'}, {\'name\': \'TEACHERS-DEEP-LEARNING\'}, {\'name\': \'TEACHERS-GENDER\'}, {\'name\': \'STUDENTS\'}, {\'name\': \'ACHIEVEMENT\'}, {\'name\': \'PERFORMANCE\'}, {\'name\': \'LEADERSHIP\'}, {\'name\': \'PROGRAMS\'}, {\'name\': \'SCIENCE\'}, {\'name\': \'QUALITY\'}, {\'name\': \'A\'}, {\'name\': \'B\'}, {\'name\': \'C\'}, {\'name\': \'D\'}, {\'name\': \'E\'}]','[{\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'STRATEGY-AND-MOTIVATION\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'TEACHERS-DEEP-LEARNING\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'TEACHERS-GENDER\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'STUDENTS\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'ACHIEVEMENT\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'PERFORMANCE\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'LEADERSHIP\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'PROGRAMS\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'TEACHERS-DEEP-LEARNING\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'TEACHERS-GENDER\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'STUDENTS\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'ACHIEVEMENT\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'PERFORMANCE\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'LEADERSHIP\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'PROGRAMS\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'TEACHERS-GENDER\', \'count\': 2}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'STUDENTS\', \'count\': 2}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'ACHIEVEMENT\', \'count\': 2}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'PERFORMANCE\', \'count\': 2}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'LEADERSHIP\', \'count\': 2}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'PROGRAMS\', \'count\': 2}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'TEACHERS-GENDER\', \'target\': \'STUDENTS\', \'count\': 2}, {\'source\': \'TEACHERS-GENDER\', \'target\': \'ACHIEVEMENT\', \'count\': 2}, {\'source\': \'TEACHERS-GENDER\', \'target\': \'PERFORMANCE\', \'count\': 2}, {\'source\': \'TEACHERS-GENDER\', \'target\': \'LEADERSHIP\', \'count\': 2}, {\'source\': \'TEACHERS-GENDER\', \'target\': \'PROGRAMS\', \'count\': 2}, {\'source\': \'TEACHERS-GENDER\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'TEACHERS-GENDER\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'STUDENTS\', \'target\': \'ACHIEVEMENT\', \'count\': 2}, {\'source\': \'STUDENTS\', \'target\': \'PERFORMANCE\', \'count\': 2}, {\'source\': \'STUDENTS\', \'target\': \'LEADERSHIP\', \'count\': 2}, {\'source\': \'STUDENTS\', \'target\': \'PROGRAMS\', \'count\': 2}, {\'source\': \'STUDENTS\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'STUDENTS\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'ACHIEVEMENT\', \'target\': \'PERFORMANCE\', \'count\': 2}, {\'source\': \'ACHIEVEMENT\', \'target\': \'LEADERSHIP\', \'count\': 2}, {\'source\': \'ACHIEVEMENT\', \'target\': \'PROGRAMS\', \'count\': 2}, {\'source\': \'ACHIEVEMENT\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'ACHIEVEMENT\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'PERFORMANCE\', \'target\': \'LEADERSHIP\', \'count\': 2}, {\'source\': \'PERFORMANCE\', \'target\': \'PROGRAMS\', \'count\': 2}, {\'source\': \'PERFORMANCE\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'PERFORMANCE\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'LEADERSHIP\', \'target\': \'PROGRAMS\', \'count\': 2}, {\'source\': \'LEADERSHIP\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'LEADERSHIP\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'PROGRAMS\', \'target\': \'SCIENCE\', \'count\': 2}, {\'source\': \'PROGRAMS\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'SCIENCE\', \'target\': \'QUALITY\', \'count\': 2}, {\'source\': \'EMPIRICAL-RESEARCH\', \'target\': \'A\', \'count\': 1}, {\'source\': \'STRATEGY-AND-MOTIVATION\', \'target\': \'A\', \'count\': 1}, {\'source\': \'TEACHERS-DEEP-LEARNING\', \'target\': \'A\', \'count\': 1}, {\'source\': \'TEACHERS-GENDER\', \'target\': \'A\', \'count\': 1}, {\'source\': \'STUDENTS\', \'target\': \'A\', \'count\': 1}, {\'source\': \'ACHIEVEMENT\', \'target\': \'A\', \'count\': 1}, {\'source\': \'PERFORMANCE\', \'target\': \'A\', \'count\': 1}, {\'source\': \'LEADERSHIP\', \'target\': \'A\', \'count\': 1}, {\'source\': \'PROGRAMS\', \'target\': \'A\', \'count\': 1}, {\'source\': \'SCIENCE\', \'target\': \'A\', \'count\': 1}, {\'source\': \'QUALITY\', \'target\': \'A\', \'count\': 1}, {\'source\': \'A\', \'target\': \'B\', \'count\': 2}, {\'source\': \'A\', \'target\': \'C\', \'count\': 2}, {\'source\': \'A\', \'target\': \'D\', \'count\': 2}, {\'source\': \'A\', \'target\': \'E\', \'count\': 2}, {\'source\': \'B\', \'target\': \'C\', \'count\': 2}, {\'source\': \'B\', \'target\': \'D\', \'count\': 2}, {\'source\': \'B\', \'target\': \'E\', \'count\': 2}, {\'source\': \'C\', \'target\': \'D\', \'count\': 2}, {\'source\': \'C\', \'target\': \'E\', \'count\': 2}, {\'source\': \'D\', \'target\': \'E\', \'count\': 2}]'),('a03e0ada-d996-4344-8bef-c39b0ba5f7af','test','a',NULL,NULL),('d8a0ece7-319a-4887-b36e-9381e03c4a45','Manuel Gálvez Gómez','Proyecto 1',NULL,NULL);
/*!40000 ALTER TABLE `Projects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-13 14:49:39
