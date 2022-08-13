# rawfile

Database에 존재하는 여러 정보(table)을 하나의 Raw Excel로 변환 해주는 Tool 입니다.

## 패키지 구성

```
 |-- .rawfile
    |-- out
    |-- script
        |-- build.sh
        |-- run.sh
    |-- src
```

- out: pyinstaller에 의해 생성 되는 결과 폴더
- script: 스크립트 폴더
    - build.sh: pyinstaller 를 이용 하여 실행 파일 만드는 스크립트
- src: 소스 폴더 패키지

## 환경 변수

| environment     | description       | example                                                   |
|:----------------|:------------------|:----------------------------------------------------------|
| INPUT_DIR_PATH  | 입력 excel 파일 경로    | /Users/mac/github/A.fume.Analysis/rawfile/input           |
| OUTPUT_DIR_PATH | 출력 excel 저장 파일 경로 | /Users/mac/github/A.fume.Analysis/rawfile/output          |
| TARGET          | 가져 오려고 하는 정보      | (ingredient_info,perfume_info,brand_info,series_info 중 1) |
| COMMAND         | 수행 하는 작업의 종류      | db2excel 또는 excel2db                                      |
