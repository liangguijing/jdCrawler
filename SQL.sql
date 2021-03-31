create database jingdong default charset utf8;
create user 'jingdong'@'%' identified by 'jingdong';
grant all privileges on jingdong.* to 'jingdong'@'%';
flush privileges;

use jingdong;
create table `items`
(
	`id` integer auto_increment,
	`keyword` char(48) not null,
	`pageIndex` char(8),
	`wareid` char(32),
	`shop_name` char(32),
	`warename` char(128),
	`color` char(128),
	`price` char(32),
	`totalsales` char(32),
	`good` char(32),
	`url` varchar(1024),
	`created` datetime default now(),
	primary key (`id`)
);

/*
--报错Authentication plugin 'caching_sha2_password' cannot be loaded
--执行下面语句
ALTER USER 'jingdong'@'%' IDENTIFIED WITH mysql_native_password BY 'jingdong';
flush privileges;
*/
