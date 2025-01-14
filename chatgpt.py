from dotenv import load_dotenv
import openai
import os
import pandas as pd
import random
from typing import List, Dict, Tuple
import json
from collections import defaultdict

class TextRestorationSystem:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.char_mapping = self._initialize_char_mapping()
        self.common_patterns = self._initialize_common_patterns()
        
    def _initialize_char_mapping(self) -> Dict:
        """자주 발생하는 문자 변환 패턴 초기화"""
        return {
            '깥': '같', '맒': '말', '섧': '설', '멍': '명', '탯': '댓',
            '녀': '너', '퀼': '길', '윌': '일', '귑': '기', '낙': '나',
            '콧': '곳', '잚': '잠', '갉': '갈', '좋': '좋', '잇': '있',
            '앎': '알', '톨': '돌', '깸': '캠', '읊': '을', '앝': '아'
        }
        
    def _initialize_common_patterns(self) -> List[Dict]:
        """자주 발생하는 문장 패턴 초기화"""
        return [
            {
                'pattern': r'좋([꾜앝])',
                'replacement': '좋아'
            },
            {
                'pattern': r'([가-힣])씁니다',
                'replacement': r'\1습니다'
            },
            {
                'pattern': r'([가-힣])엇([어요])',
                'replacement': r'\1었\2'
            }
        ]

    def _create_system_prompt(self, examples: List[Tuple[str, str]]) -> str:
        """시스템 프롬프트 생성"""
        prompt = (
            "당신은 난독화된 한국어 텍스트를 원문으로 복원하는 전문가입니다. "
            "다음의 규칙과 패턴을 참고하여 텍스트를 복원하세요:\n\n"
            "1. 자음/모음 대체 패턴:\n"
            "- ㅏ→ㅑ, ㅓ→ㅕ 등의 변환이 자주 발생\n"
            "- 받침의 경우 ㄱ→ㄲ, ㄹ→ㄷ 등으로 변환\n\n"
            "2. 단어 구조:\n"
            "- 기본 형태는 유지되나 자음/모음이 변형됨\n"
            "- 띄어쓰기는 대체로 원문과 유사하게 유지됨\n\n"
            "3. 문맥 고려사항:\n"
            "- 리뷰 텍스트의 특성을 반영 (숙소, 음식점 등)\n"
            "- 감정 표현과 평가 내용의 일관성 유지\n\n"
            "예시:\n"
        )
        
        for input_text, output_text in examples[:5]:  # 5개 예시만 사용
            prompt += f"입력: {input_text}\n출력: {output_text}\n\n"
            
        return prompt

    def _analyze_patterns(self, text: str) -> Dict:
        """텍스트의 주요 패턴 분석"""
        patterns = {
		    'special_chars': list(c for c in text if not c.isalnum() and c not in ' .,!?'),
		    'repeated_chars': [],
		    'word_endings': []
		}

        
        words = text.split()
        for word in words:
            # 반복되는 문자 패턴 찾기
            for i in range(len(word)-1):
                if word[i] == word[i+1]:
                    patterns['repeated_chars'].append(word[i:i+2])
                    
            # 단어 끝 패턴 찾기
            if len(word) > 2:
                patterns['word_endings'].append(word[-2:])
                
        return patterns

    def restore_text(self, input_text: str, examples: List[Tuple[str, str]] = None) -> str:
        """텍스트 복원 메인 함수"""
        # 시스템 프롬프트 생성
        system_prompt = self._create_system_prompt(examples)
        
        # 입력 텍스트 패턴 분석
        patterns = self._analyze_patterns(input_text)
        
        # GPT 요청을 위한 메시지 구성
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": (
                    f"다음 텍스트를 복원하세요. 분석된 패턴 정보도 참고하세요:\n"
                    f"입력 텍스트: {input_text}\n"
                    f"발견된 패턴: {json.dumps(patterns, ensure_ascii=False)}\n"
                    "복원 시 다음을 주의하세요:\n"
                    "1. 띄어쓰기는 원문의 패턴을 최대한 유지\n"
                    "2. 특수문자와 문장 부호는 자연스럽게 변환\n"
                    "3. 존댓말/반말 등의 말투는 문맥에 맞게 유지"
                )
            }
        ]

        try:
            completion = openai.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,  # 일관성을 위해 낮은 temperature 사용
                top_p=0.8,
            )
            
            restored_text = completion.choices[0].message.content.strip()
            
            # 후처리: 불필요한 설명이나 따옴표 제거
            restored_text = restored_text.replace('복원 결과: ', '')
            restored_text = restored_text.strip('"\'')
            
            return restored_text
            
        except Exception as e:
            print(f"Error in text restoration: {e}")
            return input_text

def main():
    # 환경 설정
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # 데이터 로드
    train = pd.read_csv('./open/train.csv', encoding='utf-8-sig')
    
    # 시스템 초기화
    system = TextRestorationSystem(OPENAI_API_KEY)
    
    # 학습 예제 준비
    examples = []
    sample_size = min(20, len(train))
    for i in range(sample_size):
        examples.append((train['input'][i], train['output'][i]))
    
    # 테스트 실행
    random_indices = random.sample(range(len(train)), 5)
    correct_count = 0
    
    for j, idx in enumerate(random_indices, start=1):
        query = train['input'][idx]
        expected_output = train['output'][idx]
        
        try:
            result = system.restore_text(query, examples)
            
            # 결과 평가
            is_correct = result.strip() == expected_output.strip()
            if is_correct:
                correct_count += 1
            
            print(f"\n{j}번째 샘플")
            print(f"복원 결과: {result}")
            print(f"정답: {expected_output}")
            print(f"정확도: {'일치' if is_correct else '불일치'}")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error processing sample {j}: {e}")
    
    # 최종 정확도 출력
    print(f"\n전체 정확도: {(correct_count/5)*100:.2f}%")

if __name__ == "__main__":
    main()