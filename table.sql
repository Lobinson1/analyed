CREATE TABLE `t_securities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL COMMENT '代码',
  `name` varchar(20) NOT NULL COMMENT '名称',
  `market` varchar(20) NOT NULL COMMENT '市场',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_code_market` (`code`,`market`)
) ENGINE=InnoDB AUTO_INCREMENT=4957 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `t_securities_daily` (
  `id` int NOT NULL AUTO_INCREMENT,
  `securities_id` int NOT NULL COMMENT '证券ID',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '日期',
  `begin` decimal(20,6) NOT NULL COMMENT '开盘价',
  `high` decimal(20,6) NOT NULL COMMENT '最高价',
  `low` decimal(20,6) NOT NULL COMMENT '最低价',
  `end` decimal(20,6) NOT NULL COMMENT '收盘价',
  `pre_end` decimal(20,6) DEFAULT NULL COMMENT '昨日收盘价',
  `turnover_rate` decimal(20,6) NOT NULL COMMENT '换手率',
  `is_top` bit(1) NOT NULL COMMENT '是否收盘为当日最高价',
  `is_last` bit(1) NOT NULL COMMENT '是否收盘为当日最低价',
  `turnover` decimal(20,6) NOT NULL COMMENT '成交量',
  `turnover_number` decimal(20,6) DEFAULT NULL COMMENT '成交额',
  `is_st` bit(1) NOT NULL COMMENT '是否ST',
  `percent` decimal(20,6) NOT NULL COMMENT '涨跌幅',
  `pe_ttm` decimal(20,6) NOT NULL COMMENT '滚动市盈率',
  `trade_status` bit(1) NOT NULL COMMENT '是否停牌',
  PRIMARY KEY (`id`),
  KEY `index_securities_id` (`securities_id`,`day`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;