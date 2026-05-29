FROM mysql:8.0.36

#Run init files for db
COPY init.sql /docker-entrypoint-initdb.d/init.sql
COPY views.sql /docker-entrypoint-initdb.d/views.sql
COPY procedures.sql /docker-entrypoint-initdb.d/procedures.sql