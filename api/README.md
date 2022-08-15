# api

Database로 부터 데이터를 가공 해 주는 api 패키지 입니다.

## 패키지 구성

```
 |-- .api
    |-- src
```

- src: 소스 폴더 패키지


## 환경 변수

| environment   | description   | example                                      |
|:--------------|:--------------|:---------------------------------------------|
| MYSQL_USER    | mysql 유저 이름   | admin                                        |
| MYSQL_PASSWD  | mysql 비밀 번호   | **                                           |
| MYSQL_HOST    | mysql host    | localhost                                    |
| MYSQL_DB      | database 이름   | afume-db                                     |
| MYSQL_CHARSET | mysql charset | utf8                                         | 
| MYSQL_PORT    | mysql 포트 번호   | 3306                                         |
| READ_ONLY     | 읽기 전용         | 1 (1: READ_ONLY(default), 0: ALLOW TO WRITE) |