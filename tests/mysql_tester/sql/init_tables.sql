-- =====================================================
-- simpysql MySQL 测试数据库初始化脚本
-- =====================================================

-- 测试用户表
DROP TABLE IF EXISTS `test_users`;
CREATE TABLE `test_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '用户名',
  `email` varchar(100) NOT NULL DEFAULT '' COMMENT '邮箱',
  `age` int(11) NOT NULL DEFAULT 0 COMMENT '年龄',
  `status` tinyint(4) NOT NULL DEFAULT 1 COMMENT '状态: 0=禁用, 1=启用',
  `score` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '分数',
  `created_at` int(11) NOT NULL DEFAULT 0 COMMENT '创建时间',
  `updated_at` int(11) NOT NULL DEFAULT 0 COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_age` (`age`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试用户表';

-- 测试订单表 (用于关联查询测试)
DROP TABLE IF EXISTS `test_orders`;
CREATE TABLE `test_orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `user_id` int(11) NOT NULL DEFAULT 0 COMMENT '用户ID',
  `order_no` varchar(50) NOT NULL DEFAULT '' COMMENT '订单号',
  `amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '订单金额',
  `status` tinyint(4) NOT NULL DEFAULT 0 COMMENT '状态: 0=待支付, 1=已支付, 2=已取消',
  `created_at` int(11) NOT NULL DEFAULT 0 COMMENT '创建时间',
  `updated_at` int(11) NOT NULL DEFAULT 0 COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试订单表';

-- 测试商品表 (用于关联查询测试)
DROP TABLE IF EXISTS `test_products`;
CREATE TABLE `test_products` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '商品名称',
  `price` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '商品价格',
  `stock` int(11) NOT NULL DEFAULT 0 COMMENT '库存',
  `status` tinyint(4) NOT NULL DEFAULT 1 COMMENT '状态: 0=下架, 1=上架',
  `created_at` int(11) NOT NULL DEFAULT 0 COMMENT '创建时间',
  `updated_at` int(11) NOT NULL DEFAULT 0 COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试商品表';

-- 测试文章表 (用于全文搜索和LIKE测试)
DROP TABLE IF EXISTS `test_articles`;
CREATE TABLE `test_articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `title` varchar(200) NOT NULL DEFAULT '' COMMENT '标题',
  `content` text COMMENT '内容',
  `author_id` int(11) NOT NULL DEFAULT 0 COMMENT '作者ID',
  `view_count` int(11) NOT NULL DEFAULT 0 COMMENT '浏览次数',
  `status` tinyint(4) NOT NULL DEFAULT 1 COMMENT '状态: 0=草稿, 1=发布',
  `created_at` int(11) NOT NULL DEFAULT 0 COMMENT '创建时间',
  `updated_at` int(11) NOT NULL DEFAULT 0 COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_author_id` (`author_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试文章表';

-- =====================================================
-- 测试数据初始化
-- =====================================================

-- 插入测试用户数据
INSERT INTO `test_users` (`name`, `email`, `age`, `status`, `score`, `created_at`, `updated_at`) VALUES
('张三', 'zhangsan@test.com', 25, 1, 85.50, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('李四', 'lisi@test.com', 30, 1, 92.00, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('王五', 'wangwu@test.com', 28, 0, 78.50, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('赵六', 'zhaoliu@test.com', 35, 1, 88.00, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('钱七', 'qianqi@test.com', 22, 1, 95.50, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('孙八', 'sunba@test.com', 40, 0, 72.00, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('周九', 'zhoujiu@test.com', 33, 1, 81.50, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('吴十', 'wushi@test.com', 27, 1, 90.00, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('郑十一', 'zheng11@test.com', 29, 1, 86.50, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('王小明', 'xiaoming@test.com', 24, 1, 91.00, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('李小红', 'xiaohong@test.com', 26, 0, 83.50, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('张伟', 'zhangwei@test.com', 31, 1, 87.00, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('刘洋', 'liuyang@test.com', 23, 1, 94.00, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('陈静', 'chenjing@test.com', 32, 1, 89.50, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('杨帆', 'yangfan@test.com', 28, 0, 76.00, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- 插入测试订单数据
INSERT INTO `test_orders` (`user_id`, `order_no`, `amount`, `status`, `created_at`, `updated_at`) VALUES
(1, 'ORD20240101001', 199.90, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(1, 'ORD20240101002', 299.00, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(2, 'ORD20240102001', 599.00, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(3, 'ORD20240103001', 88.00, 2, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(4, 'ORD20240104001', 1288.00, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(5, 'ORD20240105001', 66.60, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(6, 'ORD20240106001', 456.00, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(7, 'ORD20240107001', 789.00, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(8, 'ORD20240108001', 123.45, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(9, 'ORD20240109001', 999.99, 2, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- 插入测试商品数据
INSERT INTO `test_products` (`name`, `price`, `stock`, `status`, `created_at`, `updated_at`) VALUES
('iPhone 15', 6999.00, 100, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('MacBook Pro', 12999.00, 50, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('AirPods Pro', 1799.00, 200, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('iPad Air', 4799.00, 80, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Apple Watch', 2999.00, 150, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Magic Keyboard', 999.00, 60, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Magic Mouse', 699.00, 100, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Studio Display', 11499.00, 30, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Mac Mini', 4499.00, 40, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('HomePod', 2299.00, 70, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- 插入测试文章数据
INSERT INTO `test_articles` (`title`, `content`, `author_id`, `view_count`, `status`, `created_at`, `updated_at`) VALUES
('Python入门教程', 'Python是一门优秀的编程语言...', 1, 1500, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('MySQL优化指南', '本文介绍MySQL的性能优化技巧...', 2, 2300, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Redis实战', 'Redis是一个高性能的键值存储...', 3, 1800, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Docker容器化部署', 'Docker让应用部署更加简单...', 1, 950, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('微服务架构设计', '微服务架构的核心概念...', 4, 3200, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Git版本控制', 'Git是现代开发的必备工具...', 5, 1100, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Linux运维基础', 'Linux系统管理入门...', 6, 880, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('Nginx配置详解', 'Nginx是一款高性能的Web服务器...', 7, 1650, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('RESTful API设计', 'REST架构风格的设计原则...', 2, 2100, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('单元测试最佳实践', '编写高质量测试用例...', 8, 750, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
