# backend-BIEN

MAIN GOALS:
-Use this skeleton back-end to replicate bien-data.org functionality
-Build the front-end agnostic to BIEN API representations

TO-DO:
-Find out how to transfer viewport information inside queries
	-Use viewport information for PostGIS spatial queries
-Create routes for political boundaries
-Create routes for traits
-Integrate backend functionality with Chamberlain's BIEN API

## Build Azure database
az postgres server firewall-rule create --resource-group BIEN --server-name vegbien --start-ip-address=0.0.0.0 --end-ip-address=0.0.0.0 --name AllowAllAzureIPs
  
## Set privileges on empty tablespace folder with 'chown postgres:postgres biendb' first
```
create tablespace biendb owner bien location '/media/ssd';
CREATE DATABASE public_vegbien with tablespace biendb;
\c public_vegbien
CREATE SCHEMA public;

CREATE EXTENSION postgis;
CREATE SCHEMA postgis;

UPDATE pg_extension SET extrelocatable = TRUE WHERE extname = 'postgis'; 
ALTER EXTENSION postgis SET SCHEMA postgis;

REVOKE ALL ON DATABASE public_vegbien FROM PUBLIC;
ALTER DATABASE public_vegbien OWNER TO bien;
GRANT ALL PRIVILEGES ON DATABASE public_vegbien TO bien;

GRANT USAGE ON SCHEMA postgis TO bien;
GRANT SELECT ON ALL TABLES IN SCHEMA postgis TO bien;

ALTER SCHEMA public OWNER TO bien;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO bien;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO bien;

ALTER DATABASE public_vegbien SET search_path = public,postgis;

#May need to specify a port number as well
pg_restore -x -U bien -h localhost -d public_vegbien -n public bien_adb_public.pgd

#Useful commands
'server.py' is the entry point.
DON'T FORGET export FLASK_APP=server.py !!!
python3 server.py
flask run

Note: We don't plan on performing migrations because we are only reading from the database
General workflow:
-Change database representations -> 
perform a migration: flask db migrate (sometimes push code to production server)  then: flask db upgrade

Undo migration (migrating twice to go backwards is probably not ideal)
after upgrade: flask db downgrade 
then delete the obsolete migration script in '/versions', revise your code, and migrate as usual. Obviously, to revert changes, revert your code

DONE:
-Attach BIEN postgresql to Flask
---Migrate to Flask/SQLAlchemy and a postgres thingy
-Figure out how to read-only using ORM.
	-can't reflect database contents into the database connection
	-Reflect table data to objects (FLASK)
-construct an ORM representation (initialize an object from a class) based on a query/request from the database (use session.query(class))
-Set up route for species to query the table class ORM thingy, response as JSON

--Find out how to query occurrences with sqlalchemy based on a species name
	-Route a species name through the taxon table to get the foreign key species_taxon_id

-Find out how to decorate route function to accept a species name from a request
	-Properly parse spaces in URLs

-Find out how to bind multiple schema so that we can integrate postgis (used geoalchemy2 as an interface)