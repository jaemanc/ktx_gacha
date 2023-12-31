# ktx_gacha

###  카카오채널 챗봇과 연동한 ktx 예매 매크로 입니다. 

__Blog__ : https://girinprogram93.tistory.com/108 
<br>
__Contact__ : jaemanc93@gmail.com

---
<p align="center">

<img src= "https://github.com/jaemanc/ktx_gacha/assets/104718153/cc030dda-eecf-4972-a2ea-cd7e4b981371" align="center" width="32%">
<img src= "https://github.com/jaemanc/ktx_gacha/assets/104718153/167f77b2-bf02-410a-bd08-374116ceef38" align="center" width="32%">
<img src= "https://github.com/jaemanc/ktx_gacha/assets/104718153/2e80618f-2bc1-4fbe-af8f-31896383d2bb" align="center" width="32%">

</p>

<p align="center">

<img align="center" width="20%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/a296533a-b2a8-41a9-b78c-cfbaca9066d0">
<img align="center" width="20%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/e631714a-93f8-4895-a950-82a8ffa46c71">
<img align="center" width="20%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/b2b7f5ac-6092-4f00-a8e8-fd6735a89904">
<img align="center" width="20%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/24b739e1-a37e-4b76-ba39-8aeb27f4359e">
<img align="center" width="15%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/ea662a69-ef50-49fb-911d-59be44aacdc8">


</p>

---

### 로그인

<div style="display: flex; align-items: center;">
   <img width="25%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/7c24c875-adf2-4d2a-ade8-4828bff03c6b" style="margin-right: 20px;">
   <br>
   <h4> 카카오 채널 + 챗봇을 통해 멤버십 번호와 비밀번호로 로그인 합니다. </h4>
</div>

<br>

### 조회

<div style="display: flex; align-items: center;">
   <img width="25%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/384c3cc3-a144-4b4d-be4b-e1b23db883ea">
   <img width="25%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/d7fc6425-2bee-4b01-8324-56d5b644efa1">
   <br>
   <h4> 로그인 이후 조회요청을하고 챗봇 callback 기능을 통해 조회 목록으로 응답합니다. </h4>
</div>

<br>

### 예매

<div style="display: flex; align-items: center;">
   <img width="25%" alt="image" src="https://github.com/jaemanc/ktx_gacha/assets/104718153/bc8c81d0-cc16-4121-9c17-7e71773c2972">
   <br>
   <h4> 30분 제한으로 표를 반복해서 서치합니다. 예매 가능한 표가 있을 경우 예매요청과 발화자에게 이메일로 예매 사항을 알려줍니다. </h4>
</div>



---


## settings
* Python 3.8
* Django 
* Selenium
* Github actions ci/cd 
* Oracle Cloud - ubuntu os 사용 필요 / google chrome 설치 선행 필요 
* Docker 


---

## 일정
* ~~8월 29일 기준 기능 구현 및 챗봇 연동 종료.~~
* ~~8월 중 전체 기능 1차 테스트~~
* ~~8월 말 전체 기능 연계~~
* ~~9월 초 카카옷 챗봇 연동~~
---

# ***Todo***
### process
1. ~~플로우 차트~~
2. ~~티켓 검색 조건 (to - go, 날짜,좌석, 등급, 인원)~~
3. ~~실제 예약까지 소요 시간? 표 유무에 따라 다름~~
4. ~~리소스 필요 정도 <- 어차피 오라클 클라우드 무료버전이라 리소스를 따질 방법이 없어요..~~

### code level
1. ~~요청 URL hard coding 제거~~
2. __tag id 등 바뀔 경우 어떻게 대처 할 지 고민 필요.__
3. __공통으로 사용 할 Response 형식 정의 필요. 일관된 형식으로 리턴해야 함.__
4. ~~Selenium 속도 향상 ( 특히 목록 조회 )~~
5. __예약 대기로 인한 리소스 사용량? 예약 대기 시간?__
6. ~~예약 반복을 위한 Thread 처리 필요.~~

### 매크로 기능
1. ~~로그인~~ 
2. ~~목록 조회~~
3. ~~조건에 따른 타겟 선정~~
4. ~~예약을 위한 검색 반복 - 선택 결제 대기 또는 장바구니 ( 20 분 내로 결제 필요 )~~
5. ~~알림 카카오 챗봇 <- 챗봇 테스트 사용까지 심사기간이 5일 정도 소요~~
   1. ~~5초 이상 시간이 걸릴 경우, callback기능이 필요한데 AI챗봇으로 전환이 필요함.~~
   2. ~~무료 MMS 발송 방식으로 수정. <- SMTP 를 사용한 이메일 알림으로 구현~~

###  예약
1. 예약 방식 <br>
   1. ~~출발 시간(필수) + 차종(선택) + 객실 유형(선택) + 인원(필수) + 알림 받을 사용자 정보~~ <br>
   2. ~~20분 이내의 열차는 사이트에서 예약이 안됨.~~
2. ~~직접 결제는 복잡하므로 장바구니로 진행.~~ <br>
   1. ~~장바구니에 정상적으로 담겼을 경우 - 사용자 알림.~~ <br>
   2. ~~조회 - 예약 - 알림 순~~ <br>
   3. ~~알림 - 카카오 챗봇 ( 월 1000건 무료)~~<br>
3. ~~장바구니 없이 예매 버튼만 눌러도 발권 예약 탭으러 표가 넘어감~~
4. 2인 이상일 경우 좌석 선택 방식 확인 필요.  __차후 구현 예정__
   1. 붙어서 선택 <br>
   2. 나뉘어서 선택.<br>
   3. 창측, 통로층, 역방향, 순방향 등 옵션 많음. + 특실/우등실 , 일반실 <br>
5. 하나만 선택하던지, 범위에 해당하는 표를 선택하던지. <br>
   1. 표를 어떤 기준으로 선택하는지 확인 필요 ( 예약 요청 기준 ) -- gacha니까 랜덤으로 주는것도 방법인가 <br>
   2. 특정 시간대를 하나 설정 ( 정각 기준 ) 이후 8~9개 정도의 시간표가 나오는데 보통 선택 시간과 3시간 정도 차이가 나는 듯 ( 역마다 다름 ) <br>
   3. ~~예약시 조회되는 테이블 컬럼 개수 다 다르고, 테이블 자체가 안나올 수가 있음. 예외 처리가 많이 되어야 함.~~
    <br>



### 프로젝트 세팅
1. ~~env 설정으로 코드값들 변경~~
2. ~~DB 사용 X~~


### 사용자 연계
1. ~~외부 API 연동 ( 카카오 채널 )~~
2. ~~카카오 챗봇 시나리오 필요. (api 스킬의 경우 서버와 통신 타임아웃이 5초) <- AI 챗봇연동으로 콜백 기능으로 구현함.~~
   1. ~~로그인~~
   2. ~~조회~~
      1. ~~조회는 문제가 없으나 5초 안에 처리해줘야 함..~~
      2. ~~아무래도 조회 단계는 건너뛰고 예약만 처리해야 할 듯. 5초 내로 하기에는 클라우드 서버의 리소스가 부족한 듯~~ 조회 예매 동시 구현으로 처리함.
      3. ~~AI 챗봇으로 콜백으로 1분 내에 처리 해줘야 함. 조회와 같은 경우 조회 사항은 콜백으로 처리하는 게 좋을 듯함.~~
3. ~~예약 후 알림 (SMTP 사용.)~~

---

### TEST postman settings

https://buildabetterworld.tistory.com/75

![img.png](img.png)
![img_1.png](img_1.png)


---

### Flow chart
![image](https://github.com/jaemanc/ktx_gacha/assets/104718153/e993b595-bb60-4e68-8bc1-9d2a8ff4f28d)

---


## 동작 예시 
[ARCHIVE.md](ARCHIVE.md)
## docker command 모음
[DOCKER_COMMAND.md](DOCKER_COMMAND.md)

---

