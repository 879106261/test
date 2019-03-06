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

-- Dumping data for table hoau_auth.t_sys: ~0 rows (approximately)
DELETE FROM `t_sys`;
/*!40000 ALTER TABLE `t_sys` DISABLE KEYS */;
INSERT INTO `t_sys` (`name`, `code`, `status`, `remark`, `creator`, `create_time`, `modifier`, `modify_time`) VALUES
	('GIS', '248300776082198528', 'VALID', '天地华宇地理信息系统', '000000000000000000', '2019-01-24 10:50:13', '000000000000000000', '2019-01-24 10:50:13');
/*!40000 ALTER TABLE `t_sys` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
