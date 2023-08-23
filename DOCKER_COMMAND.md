# Docker command 정리

## OCI + ubuntu 18

###  ssh 접속 
$ ssh -i "/Users/jamal/dev/toy_workspace/ssh-key-2023-08-21.key" ubuntu@131.???.27.???


### docker 설치
$ sudo apt-get update <br>
$ sudo apt-get install -y \ <br>
    apt-transport-https \ <br>
    ca-certificates \ <br>
    curl \ <br>
    software-properties-common <br><br>

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

$ sudo apt-get update

$ sudo apt-get install -y docker-ce docker-ce-cli containerd.io


### docker run / 자동시작 설정
$ sudo systemctl start docker
$ sudo systemctl enable docker


### 버전 체크 
$ sudo docker --version



### chrome 설치
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i google-chrome-stable_current_amd64.deb


### docker login
$ docker login 


### build
$ docker build -t jaemanc/ktx-gacha-for-ubuntu:latest . <br>
$ sudo docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/${{secrets.DOCKER_REPO}} .

### push
$ docker push jaemanc/ktx-gacha-for-ubuntu:latest

### RUN 
$ docker run --name ktx-gacha-for-ubuntu -d -e SECRET_KEY='${{secrets.SECRETS_KEY}}' -p 8000:8000 jaemanc/ktx-gacha-for-ubuntu:latest

### ps 조회
$ docker ps -all

### 재실행 
$ docker restart 

### log 조회 ( container id )
$ docker logs -f d14d5e9afaf1

### docker ps 종료 
$ sudo docker rm -f $(docker ps -qa)

### 종료 시 permission 문제 생길 경우 : 
$ groups $계정명 -> <br>  sudo groupadd docker. -> 
<br> $ sudo usermod -aG docker $계정명 -> 
<br> 터미널 재 연결 -> 
<br> 재연결 이후에도 에러 일 경우 파일 그룹 지정 ( $ sudo chown root:docker /var/run/docker.sock ) -> 
<br> 실행 권한 변경 $ sudo chmod 666 /var/run/docker.sock










