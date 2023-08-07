import logging

# asctime   : 로그 기록 시간
# filename  : 파일 이름
# lineno    : 라인 번호
# funcName  : 함수 이름
# message   : 메시지


def prevent_duplicate(logger):
    # 로그 메시지 중복 방지
    logger.propagate = False
    if logger.hasHandlers():
        logger.handlers.clear()


logger1 = logging.getLogger(__name__)
logger1.setLevel(logging.DEBUG)  # 경고 수준 설정
prevent_duplicate(logger1)

logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.DEBUG)  # 경고 수준 설정
prevent_duplicate(logger2)

formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s|%(levelname)s] %(funcName)s(): %(message)s')

stream_handler = logging.StreamHandler()  # 스트림 핸들러 생성
stream_handler.setFormatter(formatter)  # 텍스트 포맷 설정
logger1.addHandler(stream_handler)  # 핸들러 등록

file_handler = logging.FileHandler('debug.log', mode='w')  # 파일 핸들러 생성
file_handler.setFormatter(formatter)  # 텍스트 포맷 설정
logger2.addHandler(file_handler)  # 핸들러 등록
