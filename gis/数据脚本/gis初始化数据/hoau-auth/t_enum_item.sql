-- --------------------------------------------------------
-- 主机:                           10.108.2.112
-- Server version:               5.7.24-log - MySQL Community Server (GPL)
-- Server OS:                    Linux
-- HeidiSQL 版本:                  10.0.0.5460
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping data for table hoau-auth.t_enum_item: ~20 rows (approximately)
DELETE FROM `t_enum_item`;
/*!40000 ALTER TABLE `t_enum_item` DISABLE KEYS */;
INSERT INTO `t_enum_item` (`enum_code`, `enum_item_key`, `enum_item_value`, `visble`, `show_order`, `remark`, `creator`, `create_time`, `modifier`, `modify_time`) VALUES
	('DEAD_STS', 'DISABLED', '停用', 1, 1, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('DEAD_STS', 'ENABLED', '启用', 1, 2, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('OPER_TYPE', 'NEW', '新增网点', 1, 1, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('OPER_TYPE', 'EDIT', '编辑网点', 1, 2, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('OPER_TYPE', 'DELETE', '删除网点', 1, 3, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('OPER_TYPE', 'SYNC', '网点同步', 1, 4, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('OPER_TYPE', 'ENABLE', '网点启用', 1, 5, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('OPER_TYPE', 'TERRI_COPY', '版图复制', 1, 6, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('OPER_TYPE', 'AUDIT', '审核网点', 1, 7, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('OPER_TYPE', 'DISABLE', '网点停用', 1, 8, NULL, 'admin', '2019-01-22 19:26:27', 'admin', '2019-01-22 19:26:27'),
	('ORG_LEVEL', 'PLATFORM', '平台', 1, 1, NULL, 'admin', '2019-01-22 13:23:50', 'admin', '2019-01-22 13:23:50'),
	('ORG_LEVEL', 'STORE', '门店', 1, 2, NULL, 'admin', '2019-01-22 13:23:50', 'admin', '2019-01-22 13:23:50'),
	('ORG_LEVEL', 'OFFSET_LINE', '偏线', 1, 3, NULL, 'admin', '2019-01-22 13:23:50', 'admin', '2019-01-22 13:23:50'),
	('ORG_LEVEL', 'TOP_LEVEL', '一级公司', 1, 4, NULL, 'admin', '2019-01-22 13:23:50', 'admin', '2019-01-22 13:23:50'),
	('AUTH_STATUS', 'VALID', '生效', 1, 1, NULL, 'admin', '2019-01-22 13:26:28', 'admin', '2019-01-22 13:26:28'),
	('AUTH_STATUS', 'INVALID', '失效', 1, 2, NULL, 'admin', '2019-01-22 13:26:28', 'admin', '2019-01-22 13:26:28'),
	('USER_STATUS', 'ENABLED', '启用', 1, 1, NULL, 'admin', '2019-01-22 13:27:32', 'admin', '2019-01-22 13:27:32'),
	('USER_STATUS', 'DISABLED', '停用', 1, 2, NULL, 'admin', '2019-01-22 13:27:32', 'admin', '2019-01-22 13:27:32'),
	('STATUS', 'NON_AUDIT', '未审核', 1, 1, NULL, 'admin', '2019-01-25 14:46:00', 'admin', '2019-01-25 14:46:00'),
	('STATUS', 'AUDITED', '已审核', 1, 2, NULL, 'admin', '2019-01-25 14:46:00', 'admin', '2019-01-25 14:46:00');
/*!40000 ALTER TABLE `t_enum_item` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
