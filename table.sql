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
  `begin` double NOT NULL COMMENT '开盘价',
  `hight` double NOT NULL COMMENT '最高价',
  `low` double NOT NULL COMMENT '最低价',
  `end` double NOT NULL COMMENT '收盘价',
  `pre_end` double DEFAULT NULL COMMENT '昨日收盘价',
  `turnover_rate` double NOT NULL COMMENT '换手率',
  `is_top` bit(1) NOT NULL COMMENT '是否涨停',
  `is_last` bit(1) NOT NULL COMMENT '是否跌停',
  `turnover` double NOT NULL COMMENT '成交量',
  `turnover_number` double DEFAULT NULL COMMENT '成交额',
  `market_value` double NOT NULL COMMENT '市值',
  `is_st` bit(1) NOT NULL COMMENT '是否ST',
  `percent` double NOT NULL COMMENT '涨跌幅',
  `pe_ttm` double NOT NULL COMMENT '滚动市盈率',
  PRIMARY KEY (`id`),
  KEY `index_securities_id` (`securities_id`,`day`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;