create table article (
  id integer primary key,
  titre varchar(100),
  identifiant varchar(50),
  auteur varchar(100),
  date_publication text,
  paragraphe varchar(500)
);
create table users (
  id integer primary key,
  utilisateur varchar(25),
  email varchar(100),
  salt varchar(32),
  hash varchar(128)
);
create table sessions (
  id integer primary key,
  id_session varchar(32),
  utilisateur varchar(25)
);
create table tokens (
  id integer primary key,
  token varchar(128),
  email varchar(100)
);

insert into users values (1, 'correcteur', 'correcteur@gmail.com', '521d914b13dc4b3e891a5d05b72485f6', '299ebcf2cb3cd949b09221b71a9dded70b011fb599f4ad7e7775e07ab3c2781c9ba1e70447f581f7b0e82f2da8f63199ff495d447b90def3487d256b72377695');
