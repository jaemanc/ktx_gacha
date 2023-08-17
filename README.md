# ktx_gacha

---

## settings
* python 3.8
* django 
* selenium
* DB 안씁니다


---

## 러프한 일정
* 8월 중 전체 기능 1차 테스트
* 8월 말 전체 기능 연계
* 9월 초 카카옷 챗봇 연동
---

# ***Todo***
### process
1. 플로우 차트
2. 티켓 검색 조건 (to - go, 날짜,좌석, 등급, 인원)
2. 실제 예약까지 소요 시간
3. 리소스 필요 정도

### code level
1. 요청 URL hard coding 제거
2. tag id 등 바뀔 경우 어떻게 대처 할 지 고민 필요.
3. 공통으로 사용 할 Response 형식 정의 필요. 일관된 형식으로 리턴해야 함.
4. ~~Selenium 속도 향상 ( 특히 목록 조회 )~~
5. 예약 대기로 인한 리소스 사용량? 예약 대기 시간?
6. 예약 반복 할 때 페이지 이동 이후 에러 시 대처가 안됨.. ㅜ

### 매크로 기능
1. ~~로그인~~ 
2. ~~목록 조회~~
3. ~~조건에 따른 타겟 선정~~
4. 예약을 위한 검색 반복 - 선택 결제 대기 또는 장바구니 ( 20 분 내로 결제 필요 )
5. 알림 카카오 챗봇

###  예약
1. 예약 방식 <br>
   1. 출발 시간(필수) + 차종(선택) + 객실 유형(선택) + 인원(필수) + 알림 받을 사용자 정보 <br>
   2. 20분 이내의 열차는 사이트에서 예약이 안됨.
2. ~~직접 결제는 복잡하므로 장바구니로 진행.~~ <br>
   1. ~~장바구니에 정상적으로 담겼을 경우 - 사용자 알림.~~ <br>
   2. ~~조회 - 예약 - 알림 순~~ <br>
   3. ~~알림 - 카카오 챗봇 ( 월 1000건 무료)~~<br>
2. 장바구니 없이 예매 버튼만 눌러도 발권 예약 탭으러 표가 넘어감
3. 2인 이상일 경우 좌석 선택 방식 확인 필요.  __차후 구현 예정__
   1. 붙어서 선택 <br>
   2. 나뉘어서 선택.<br>
   3. 창측, 통로층, 역방향, 순방향 등 옵션 많음. + 특실/우등실 , 일반실 <br>
4. 하나만 선택하던지, 범위에 해당하는 표를 선택하던지. <br>
   1. 표를 어떤 기준으로 선택하는지 확인 필요 ( 예약 요청 기준 ) -- gacha니까 랜덤으로 주는것도 방법인가 <br>
   2. 특정 시간대를 하나 설정 ( 정각 기준 ) 이후 8~9개 정도의 시간표가 나오는데 보통 선택 시간과 3시간 정도 차이가 나는 듯 ( 역마다 다름 ) <br> 
    <br>



### 프로젝트 세팅
1. env 설정으로 코드값들 변경
2. DB 사용 X

### 사용자 연계
1. 외부 API 연동 ( 카카오 채널 또는 슬랙 )

---

### TEST postman settings

https://buildabetterworld.tistory.com/75

![img.png](img.png)
![img_1.png](img_1.png)


---

### Flow chart
![image](https://github.com/jaemanc/ktx_gacha/assets/104718153/e993b595-bb60-4e68-8bc1-9d2a8ff4f28d)




