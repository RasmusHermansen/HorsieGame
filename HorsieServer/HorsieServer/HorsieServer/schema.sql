drop table if exists Sessions;
create table Sessions (
  id INTEGER primary key autoincrement,
  SessionName TEXT not null,
  IsActive INTEGER not null,
  Created TEXT  not null,
  Closed TEXT 
);

drop table if exists Users;
create table Users (
  id INTEGER primary key autoincrement,
  SessionId INTEGER not null,
  Alias TEXT not null,
  Standing REAL not null
);

drop table if exists Horses;
create table Horses (
  id INTEGER primary key autoincrement,
  SessionId INTEGER not null,
  Name TEXT not null,
  Speed REAL not null
);