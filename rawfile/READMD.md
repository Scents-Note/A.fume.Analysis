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