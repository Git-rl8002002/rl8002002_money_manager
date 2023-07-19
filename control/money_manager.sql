/*
 * database  scraping
 */ 
create database money_manager DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use money_manager;

/*
 * m_m_a
 */ 
create table m_m_a(
no int not null primary key AUTO_INCREMENT, 
s_time datetime null,
a_user varchar(200) null,
a_pwd varchar(200) null,
a_status varchar(20) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*
 * m_m_log
 */ 
create table m_m_log(
no int not null primary key AUTO_INCREMENT, 
s_time datetime null,
e_time datetime null,
a_user varchar(50) null,
content text null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*
 * m_m_r
 */ 
create table m_m_r(
no int not null primary key AUTO_INCREMENT, 
s_time date null,
r_year varchar(30),
r_month varchar(30),
r_day varchar(30),
a_user varchar(50) null,
r_kind varchar(50) null,
r_title varchar(100) null,
r_money varchar(100) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




