-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- Server version:               8.0.11 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL 版本:                  10.0.0.5460
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping data for table hoau_gis.t_territory: ~3 rows (approximately)
DELETE FROM `t_territory`;
/*!40000 ALTER TABLE `t_territory` DISABLE KEYS */;
INSERT INTO `t_territory` (`territory_code`, `territory_name`, `show_order`, `service_type`, `remark`, `creator`, `create_time`, `modifier`, `modify_time`) VALUES
	('244423365703815168', '收件版图', 0, 'CARGO_COLLECT', NULL, '000000000000000000', '2019-01-13 21:38:02', '000000000000000000', '2019-01-13 21:38:02'),
	('244423366479761408', '派送版图', 1, 'SITE_DELIVERY', NULL, '000000000000000000', '2019-01-13 21:38:02', '000000000000000000', '2019-01-13 21:38:02'),
	('244423366521704448', '自提版图', 2, 'CUSTOMER_PICK_UP', NULL, '000000000000000000', '2019-01-13 21:38:02', '000000000000000000', '2019-01-13 21:38:02');
/*!40000 ALTER TABLE `t_territory` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
