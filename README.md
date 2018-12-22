# backend-BIEN

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


