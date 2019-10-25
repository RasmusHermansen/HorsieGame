drop table if exists Sessions;
create table Sessions (
  id INTEGER primary key autoincrement,
  SessionName TEXT not null,
  SessionKey TEXT not null,
  IsActive INTEGER not null,
  Created TEXT  not null,
  Closed TEXT 
);

drop table if exists Users;
create table Users (
  id INTEGER primary key autoincrement,
  SessionId INTEGER not null,
  UserKey TEXT not null,
  IsActive INTEGER not null,
  Alias TEXT not null,
  Standing REAL not null
);

drop table if exists Horses;
create table Horses (
  id INTEGER primary key autoincrement,
  SessionId INTEGER not null,
  Name TEXT not null,
  HorseClass TEXT not null,
  Knot1 REAL not null,
  Knot2 REAL not null,
  Knot3 REAL not null,
  Knot4 REAL not null,
  Knot5 REAL not null,
  Knot6 REAL not null,
  ProbAction1 BOOLEAN not null,
  ProbAction2 BOOLEAN not null
);

drop table if exists Bets;
create table Bets (
  id INTEGER primary key autoincrement,
  SessionId INTEGER not null,
  UserId INTEGER not null,
  HorseId INTEGER not null,
  Odds REAL not null,
  Amount REAL not null,
  Handled BOOLEAN not null
);