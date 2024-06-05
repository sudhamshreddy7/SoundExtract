create user 'auth_user'@'localhost' identified by 'AUTH@123';
create database auth;
GRANT ALL PRIVILEGES ON AUTH.* TO 'auth_user'@'localhost';
use auth;
create table user(
    id int not null auto_increment primary key,
    email varchar(255) not null Unique,
    password varchar(255) not null
);
insert into user(email,password) VALUES("abc@gmail.com","abc");
