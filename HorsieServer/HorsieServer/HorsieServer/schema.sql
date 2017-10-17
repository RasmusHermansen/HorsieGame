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
  Knot1 REAL not null,
  Knot2 REAL not null,
  Knot3 REAL not null,
  Knot4 REAL not null,
  Knot5 REAL not null,
  Knot6 REAL not null
);

drop table if exists Actions;
create table Actions (
  id INTEGER primary key autoincrement,
  SessionId INTEGER not null,
  RunId INTEGER not null,
  UserId INTEGER not null,
  ActionType TEXT not null,
  IdForActionType INTEGER not null
);

drop table if exists Bets;
create table Bets (
  id INTEGER primary key autoincrement,
  Odds REAL not null,
  Amount REAL not null,
  HorseId INTEGER not null
);

drop table if exists Interactions;
create table Interactions (
  id INTEGER primary key autoincrement,
  Interaction TEXT not null,
  Value REAL not null
);
