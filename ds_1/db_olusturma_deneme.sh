docker run --name postgres-test \
  -e POSTGRES_PASSWORD=test123 \
  -p 5432:5432 \
  -d postgres:14

  psql -h localhost -p 5432 -U postgres -d postgres