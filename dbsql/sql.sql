------------------------------------------------
describe:
    database: twtoolbox
    user: twtoolbox
    tables:
        sysuser	用户	用户基础信息表
        role	角色	用户角色权限表
        menu	菜单	系统菜单表
        request	请求记录	后台API请求记录表
        api	api	后台API接口说明表
        department	部门	部门架构信息表
        excel_source	Excel源文件	Excel原始文件表
        excel_result	Excel成果文件	Excel转换成果记录表


usage:
    execute sql in database client


base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"
------------------------------------------------
-- 创建数据库、用户、授权
create database twtoolbox default character set utf8 collate utf8_general_ci;
create user 'twtoolbox'@'%' IDENTIFIED BY '2dcc0521bd32dc5100c6d65a1effa8e6';
grant all on twtoolbox.* to 'twtoolbox';
flush  privileges;

use twtoolbox;

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
	`avatar` varchar(255)  COMMENT '头像URL',
	`introduction` text  COMMENT '用户描述',
	`role` varchar(55) not null COMMENT '用户角色md5值，关联role表',
	`department` varchar(55) not null COMMENT '用户部门md5值，关联department表',
	`create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
	`create_rtx` varchar(25) COMMENT '创建人',
	`is_del` bool  COMMENT '是否已删除',
	`del_time` timestamp COMMENT '删除时间',
	`del_rtx` varchar(25) COMMENT '删除操作人',

	PRIMARY KEY (`id`),
	UNIQUE INDEX rtx_id(id ASC)
) COMMENT='用户基础信息表';

-- create index
CREATE UNIQUE INDEX sysuser_index ON sysuser (`rtx_id`);

-- insert default admin
insert into
sysuser(rtx_id, md5_id, fullname, `password`, email , phone, avatar, introduction, role, create_rtx, is_del)
VALUES
('admin', '21232f297a57a5a743894a0e4a801fc3', '系统管理员', '123456', 'gaoming971366@163.com', '13051355646',
'http://pygo2.top/images/article_github.jpg', '我是一名Python程序员', '21232f297a57a5a743894a0e4a801fc3', '第一用户', FALSE);




-- create role && index
DROP TABLES IF EXISTS `role`;
CREATE TABLE `role`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `engname` varchar(25) NOT NULL COMMENT '角色英文名称',
    `chnname` varchar(35) NOT NULL COMMENT '角色中文名称',
    `md5_id` varchar(55) NOT NULL COMMENT 'md5值',
    `authority` varchar(255) NULL COMMENT '角色权限，用英文；分割',
    `introduction` text NULL COMMENT '角色描述',
    `create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
    `create_rtx` varchar(25) COMMENT '创建人',
	`is_del` bool  COMMENT '是否已删除',
	`del_time` timestamp COMMENT '删除时间',
	`del_rtx` varchar(25) COMMENT '删除操作人',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `role_md5_index`(`md5_id`) USING HASH COMMENT 'md5唯一索引',
  UNIQUE INDEX `role_name_index`(`engname`) USING HASH COMMENT 'engname唯一索引'
) COMMENT='角色权限表';
-- insert default role
insert into
role(engname, chnname, md5_id,  authority, introduction, create_rtx, is_del)
VALUES
('admin', '管理员', '21232f297a57a5a743894a0e4a801fc3', '', '系统管理员总权限', 'admin', FALSE);




-- create menu && index
DROP TABLES IF EXISTS `menu`;
CREATE TABLE `menu`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` varchar(15) NOT NULL COMMENT '路由name，首字母大写',
    `path` varchar(35) NOT NULL COMMENT '路由path，首字母小写',
    `title` varchar(25) NOT NULL COMMENT '名称',
    `pid` int NOT NULL COMMENT '父ID',
    `level` int NOT NULL default 1 COMMENT '级别',
    `md5_id` varchar(55) NOT NULL COMMENT 'md5值',
    `component` varchar(15) NOT NULL COMMENT '路由组件，与router mappings映射',
    `hidden` bool default False COMMENT '是否在SideBar显示，默认为false',
    `redirect` varchar(55) COMMENT '重定向',
    `icon` varchar(25) COMMENT '图标',
	`noCache` bool default false COMMENT '页面是否进行cache，默认false',
	`affix` bool default false  COMMENT '是否在tags-view固定，默认false',
	`breadcrumb` bool default true COMMENT '是否breadcrumb中显示，默认true',
    `create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',
    `create_rtx` varchar(25) COMMENT '创建人',
	`is_del` bool  COMMENT '是否已删除',
	`del_time` timestamp COMMENT '删除时间',
	`del_rtx` varchar(25) COMMENT '删除操作人',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `menu_md5_index`(`md5_id`) USING HASH COMMENT 'md5唯一索引',
  UNIQUE INDEX `menu_name_index`(`name`) USING HASH COMMENT 'name唯一索引'
) COMMENT='系统菜单表';

-- insert default menu
delete from menu;
insert into
menu(id, `title`, `name`, `path`, `pid`, `level`, `md5_id`, `component`, `hidden`, `redirect`, `icon`, `noCache`, `affix`, `breadcrumb`, `create_rtx`, `is_del`)
VALUES
-- 问题检索
(1, '问题检索', 'Search', '/search', 0, 1, '13348442cc6a27032d2b4aa28b75a5d3', 'layout', FALSE, '/search/probase', 'i_search', FALSE, FALSE, TRUE, 'admin', FALSE),
(2, '问题仓库', 'SearchProbase', 'probase', 1, 2, 'c97d41080c06a689936f1c665ea334b5', 'search_probase', FALSE, '', 'i_problem', FALSE, FALSE, TRUE, 'admin', FALSE),
(3, '取数仓库', 'SearchSqlbase', 'sqlbase', 1, 2, '1b29b5aa48db5845f4a14c54a44eeb18', 'search_sqlbase', FALSE, '', 'i_sql', FALSE, FALSE, TRUE, 'admin', FALSE),
-- 表格工具
(4, '表格工具', 'Excel', '/excel', 0, 1, 'c1d81af5835844b4e9d936910ded8fdc', 'layout', FALSE, '/excel/merge', 'i_excel', FALSE, FALSE, TRUE, 'admin', FALSE),
(5, '表格合并', 'ExcelMerge', 'merge', 4, 2, '68be4837f6c739877233e527a996dd00', 'excel_merge', FALSE, '', 'i_merge', FALSE, FALSE, TRUE, 'admin', FALSE),
(6, '表格拆分', 'ExcelSplit', 'split', 4, 2, '8a9e64d86ed12ad40de129bc7f4683b2', 'excel_split', FALSE, '', 'i_split', FALSE, FALSE, TRUE, 'admin', FALSE),
(7, '我的历史', 'ExcelHistory', 'history', 4, 2, '76c9a06443a050eccb7989cda6fff225', 'excel_history', FALSE, '', 'i_history', FALSE, FALSE, TRUE, 'admin', FALSE),
-- 通知管理
(8, '通知消息', 'Notify', '/notify', 0, 1, 'aaf9ed605d0193362321ba0def15c9b7', 'layout', FALSE, '/notify/message', 'i_notify', FALSE, FALSE, TRUE, 'admin', FALSE),
(9, '短信通知', 'NotifyMessage', 'message', 8, 2, '4c2a8fe7eaf24721cc7a9f0175115bd4', 'notify_message', FALSE, '', 'message', FALSE, FALSE, TRUE, 'admin', FALSE),
(10, '钉钉绩效', 'NotifyDtalk', 'dtalk', 8, 2, '42dd43a9a00cc082e7bd9adec205439b', 'notify_dtalk', FALSE, '', 'i_dtalk', FALSE, FALSE, TRUE, 'admin', FALSE),
-- 文档转换
(11, '文档转换', 'Convert', '/convert', 0, 1, '920f4a0c5c8b9a0747380cf7c7f0b3c5', 'layout', FALSE, '/convert/pdf2word', 'i_convert', FALSE, FALSE, TRUE, 'admin', FALSE),
(12, 'PDF转WORD', 'ConvertPdf2word', 'pdf2word', 11, 2, 'aa40dbd997f60d173d05f1f8375eb6bd', 'convert_pdf2word', FALSE, '', 'i_word', FALSE, FALSE, TRUE, 'admin', FALSE),
-- 权限管理
(13, '权限管理', 'Manage', '/manage', 0, 1, '34e34c43ec6b943c10a3cc1a1a16fb11', 'layout', FALSE, '/manage/user', 'i_manage', FALSE, FALSE, TRUE, 'admin', FALSE),
(14, '用户管理', 'ManageUser', 'user', 13, 2, '8f9bfe9d1345237cb3b2b205864da075', 'manage_user', FALSE, '', 'peoples', FALSE, FALSE, TRUE, 'admin', FALSE),
(15, '角色管理', 'ManageRole', 'role', 13, 2, 'bbbabdbe1b262f75d99d62880b953be1', 'manage_role', FALSE, '', 'i_role', FALSE, FALSE, TRUE, 'admin', FALSE),
(16, '菜单管理', 'ManageMenu', 'menu', 13, 2, 'b61541208db7fa7dba42c85224405911', 'manage_menu', FALSE, '', 'component', FALSE, FALSE, TRUE, 'admin', FALSE),
-- 信息维护
(17, '信息维护', 'Info', '/info', 0, 1, '4059b0251f66a18cb56f544728796875', 'layout', FALSE, '/info/department', 'i_info', FALSE, FALSE, TRUE, 'admin', FALSE),
(18, '部门架构', 'InfoDepartment', 'department', 17, 2, '1d17cb9923b99f823da9f5a16dc460e5', 'info_department', FALSE, '', 'tree', FALSE, FALSE, TRUE, 'admin', FALSE),
(19, '数据字典', 'InfoDict', 'dict', 17, 2, '91516e7a50ce0a67a8eb1f9229c293d1', 'info_dict', FALSE, '', 'i_dict', FALSE, FALSE, TRUE, 'admin', FALSE),
-- 个人设置
(20, '个人设置', 'Setter', '/setter', 0, 1, '130bdeec588552954b9e3bea0ef364b2', 'layout', FALSE, '/setter/profile', 'i_setter', FALSE, FALSE, TRUE, 'admin', FALSE),
(21, '个人中心', 'SetterProfile', 'profile', 20, 2, 'cce99c598cfdb9773ab041d54c3d973a', 'setter_profile', FALSE, '', 'i_user', FALSE, FALSE, TRUE, 'admin', FALSE),
(22, '系统向导', 'SetterGuide', 'guide', 20, 2, '6602bbeb2956c035fb4cb5e844a4861b', 'setter_guide', FALSE, '', 'guide', FALSE, FALSE, TRUE, 'admin', FALSE);




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




-- create api mapping && index
DROP TABLES IF EXISTS `api`;
CREATE TABLE `api`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `blueprint` varchar(25) NULL COMMENT 'API接口blueprint',
  `endpoint` varchar(35) NULL COMMENT 'API接口endpoint',
  `path` varchar(35) NULL COMMENT 'API接口path，与request表关联',
  `type` varchar(15) NULL COMMENT 'API接口类型：primary登录/success数据获取/warning/danger退出/info新增/更新/删除数据',
  `short` varchar(35) NULL COMMENT 'API接口简述',
  `long` text NULL COMMENT 'API接口描述',
  `create_time` timestamp not null default CURRENT_TIMESTAMP COMMENT '数据添加时间',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `index_id`(`id`) USING HASH COMMENT 'id索引'
) COMMENT='API接口说明表';
-- delete
delete from api;
-- insert data
insert into
api(`blueprint`, `endpoint`, `path`, `type`, `short`, `long`)
VALUES
-- manage
('manage', 'manage.login_in', '/manage/login', 'primary', '登录', '用户请求系统登录'),
('manage', 'manage.login_out', '/manage/logout', 'danger', '退出', '用户请求系统退出'),
-- user
('user', 'user.info', '/user/info', 'info', '用户信息', '请求获取用户信息'),
('user', 'user.auth', '/user/auth', 'info', '用户权限', '请求获取用户权限'),
('user', 'user.timeline', '/user/timeline', 'info', '访问日志', '请求用户操作系统日志信息'),
('user', 'user.update', '/user/update', 'success', '更新用户信息', '更新用户基础信息数据'),
('user', 'user.password', '/user/password', 'success', '更新用户密码', '更新用户密码信息'),
('user', 'user.avatar', '/user/avatar', 'success', '更新用户头像', '更新用户头像信息'),
-- excel
('excel', 'excel.list', '/excel/list', 'info', 'Excel文件列表', '获取Excel文件列表'),
('excel', 'excel.upload', '/excel/upload', 'success', 'Excel上传文件', '上传单个Excel文件'),
('excel', 'excel.uploads', '/excel/uploads', 'success', 'Excel上传文件', '上传多个Excel文件'),
('excel', 'excel.update', '/excel/update', 'success', 'Excel更新数据', '更新Excel文件信息'),
('excel', 'excel.delete', '/excel/delete', 'success', 'Excel删除文件', '删除单个Excel文件'),
('excel', 'excel.deletes', '/excel/deletes', 'success', 'Excel批量文件', '批量删除多个Excel文件'),
('excel', 'excel.merge', '/excel/merge', 'success', 'Excel数据合并', '多个Excel、Sheet文件合并');



-- create enum mapping && index
DROP TABLES IF EXISTS `enum`;
CREATE TABLE `enum`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `name` varchar(25) NULL COMMENT '枚举名称',
  `md5_id` varchar(55) NULL COMMENT '枚举md5-id，以name为md5',
  `key` varchar(25) NULL COMMENT '枚举子集对应的key',
  `value` varchar(55) NULL COMMENT '枚举子集对应的value',
  `description` text COMMENT '枚举子集对应的value说明',
  `create_rtx` varchar(50) COMMENT '创建用户rtx',
  `create_time` datetime COMMENT '创建时间',
  `delete_rtx` varchar(50) COMMENT '删除用户rtx',
  `delete_time` datetime COMMENT '删除时间',
  `is_del` bool DEFAULT False COMMENT '是否删除',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `index_id`(`id`) USING HASH COMMENT 'id索引'
) COMMENT='ENUM枚举表';
-- delete
delete from enum;
-- insert data
insert into
enum(`name`, `md5_id`, `key`, `value`, `description`, `create_rtx`, `create_time`)
VALUES
-- bool
('bool-type', '5886ecb16dfd303f97ef685f943f4735', '1', '是', '是', 'admin', '2022-04-27 00:00:00'),
('bool-type', '5886ecb16dfd303f97ef685f943f4735', '0', '否', '否', 'admin', '2022-04-27 00:00:00'),
-- excel-type
('excel-type', '3a4048a9372203790ebfc88337f38981', '1', '合并', '表格处理方式合并', 'admin', '2022-04-27 00:00:00'),
('excel-type', '3a4048a9372203790ebfc88337f38981', '2', '拆分', '表格处理方式拆分', 'admin', '2022-04-27 00:00:00'),
-- excel-split-store
('excel-split-store', '1c4512eb1dd13274569ec4763adfb12f', '1', '多表一Sheet', '表格拆分多表一Sheet存储方式', 'admin', '2022-04-27 00:00:00'),
('excel-split-store', '1c4512eb1dd13274569ec4763adfb12f', '2', '一表多Sheet', '表格拆分一表多Sheet存储方式', 'admin', '2022-04-27 00:00:00'),
-- excel-num
('excel-num', '9890c80bbbbf66fa44c808243186c4d1', '1', '行', '行', 'admin', '2022-04-27 00:00:00'),
('excel-num', '9890c80bbbbf66fa44c808243186c4d1', '2', '列', '列', 'admin', '2022-04-27 00:00:00');


-- create excel_source
DROP TABLES IF EXISTS `excel_source`;

CREATE TABLE `excel_source` (
	`id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
	`name` varchar(80) COMMENT '原始名称',
	`store_name` varchar(100) COMMENT '存储名称',
	`md5_id` varchar(55) NOT NULL COMMENT 'md5-id',
	`rtx_id` varchar(25) NOT NULL COMMENT '用户rtx-id',
	`ftype` varchar(2) NOT NULL COMMENT '文件上传类型：1拆分;2合并',
	`local_url` varchar(120) COMMENT '文件本地资源路径（绝对路径）',
	`store_url` varchar(120) COMMENT '文件store对象存储资源路径（相对路径）',
	`numopr` int COMMENT '操作次数',
	`nsheet` int COMMENT 'sheet数',
	`set_sheet` varchar(30) COMMENT '当前设置的sheet选择索引，列表格式',
	`sheet_names` text COMMENT 'Sheets名称列表，以json方式存储',
	`sheet_columns` text COMMENT 'Sheets列名的集合，以json方式存储',
	`headers`text COMMENT 'excel的header信息，以json方式存储',
	`create_time` datetime COMMENT '创建时间',
	`delete_rtx` varchar(25) COMMENT '删除用户rtx',
	`delete_time` datetime COMMENT '删除时间',
	`is_del` bool DEFAULT False COMMENT '是否删除',
	PRIMARY KEY (`id`)
) COMMENT='Excel原始文件表';

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
	`create_time` datetime COMMENT '创建时间',
	`delete_rtx` varchar(25) COMMENT '删除用户rtx',
	`delete_time` datetime COMMENT '删除时间',
	`is_del` bool DEFAULT False COMMENT '是否删除',
	PRIMARY KEY (`id`)
) COMMENT='Excel转换成功记录表';

CREATE UNIQUE INDEX excel_result_index ON excel_result (`md5_id`);






