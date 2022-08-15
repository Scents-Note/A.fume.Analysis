# api

Database로 부터 데이터를 가공 해 주는 api 패키지 입니다.

## 패키지 구성

```
 |-- .api
    |-- src
        |-- commmon
            |-- Object.py
            |-- SystemEnvironment.py
        |-- data
            |-- Ingredient.py
            |-- Note.py
            |-- Perfume.py
            |-- Serie.py
        |-- internal
            |-- entity
                |-- BrandEntity.py
                |-- IngredientCategoryEntity.py
                |-- IngredientEntity.py
                |-- NoteEntity.py
                |-- PerfumeEntity.py
                |-- SeriesEntity.py
            |-- sql
                |-- SqlModel.py
                |-- SqlUtils.py
        |-- repository 
            |-- IngredientRepository.py
            |-- KeywordRepository.py
            |-- NoteRepository.py
            |-- PerfumeRepository.py
            |-- SeriesRepository.py
        |-- Config.py
```

- src: 소스 폴더 패키지
  - common: 공통 으로 사용 되는 모듈을 모아 놓은 패키지
    - Object.py: Singleton 객체를 가지고 있음
    - SystemEnvironment.py: 환경 변수 관련 클래스
  - data: api에서 함수의 입출력으로 사용 되는 데이터 클래스
  - internal: api 내부 로직 수행을 위한 패키지
    - entity: db 테이블와 매핑 되는 Entity 클래스
    - sql: sql관련 패키지
      - SqlModel.py: CRUD를 수행 하는 model를 생성
      - SqlUtils.py: SQL 를 직접 수행하고 설정하는 클래스
    - repository: DB로 부터 값을 가져온 이후 가공 해서 반환 해주는 클래스
    - Config.py: api에서 사용 되는 환경 변수를 env파일로 부터 로드 

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

## API

### IngredientRepository

> 재료 이름 으로 재료 index 인덱스 조회

| api | get_ingredient_idx_by_name |
|:----|:---------------------------|
| 입력  | 재료(Ingredient) 이름          |
| 출력  | 재료(Ingredient) idx         |

```python
def get_ingredient_idx_by_name(name: str) -> int:
    pass
```

> 재료 카테고리 이름 으로 재료 카테고리 인덱스 조회

| api | get_category_idx_by_name        |
|:----|:--------------------------------|
| 입력  | 재료 카테고리(IngredientCategory) 이름  |
| 출력  | 재료 카테고리(IngredientCategory) idx |

```python
def get_category_idx_by_name(name: str) -> int:
    pass
```
 
> 특정 재료 리스트 조회

| api | get_ingredient_list |
|:----|:--------------------|
| 입력  | 재료 인덱스 리스트          |
| 출력  | 재료 리스트              |
    
```python
def get_ingredient_list(ingredient_idx_list: [int]) -> List[Ingredient]:
    pass
```

> 재료 정보 조회

| api | get_ingredient_info_list              |
|:----|:--------------------------------------|
| 입력  | None                                  |
| 출력  | [재료 정보](./src/data/Ingredient.py) 리스트 |


```python
def get_ingredient_info_list() -> List[IngredientInfo]:
    pass
```

```python
class IngredientInfo:
    def __init__(self, idx: int, name: str, description: str, series_idx: int, series_name: str, category_idx: int,
                 category_name: str, image_url: str):
        self.idx = idx
        self.name = name
        self.description = description
        self.series_idx = series_idx
        self.series_name = series_name
        self.category_idx = category_idx
        self.category_name = category_name
        self.image_url = image_url
```

### KeywordRepository

...

### NoteRepository

...

### PerfumeRepository

...

### SeriesRepository

...