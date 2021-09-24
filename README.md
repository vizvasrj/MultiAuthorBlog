su postgres
psql -U <username> -d <database>
SELECT * FROM django_site;

CREATE TABLE django_site(
id serial PRIMARY KEY,domain VARCHAR (50) NULL,
name VARCHAR (50) NULL);

INSERT INTO django_site VALUES('1','mysite.com', 'mysite');

\q
