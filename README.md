# fastapi-postgres

FastAPIとPostgresql でWeb Server構築

## setup and how to

```sh
docker-compose up
```

## tips

* DBに接続する

```sh
docker-compose exec [サービス名] psql -U [ユーザー名] -d [データベース名]
```
