# 난독화된 한글 리뷰 복원 AI 경진대회 (현재 진행중)

![화면 캡처 2025-01-16 080717](https://github.com/user-attachments/assets/b6203832-2223-49e1-8cf6-bdcad267d21b)

## 프로젝트 소개
이 저장소는 난독화된 한국어 텍스트를 원문으로 복원하기 위한 시스템을 구현한 프로젝트입니다. ChatGPT, Gemini 그리고 오픈소스 모델인 LLaMA, EXAONE, GEMMA 등을 활용하여 왜곡된 한국어 문장을 원래 형태로 복원합니다. 또한, 오픈소스 모델들을 데이터셋에 맞게 **파인튜닝**하여 특정 도메인에 최적화된 결과를 제공합니다. 텍스트 복원은 리뷰 데이터나 자연어 처리 작업에서 품질을 높이는 데 활용될 수 있습니다.

---

## 주요 기능

### 1. **자동 텍스트 복원**
- 난독화된 한국어 문장을 분석하여 원문으로 복원.
- ChatGPT, Gemini, LLaMA, EXAONE, GEMMA 모델을 사용.
- 오픈소스 LLM 도메인에 최적화된 모델로 파인튜닝
### 2. **유연한 설정**
- 사용자 정의 문자 매핑 및 복원 패턴 적용.
- 추가 데이터셋 통합 및 확장 가능.

### 3. **문자 및 문장 패턴 기반 분석**
- 잘못된 자음/모음 및 띄어쓰기 수정.
- 문맥 기반 문장 구조 복원.

---

## 파일 설명

### 1. `chatgpt.py`
- OpenAI GPT 모델을 사용하여 텍스트를 복원하는 스크립트.
- 주요 기능:
  - **TextRestorationSystem** 클래스 구현.
  - 문자 매핑 및 자주 발생하는 문장 패턴 정의.
  - 테스트 샘플을 복원하고 정확도 평가.

### 2. `gemini.py`
- Google Gemini AI 모델을 사용하여 텍스트를 복원하는 스크립트.
- 주요 기능:
  - **Gemini Generative AI 모델** 활용.
  - 예제 데이터를 기반으로 복원 결과 생성 및 비교.

### 3. `finetuning.ipynb` & `opensource-models.ipynb`
- 데이터 전처리, 추론 과정 포함.
- 오픈소스 모델(LLaMA, EXAONE, GEMMA 등)을 특정 데이터셋에 맞게 파인튜닝한 과정 포함.
- LLaMA 3.1 8B 모델로 파인튜닝 시:
 - Training Loss: 1.360500	
 - Validation Loss: 1.385290
 - 안정적으로 수렴하며 높은 복원 성능을 보임.
---

## 설치 방법

### 1. 환경 설정
```bash
git clone https://github.com/bigdefence/Restoration-of-obfuscated-Korean.git
cd Restoration-of-obfuscated-Korean
```

### 2. API 키 설정
`.env` 파일 생성 후 아래와 같이 추가:
```
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

## 사용 방법

### OpenAI GPT 모델로 복원 실행
```bash
python chatgpt.py
```

### Google Gemini 모델로 복원 실행
```bash
python gemini.py
```
### Opensource 모델로 복원 실행
```bash
opensource-model.ipynb 실행
```
---

## 예제

### 입력:
```
좋앝다. 이 방 진짜 깥을만했어요.
```

### 출력:
```
좋았다. 이 방 진짜 같을만했어요.
```

---

## 향후 계획
- 강화된 문장 패턴 분석 알고리즘.
- 오픈소스 모델 기반의 더 많은 도메인 특화 파인튜닝.
- API 서비스 배포 및 실시간 텍스트 복원.

---


