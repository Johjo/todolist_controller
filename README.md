git-gamble : 

- for powershell
```
$env:GAMBLE_TEST_COMMAND='pytest -vv'
```

Lancer une image postgres pour la base de données
```shell
docker run --name todolist_db -e POSTGRES_PASSWORD=mysecretpassword -d postgres:17.4-alpine
```

