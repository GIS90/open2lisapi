------------------------------------------------
describe[线上地址]:
    database: opentool
    user: opentool
    tables:
        sysuser	用户	用户基础信息表	sysuser
        role	角色	用户角色权限表	role
        menu	菜单	系统菜单表	menu
        request	用户请求API记录	用户前端请求后台API记录表	request
        api	api	后台API接口说明表	api
        department	部门	部门架构信息表	department
        excel_source	Excel源文件	Excel原始文件表	excel_source
        excel_result	Excel成果文件	Excel转换成果记录表	excel_result
        office_pdf	PDF文件表	PDF转WORD文档转换记录表	office_pdf
        dtalk_message	钉钉消息	钉钉消息记录表	dtalk_message
        dtalk_robot	钉钉机器人	钉钉消息机器人配置表	dtalk_robot


usage:
    execute sql in database client


base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2liapi"

常用命令:
远程连接: mysql -h 127.0.0.1 -P 3306  -u root -p
授权: grant all on *.* to '用户名'@'%' identified by '密码';
删除授权: revoke all privileges on *.* from '用户名'@'%';
刷新: flush privileges;
查询版本: select version(),current_date;;
显示所有数据库:  show databases;
显示当前数据库包含的表: show tables;
查看数据库字符集: show variables like '%char%';
查看mysql实例的端口: show variables like 'port';
用户重命名: RENAME USER '老名'@'%' TO '新名'@'%';
锁表:  flush tables with read lock;
查看当前用户:  select user();
查看所有用户: SELECT User, Host, Password FROM mysql.user;
显示表结构和列结构的命令: desc tablename;
查看master状态: show master status;
查看slave状态: show slave status ;
查看所有的log文件: show master logs;在主服务器上执行(即查看所有binlog日志列表)
显示最近的警告详情:

导出工具:
    mysqldump
------------------------------------------------

-- 创建数据库、用户、授权
create database opentool default character set utf8 collate utf8_general_ci;
create user 'opentool'@'%' IDENTIFIED BY 'ed39def30b9110d6668013133def82a3';
grant all on opentool.* to 'opentool';
flush  privileges;

use opentool;

-- create user
DROP TABLES IF EXISTS `sysuser`;
CREATE TABLE `sysuser` (
	`id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
	`rtx_id` varchar(25) not null COMMENT '用户rtx唯一标识',
	`md5_id` varchar(55) not null COMMENT 'rtx-md5标识',
	`fullname` varchar(30) not null COMMENT '用户名称',
	`password` varchar(30) not null COMMENT '用户明文密码',
	`email` varchar(35)  COMMENT '邮箱',
	`phone` varchar(15)  COMMENT '电话',
	`avatar` varchar(120)  COMMENT '头像URL',
	`introduction` text  COMMENT '用户描述',
	`role` varchar(80) not null COMMENT '用户角色rtx-id值，关联role表，多角色用;分割',
	`department` varchar(55) null COMMENT '用户部门md5值，关联department表',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`create_rtx` varchar(25) default 'admin' COMMENT '创建人',
	`delete_time` timestamp COMMENT '删除时间',
	`delete_rtx` varchar(25) COMMENT '删除操作人',
	`is_del` bool default False COMMENT '是否已删除',

	PRIMARY KEY (`id`)
) COMMENT='用户基础信息表';

-- create index
CREATE UNIQUE INDEX sysuser_rtx_id_index ON sysuser (`rtx_id`);

-- insert default admin
insert into
sysuser(rtx_id, md5_id, fullname, `password`, email , phone, avatar, introduction, role, create_rtx, is_del)
VALUES
('admin', '21232f297a57a5a743894a0e4a801fc3', '系统管理员', '1234567', 'gaoming971366@163.com', '13051355646',
'http://pygo2.top/images/article_github.jpg', 'ADMIN系统管理员', 'admin', 'admin', FALSE);




-- create role && index
DROP TABLES IF EXISTS `role`;
CREATE TABLE `role`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `engname` varchar(25) NOT NULL COMMENT '角色英文名称',
    `chnname` varchar(35) NOT NULL COMMENT '角色中文名称',
    `md5_id` varchar(55) NOT NULL COMMENT 'md5值',
    `authority` varchar(120) NULL COMMENT '角色权限ID集合，用英文；分割',
    `introduction` text NULL COMMENT '角色描述',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`create_rtx` varchar(25) default 'admin' COMMENT '创建人',
	`delete_time` timestamp COMMENT '删除时间',
	`delete_rtx` varchar(25) COMMENT '删除操作人',
	`is_del` bool default False COMMENT '是否已删除',

  PRIMARY KEY (`id`),
  UNIQUE INDEX `role_md5_index`(`md5_id`) USING HASH COMMENT 'md5唯一索引',
  UNIQUE INDEX `role_engname_index`(`engname`) USING HASH COMMENT 'engname唯一索引'
) COMMENT='角色权限表';
-- insert default role
insert into
role(engname, chnname, md5_id,  authority, introduction, create_rtx, is_del)
VALUES
('admin', '管理员', '21232f297a57a5a743894a0e4a801fc3', '', '所有功能权限', 'admin', FALSE);




-- create menu && index
DROP TABLES IF EXISTS `menu`;
CREATE TABLE `menu`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` varchar(25) NOT NULL COMMENT '路由rtx-id，首字母大写',
    `path` varchar(35) NOT NULL COMMENT '路由path，首字母小写',
    `title` varchar(25) NOT NULL COMMENT '名称',
    `pid` int NOT NULL COMMENT '父ID',
    `level` int NOT NULL default 1 COMMENT '级别',
    `md5_id` varchar(55) NOT NULL COMMENT 'md5值',
    `component` varchar(25) NOT NULL COMMENT '路由组件，与router mappings映射',
    `hidden` bool default False COMMENT '是否在SideBar显示，默认为false',
    `redirect` varchar(35) COMMENT '菜单重定向，主要用于URL一级菜单跳转',
    `icon` varchar(25) COMMENT '图标',
	`cache` bool default true COMMENT '页面是否进行cache，默认True缓存',
	`affix` bool default false  COMMENT '是否在tags-view固定，默认false',
	`breadcrumb` bool default true COMMENT '是否breadcrumb中显示，默认true',
    `order_id` int COMMENT '排序ID',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`create_rtx` varchar(25) default 'admin' COMMENT '创建人',
	`delete_time` timestamp COMMENT '删除时间',
	`delete_rtx` varchar(25) COMMENT '删除操作人',
	`is_del` bool default False COMMENT '是否已删除',

  PRIMARY KEY (`id`),
  UNIQUE INDEX `menu_md5_index`(`md5_id`) USING HASH COMMENT 'md5唯一索引',
  UNIQUE INDEX `menu_name_index`(`name`) USING HASH COMMENT 'name唯一索引'
) COMMENT='系统菜单表';

-- insert default menu
delete from menu;
insert into
    menu(id, `title`, `name`, `path`, `pid`, `level`, `md5_id`, `component`, `hidden`, `redirect`, `icon`, `cache`, `affix`, `breadcrumb`, `order_id`, `create_rtx`, `is_del`)
VALUES
-- root
 (0, '首页', 'Home', '/', 0, 0, '5ecb64c5576af2642f7eacb4679c8fda', 'layout', FALSE, '/', '', TRUE, FALSE, TRUE, 0, 'admin', FALSE),
-- 问题检索
(1, '问题检索', 'Search', '/search', 0, 1, '13348442cc6a27032d2b4aa28b75a5d3', 'layout', FALSE, '/search/probase', 'i_search', TRUE, FALSE, TRUE, 1, 'admin', FALSE),
(2, '问题仓库', 'SearchProbase', 'probase', 1, 2, 'c97d41080c06a689936f1c665ea334b5', 'searchProbase', FALSE, '', 'i_problem', TRUE, FALSE, TRUE, 2, 'admin', FALSE),
(3, '取数仓库', 'SearchSqlbase', 'sqlbase', 1, 2, '1b29b5aa48db5845f4a14c54a44eeb18', 'searchSqlbase', FALSE, '', 'i_sql', TRUE, FALSE, TRUE, 3, 'admin', FALSE),
-- 表格工具
(4, '文档工具', 'Office', '/office', 0, 1, 'c1d81af5835844b4e9d936910ded8fdc', 'layout', FALSE, '/office/pdf2word', 'i_office', TRUE, FALSE, TRUE, 4, 'admin', FALSE),
(5, 'PDF转WORD', 'PdfToWord', 'pdf2word', 4, 2, 'aa40dbd997f60d173d05f1f8375eb6bd', 'pdf2Word', FALSE, '', 'i_word', TRUE, FALSE, TRUE, 5, 'admin', FALSE),
(6, '表格合并', 'ExcelMerge', 'merge', 4, 2, '68be4837f6c739877233e527a996dd00', 'excelMerge', FALSE, '', 'i_merge', TRUE, FALSE, TRUE, 6, 'admin', FALSE),
(7, '表格拆分', 'ExcelSplit', 'split', 4, 2, '8a9e64d86ed12ad40de129bc7f4683b2', 'excelSplit', FALSE, '', 'i_split', TRUE, FALSE, TRUE, 7, 'admin', FALSE),
(8, '表格历史', 'ExcelHistory', 'history', 4, 2, '76c9a06443a050eccb7989cda6fff225', 'excelHistory', FALSE, '', 'i_excel', TRUE, FALSE, TRUE, 8, 'admin', FALSE),
-- 通知管理
(9, '通知消息', 'Notify', '/notify', 0, 1, 'aaf9ed605d0193362321ba0def15c9b7', 'layout', FALSE, '/notify/message', 'i_notify', TRUE, FALSE, TRUE, 9, 'admin', FALSE),
(10, '短信通知', 'NotifyMessage', 'message', 9, 2, '4c2a8fe7eaf24721cc7a9f0175115bd4', 'notifyMessage', FALSE, '', 'message', TRUE, FALSE, TRUE, 11, 'admin', FALSE),
(11, '钉钉绩效', 'NotifyDtalk', 'dtalk', 9, 2, '42dd43a9a00cc082e7bd9adec205439b', 'notifyDtalk', FALSE, '', 'i_dtalk', TRUE, FALSE, TRUE, 10, 'admin', FALSE),
-- 信息维护
(12, '信息维护', 'Info', '/info', 0, 1, '4059b0251f66a18cb56f544728796875', 'layout', FALSE, '/info/department', 'i_info', TRUE, FALSE, TRUE, 12, 'admin', FALSE),
(13, '部门架构', 'InfoDepartment', 'department', 12, 2, '1d17cb9923b99f823da9f5a16dc460e5', 'infoDepartment', FALSE, '', 'tree', TRUE, FALSE, TRUE, 13, 'admin', FALSE),
(14, '数据字典', 'InfoDict', 'dict', 12, 2, '91516e7a50ce0a67a8eb1f9229c293d1', 'infoDict', FALSE, '', 'i_dict', TRUE, FALSE, TRUE, 14, 'admin', FALSE),
-- 权限管理
(15, '权限管理', 'Manage', '/manage', 0, 1, '34e34c43ec6b943c10a3cc1a1a16fb11', 'layout', FALSE, '/manage/user', 'i_manage', TRUE, FALSE, TRUE, 15, 'admin', FALSE),
(16, '用户管理', 'ManageUser', 'user', 15, 2, '8f9bfe9d1345237cb3b2b205864da075', 'manageUser', FALSE, '', 'peoples', TRUE, FALSE, TRUE, 16, 'admin', FALSE),
(17, '角色管理', 'ManageRole', 'role', 15, 2, 'bbbabdbe1b262f75d99d62880b953be1', 'manageRole', FALSE, '', 'i_role', TRUE, FALSE, TRUE, 17, 'admin', FALSE),
(18, '菜单管理', 'ManageMenu', 'menu', 15, 2, 'b61541208db7fa7dba42c85224405911', 'manageMenu', FALSE, '', 'component', TRUE, FALSE, TRUE, 18, 'admin', FALSE),
-- 个人设置
(19, '个人设置', 'Setter', '/setter', 0, 1, '130bdeec588552954b9e3bea0ef364b2', 'layout', FALSE, '/setter/profile', 'i_setter', TRUE, FALSE, TRUE, 19, 'admin', FALSE),
(20, '个人中心', 'SetterProfile', 'profile', 19, 2, 'cce99c598cfdb9773ab041d54c3d973a', 'setterProfile', FALSE, '', 'i_user', TRUE, FALSE, TRUE, 20, 'admin', FALSE),
(21, '系统向导', 'SetterGuide', 'guide', 19, 2, '6602bbeb2956c035fb4cb5e844a4861b', 'setterGuide', FALSE, '', 'guide', TRUE, FALSE, TRUE, 21, 'admin', FALSE);




-- create request && index
DROP TABLES IF EXISTS `request`;
CREATE TABLE `request`  (
    `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `rtx_id` varchar(25) NOT NULL COMMENT '用户rtx唯一标识',
    `ip` varchar(15) NOT NULL COMMENT '用户IP',
    `blueprint` varchar(25) NULL COMMENT 'API地址blueprint',
    `endpoint` varchar(35) NULL COMMENT 'API地址endpoint',
    `method` varchar(10) NULL COMMENT 'API请求method',
    `path` varchar(35) NULL COMMENT 'API地址path',
    `full_path` varchar(85) NULL COMMENT 'API地址full_path',
    `host_url` varchar(55) NULL COMMENT 'API地址host_url',
    `url` varchar(120) NULL COMMENT 'API地址url',
    `create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '请求时间点',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `index_id`(`id`) USING HASH COMMENT 'id索引'
) COMMENT='系统API请求记录表';

-- delete
delete from request;
-- no insert data




-- create api mapping && index
DROP TABLES IF EXISTS `api`;
CREATE TABLE `api`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `blueprint` varchar(25) NOT NULL COMMENT 'API接口blueprint',
    `endpoint` varchar(35) NOT NULL COMMENT 'API接口endpoint',
    `path` varchar(35) NOT NULL COMMENT 'API接口path，与request表关联',
    `type` varchar(15) NOT NULL default 'success' COMMENT 'API接口类型：primary登录/success数据获取/warning/danger退出/info新增/更新/删除数据',
    `short` varchar(35) NULL COMMENT 'API接口简述',
    `long` varchar(120) NULL COMMENT 'API接口详细描述',
    `create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
    `create_rtx` varchar(25) default 'admin' COMMENT '创建人',
    `delete_time` timestamp COMMENT '删除时间',
    `delete_rtx` varchar(25) COMMENT '删除操作人',
    `is_del` bool default FALSE COMMENT '是否已删除',

  PRIMARY KEY (`id`),
  UNIQUE INDEX `index_id`(`id`) USING HASH COMMENT 'id索引'
) COMMENT='API接口说明表';
-- delete
delete from api;
-- insert data
-- SQL见开发进度表->后台API




-- create enum mapping && index
DROP TABLES IF EXISTS `enum`;
CREATE TABLE `enum`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` varchar(25) NOT NULL COMMENT '枚举名称',
    `md5_id` varchar(55) NOT NULL COMMENT '枚举md5-id，以name为md5',
    `key` varchar(25) NOT NULL COMMENT '枚举子集对应的key',
    `value` varchar(55) NOT NULL COMMENT '枚举子集对应的value',
    `description` text COMMENT '枚举子集对应的value说明',
    `create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
    `create_rtx` varchar(25) default 'admin' COMMENT '创建人',
    `delete_time` timestamp COMMENT '删除时间',
    `delete_rtx` varchar(25) COMMENT '删除操作人',
    `is_del` bool default FALSE COMMENT '是否已删除',

  PRIMARY KEY (`id`),
  UNIQUE INDEX `index_id`(`id`) USING HASH COMMENT 'id索引'
) COMMENT='ENUM枚举表';
-- delete
delete from enum;
-- insert data
insert into
enum(`name`, `md5_id`, `key`, `value`, `description`, `create_rtx`)
VALUES
-- bool
('bool-type', '5886ecb16dfd303f97ef685f943f4735', '1', '是', '是', 'admin'),
('bool-type', '5886ecb16dfd303f97ef685f943f4735', '0', '否', '否', 'admin'),
-- excel-type
('excel-type', '3a4048a9372203790ebfc88337f38981', '1', '合并', '表格处理方式合并', 'admin'),
('excel-type', '3a4048a9372203790ebfc88337f38981', '2', '拆分', '表格处理方式拆分', 'admin'),
-- excel-split-store
('excel-split-store', '1c4512eb1dd13274569ec4763adfb12f', '1', '多表一Sheet', '表格拆分多表一Sheet存储方式', 'admin'),
('excel-split-store', '1c4512eb1dd13274569ec4763adfb12f', '2', '一表多Sheet', '表格拆分一表多Sheet存储方式', 'admin'),
-- excel-num
('excel-num', '9890c80bbbbf66fa44c808243186c4d1', '1', '行', '行', 'admin'),
('excel-num', '9890c80bbbbf66fa44c808243186c4d1', '2', '列', '列', 'admin'),
-- menu-level
('menu-level', 'cde5d071f0b5bbb56033121304b6604a', '1', '一级菜单', '一级菜单', 'admin'),
('menu-level', 'cde5d071f0b5bbb56033121304b6604a', '2', '二级菜单', '二级菜单', 'admin'),
-- 文件类型
('file-type', 'e74dbc2d915cec9012135907cc4932eb', '1', 'WORD', 'WORD文档', 'admin'),
('file-type', 'e74dbc2d915cec9012135907cc4932eb', '2', 'EXCEL', 'EXCEL表格', 'admin'),
('file-type', 'e74dbc2d915cec9012135907cc4932eb', '3', 'PPT', 'PPT演示文稿', 'admin'),
('file-type', 'e74dbc2d915cec9012135907cc4932eb', '4', '文本', '文本文件', 'admin'),
('file-type', 'e74dbc2d915cec9012135907cc4932eb', '5', 'PDF', 'PDF文件', 'admin'),
('file-type', 'e74dbc2d915cec9012135907cc4932eb', '99', '其他', '其他类型文件', 'admin');




-- create excel_source
DROP TABLES IF EXISTS `excel_source`;

CREATE TABLE `excel_source` (
	`id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
	`name` varchar(80) COMMENT '原始名称',
	`store_name` varchar(100) COMMENT '存储名称',
	`md5_id` varchar(55) NOT NULL COMMENT 'md5-id',
	`rtx_id` varchar(25) NOT NULL COMMENT '用户rtx-id',
	`ftype` varchar(2) NOT NULL default '1' COMMENT '文件上传类型：1拆分;2合并',
	`local_url` varchar(120) COMMENT '文件本地资源路径（绝对路径）',
	`store_url` varchar(120) COMMENT '文件store对象存储资源路径（相对路径）',
	`numopr` int default 0 COMMENT '操作次数',
	`nsheet` int default 1 COMMENT 'sheet数',
	`set_sheet` varchar(35) COMMENT '当前设置的sheet选择索引，列表格式',
	`sheet_names` text COMMENT 'Sheets名称列表，以json方式存储',
	`sheet_columns` text COMMENT 'Sheets列名的集合，以json方式存储',
	`headers` text COMMENT 'excel的header信息，以json方式存储',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`delete_rtx` varchar(25) COMMENT '删除用户rtx',
	`delete_time` datetime COMMENT '删除时间',
	`is_del` bool DEFAULT False COMMENT '是否删除',

	PRIMARY KEY (`id`)
) COMMENT='Excel原始文件表';
-- create index
CREATE UNIQUE INDEX excel_source_index ON excel_source (`md5_id`);




-- create excel_result
DROP TABLES IF EXISTS `excel_result`;

CREATE TABLE `excel_result` (
	`id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
	`name` varchar(80) COMMENT '原始名称',
	`store_name` varchar(100) COMMENT '存储名称',
	`md5_id` varchar(55) NOT NULL COMMENT 'md5-id',
	`rtx_id` varchar(25) NOT NULL COMMENT '用户rtx-id',
	`ftype` varchar(2) NOT NULL COMMENT '转换类型：1拆分;2合并',
	`local_url` varchar(120) COMMENT '文件本地资源路径（绝对路径）',
	`store_url` varchar(120) COMMENT '文件store对象存储资源路径（相对路径）',
	`is_compress` bool DEFAULT False COMMENT '是否是压缩文件',
	`nfile` int COMMENT '文件个数',
	`nsheet` int COMMENT 'sheet总数',
	`row` int COMMENT '行数',
	`col` int COMMENT '列数',
	`sheet_names` text COMMENT 'Sheets名称列表，以json方式存储',
	`sheet_columns` text COMMENT 'Sheets列名的集合，以json方式存储',
	`headers` text COMMENT 'excel的header信息，以json方式存储',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`delete_rtx` varchar(25) COMMENT '删除用户rtx',
	`delete_time` datetime COMMENT '删除时间',
	`is_del` bool DEFAULT False COMMENT '是否删除',

	PRIMARY KEY (`id`)
) COMMENT='Excel转换成功记录表';

CREATE UNIQUE INDEX excel_result_index ON excel_result (`md5_id`);




-- create office
DROP TABLES IF EXISTS `office_pdf`;

CREATE TABLE `office_pdf` (
	`id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
	`name` varchar(80) NOT NULL COMMENT '原始名称',
	`store_name` varchar(100) COMMENT '原始文件store存储名称',
	`transfer_name` varchar(100) COMMENT '转换文件store存储名称',
	`md5_id` varchar(55) NOT NULL COMMENT 'md5-id',
	`rtx_id` varchar(25) NOT NULL COMMENT '用户rtx-id',
	`file_type` varchar(2) NOT NULL COMMENT '文件类型',
	`transfer` bool DEFAULT False COMMENT '转换状态',
    `transfer_time` datetime COMMENT '转换时间',
    `local_url` varchar(120) COMMENT '文件本地资源路径（绝对路径）',
	`store_url` varchar(120) COMMENT '原始文件store对象存储资源路径（相对路径）',
	`transfer_url` varchar(120) COMMENT '转换文件store对象存储资源路径（相对路径）',
	`mode` bool DEFAULT True COMMENT '转换模式：True页码，False指定页码',
	`start` int COMMENT '转换开始页',
	`end` int COMMENT '转换结束页',
	`pages` varchar(120) COMMENT '指定的转换页码',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`delete_rtx` varchar(25) COMMENT '删除用户rtx',
	`delete_time` datetime COMMENT '删除时间',
	`is_del` bool DEFAULT False COMMENT '是否删除',

	PRIMARY KEY (`id`)
) COMMENT='PDF文件记录表';

CREATE UNIQUE INDEX office_pdf_index ON office_pdf (`md5_id`);


-- create dtalk_message
DROP TABLES IF EXISTS `dtalk_message`;

CREATE TABLE `dtalk_message`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `rtx_id` varchar(25) NOT NULL COMMENT '用户RTX-ID',
    `file_name` varchar(80) NOT NULL COMMENT '文件名称',
    `file_local_url` varchar(120) NULL COMMENT '文件存储本地路径',
    `file_store_url` varchar(120) NULL COMMENT '文件存储云对象存储位置',
    `md5_id` varchar(55) NOT NULL COMMENT '数据记录record',
    `robot` varchar(55) NULL COMMENT 'dtalk选择机器人配置md5-id',
    `count` int NULL default 0 COMMENT '消息文件发送的累积次数',
    `number` int NULL default 0 COMMENT '消息发送的累积次数',
    `nsheet` int default 1 COMMENT 'sheet数',
    `sheet_names` text COMMENT 'Sheets名称列表，以json方式存储',
    `sheet_columns` text COMMENT 'Sheets列名的集合，以json方式存储',
    `headers` text COMMENT 'excel的header信息，以json方式存储',
    `set_sheet` varchar(35) COMMENT '当前设置的sheet选择索引，列表格式',
    `cur_sheet` varchar(3) COMMENT '当前设置的sheet索引',
    `set_column` text COMMENT '当前设置的sheet选择索引，表头列表设置，json字符串',
    `set_title` text COMMENT '每个sheet页码的消息标题',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`delete_rtx` varchar(25) COMMENT '删除用户rtx',
	`delete_time` datetime COMMENT '删除时间',
	`is_del` bool DEFAULT False COMMENT '是否删除',

    PRIMARY KEY (`id`)
) COMMENT='钉钉消息表';

CREATE UNIQUE INDEX dtalk_message_index ON dtalk_message (`md5_id`);



-- create dtalk_robot
DROP TABLES IF EXISTS `dtalk_robot`;

CREATE TABLE `dtalk_robot`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `rtx_id` varchar(25) NOT NULL COMMENT '用户RTX-ID',
    `name` varchar(30) NOT NULL COMMENT '机器人名称',
    `md5_id` varchar(55) NOT NULL COMMENT '数据记录record',
    `key` varchar(30) NOT NULL COMMENT '机器人APP-KEY',
    `secret` varchar(70) NOT NULL COMMENT '机器人APP-SECRET',
    `select` bool DEFAULT False COMMENT '是否当前为选择',
    `description` text COMMENT '描述',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`delete_rtx` varchar(25) COMMENT '删除用户rtx',
	`delete_time` datetime COMMENT '删除时间',
	`is_del` bool DEFAULT False COMMENT '是否删除',

    PRIMARY KEY (`id`)
) COMMENT='钉钉消息-机器人配置表';

CREATE UNIQUE INDEX dtalk_robot_index ON dtalk_robot (`md5_id`);

