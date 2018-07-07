Introduction
------------
Program Y를 사용한 rule base 챗봇입니다.
Program Y에 관한 사항은 `Program Y Wiki <https://github.com/keiffster/program-y/wiki>`_ 참고하시면 됩니다.
Program Y에서 Y-Bot을 이용하였고 효과적인 문장 인식을 위하여 전통적인 텍스트 분류에 사용되어지는 나이브베이즈 분류를 이용하였습니다.
인식하고자 하는 문장과 그에 해당하는 대답을 aiml파일로 작성시 손쉽게 해당 답변이 구현가능하며,
서버에서 구동시 flask를 이용하여 restful하게 이용가능합니다.

Tutorial
---------
 - chatbot/src 구조에서 소스 수정이 가능합니다.
 - chatbot/src/programy/clients/restful/classification.py에 소스는 나이브 베이즈 분류가 적용되어있습니다.
   1. 처음 실행시 2번째 줄에 주석을 해제하여 nltk를 다운로드 받아합니다.
   2. 서버에서 구동시 12번째 줄 self.base_path를 서버 절대경로로 바꿔주셔야 구동가능합니다.
      (여기에서 가리키는 base_path인 conversation은 인식하고자 하는 대화를 작성하는 파일입니다.)
 - chatbot/src/programy/conversation 파일에 카테고리에 해당하는 대화를 입력합니다.


 새로운 대화 파일 추가
  1. 새로 카테고리를 추가하고자 할 경우 chatbot/src/programy/conversation파일 안에 파일제목을 카테고리와 동일하게 작성, 대화를 추가합니다.
  2. chatbot/src/programy/clients/restful/client.py에 classify()함수가 구현되어 있는 데,
     이는 질문 시에 질문한 질문이 어떤 카테고리의 질문인지 분류해주므로 새로운 카테고리 작성시 분기점에서 파일 제목과 동일한 형태로
     분기를 시켜야 합니다. 분기를 시키게 되면 질문에 대한 카테고리를 high_class로 반환하게 됩니다.
  3. chatbot/bots/y-bot/aiml/conversation에 해당 카테고리에 관한 질문을 aiml형태로 작성합니다.
     aiml 작성 시에 high_class에서 반환되어지는 값을 pattern에 입력하여야 답변이 가능합니다.
     aiml 작성 관련 내용은 `https://www.tutorialspoint.com/aiml/index.htm`_ 참고하시면 됩니다.

  실행
  - Mac OSX
    chatbot/bots/y-bot/y-bot-flask-rest.sh를 이용하여 실행이 가능합니다.

  - Windows
    Pycharm IDE를 통하여 구동가능하며, 구동시 chatbot/src를 source root로 지정하여야 합니다.
    chatbot/src/programy/clients/restful/flask/client.py를 실행시킨 후
    브라우저에 localhost:8989/api/rest/v1.0/ask?question=질문내용 으로 실행가능합니다.







