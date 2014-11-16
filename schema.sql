drop table if exists snacks;
create table snacks (
  id integer primary key autoincrement,
  name text not null,
  type text not null,
  date datetime not null,
  cost double
);