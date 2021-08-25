# CVAT_custom_model

## 커스텀 모델 구현을 위해 참고한 링크

>https://github.com/openvinotoolkit/cvat/blob/d8ab99c22f84718d853e1f4939abed24dd63a17e/docs/serverless_tutorial.md



## 커스텀 모델 구현을 위해 작성해야 하는 파일 목록

> main.py, function.yaml



### main.py

> 1. object detection 모델의 github 페이지의 demo.py, test.py 등 모델 시연을 위한 코드를 http Response로 구현한 파일. init_context와 handler 메소드로 구성됨
> 2. init_context의 경우 cfg파일과 weight파일을 이용해 객체 검출에 사용될 모델을 생성하고 이후에 기술할 function.yaml의 레이블 정보를 불러와 함수 인자로 받은 context에 입력해주는 메소드임.
> 3. handler의 경우 인자로 받은 event에서 이미지를 추출하여 모델을 통과시켜 얻은 결과값을 레이블에 맞춰 재가공한 뒤, json으로 변환하여 반환하는 메소드

### function.yaml

> 1. 크게 모델의 레이블 데이터 부분과 nuclio로 기능을 구현할때 초기 세팅 부분으로 나누어져 있음.
> 2. 이외의 부분들은 description으로 크게 상관하지 않아도 됨
> 3. 현재 spec-build-directives-preCopy부분에서 지속적인 오류가 발생하고 있음



## 그 외 중요 사항

### custom model 함수 deploy

> 26번 서버의 sungmin(pwd: 9939tjdals)에서 다음 명령어를 작성하면 됨.
>
> > ./nuctl-1.5.8-linux-amd64 deploy --project-name cvat --path cvat/serverless/pytorch/yolov4/ --platform local
>
> 