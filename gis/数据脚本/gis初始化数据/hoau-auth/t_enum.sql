-- --------------------------------------------------------
-- 主机:                           10.108.2.115
-- Server version:               5.7.24-log - MySQL Community Server (GPL)
-- Server OS:                    Linux
-- HeidiSQL 版本:                  10.0.0.5460
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping data for table hoau-auth.t_enum: ~0 rows (approximately)
DELETE FROM `t_enum`;
/*!40000 ALTER TABLE `t_enum` DISABLE KEYS */;
INSERT INTO `t_enum` (`name`, `code`, `sys_code`, `app_code`, `remark`, `creator`, `create_time`, `modifier`, `modify_time`) VALUES
	('状态', 'STATUS', 'hoau', 'hoau-gis', NULL, 'admin', '2019-01-21 13:37:13', 'admin', '2019-01-21 13:37:13'),
	('停用状态', 'DEAD_STS', 'hoau', 'hoau-gis', NULL, 'admin', '2019-01-21 13:37:13', 'admin', '2019-01-21 13:37:13'),
	('操作类型', 'OPER_TYPE', 'hoau', 'hoau-gis', NULL, 'admin', '2019-01-21 13:37:13', 'admin', '2019-01-21 13:37:13'),
	('用户状态', 'USER_STATUS', 'hoau', 'hoau-auth', NULL, 'admin', '2019-01-22 13:11:10', 'admin', '2019-01-22 13:11:10'),
	('权限通用状态', 'AUTH_STATUS', 'hoau', 'hoau-auth', NULL, 'admin', '2019-01-22 13:12:32', 'admin', '2019-01-22 13:12:32'),
	('机构级别', 'ORG_LEVEL', 'hoau', 'hoau-auth', NULL, 'admin', '2019-01-22 13:13:25', 'admin', '2019-01-22 13:13:25');
/*!40000 ALTER TABLE `t_enum` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
