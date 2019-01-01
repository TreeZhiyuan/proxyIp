DROP TABLE IF EXISTS `xc_proxy_ip`;
CREATE TABLE `xc_proxy_ip` (
  `IP` VARCHAR(15) NOT NULL DEFAULT '' COMMENT 'IP地址',
  `PORT` INT NOT NULL DEFAULT 80 COMMENT '端口号',
  `REGION` VARCHAR(50) NOT NULL DEFAULT '' COMMENT '地区',
  UNIQUE KEY `IPPORTPERM` (`IP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table if exists `zy_account`;
CREATE TABLE `zy_account` (
  `id` bigint(32) NOT NULL AUTO_INCREMENT comment '自增主键',
  `name` VARCHAR(15) NOT NULL COMMENT '账户',
  `password` VARCHAR(64) NOT NULL COMMENT '加密后的密码',
  `role` tinyint NOT NULL DEFAULT 1 COMMENT '管理员权限 0为超级管理员',
  `status` tinyint not null default 1 comment '账号状态 1: 正常 0:异常',
  PRIMARY KEY `PRIMARYID` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='账户信息表';