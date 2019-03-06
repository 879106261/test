-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        8.0.11 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出  表 g7.tb_station 结构
DROP TABLE IF EXISTS `tb_station`;
CREATE TABLE IF NOT EXISTS `tb_station` (
  `id` int(11) DEFAULT NULL,
  `orgcode` varchar(32) DEFAULT NULL,
  `code` varchar(32) DEFAULT NULL,
  `types` varchar(20) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `lat` decimal(10,7) DEFAULT NULL,
  `lng` decimal(10,7) DEFAULT NULL,
  `radius` varchar(20) DEFAULT NULL,
  `linkman` varchar(20) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  `bounded` varchar(20) DEFAULT NULL,
  `area` varchar(20) DEFAULT NULL,
  `used` varchar(20) DEFAULT NULL,
  `issync` varchar(20) DEFAULT NULL,
  `parentid` varchar(32) DEFAULT NULL,
  `provinceid` varchar(20) DEFAULT NULL,
  `cityid` varchar(20) DEFAULT NULL,
  `partid` varchar(20) DEFAULT NULL,
  `remark` varchar(512) DEFAULT NULL,
  `color` varchar(16) DEFAULT NULL,
  `maxlat` decimal(10,6) DEFAULT NULL,
  `maxlng` decimal(10,6) DEFAULT NULL,
  `minlat` decimal(10,6) DEFAULT NULL,
  `minlng` decimal(10,6) DEFAULT NULL,
  `maptype` varchar(20) DEFAULT NULL,
  `operateid` varchar(32) DEFAULT NULL,
  `areadesc` varchar(32) DEFAULT NULL,
  `orgcheck` varchar(16) DEFAULT NULL,
  `iswithmoney` varchar(20) DEFAULT NULL,
  `issignlist` varchar(20) DEFAULT NULL,
  `isEdit` varchar(20) DEFAULT NULL,
  `orgcheck_opt` varchar(20) DEFAULT NULL,
  `orgname` varchar(50) DEFAULT NULL,
  `bound` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
