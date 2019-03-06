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

-- Dumping data for table hoau_auth.t_role: ~2 rows (approximately)
DELETE FROM `t_role`;
/*!40000 ALTER TABLE `t_role` DISABLE KEYS */;
INSERT INTO `t_role` (`name`, `code`, `status`, `sys_code`, `scope`, `remark`, `creator`, `create_time`, `modifier`, `modify_time`) VALUES
	('平台门店操作员', '248311166052651008', 'VALID', '248300776082198528', '0', NULL, '000000000000000000', '2019-01-24 15:08:05', '000000000000000000', '2019-01-24 15:08:07'),
	('超级管理员', '248300698252693504', 'VALID', '248300776082198528', '0', NULL, '000000000000000000', '2019-01-24 10:50:05', '000000000000000000', '2019-01-24 10:50:05');
/*!40000 ALTER TABLE `t_role` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
