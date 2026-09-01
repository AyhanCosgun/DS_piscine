docker run --name my_postgres_container -e POSTGRES_PASSWORD=123 -d postgres &&
psql -h localhost -U postgres -d postgres -c "CREATE DATABASE my_database;" &&