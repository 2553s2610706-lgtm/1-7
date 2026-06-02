import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="Self-Care Chatbot", page_icon="🌱")

st.title("🌱 나의 자기 관리 어시스턴트")
st.caption("건강한 습관, 멘탈 케어, 일상 관리를 다정하게 도와주는 챗봇입니다.")

# 2. API 키 설정 (Secrets에서 불러오기)
try:
    # st.secrets를 통해 안전하게 키를 불러옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("🚨 API 키가 설정되지 않았습니다. Streamlit Secrets에 'GEMINI_API_KEY'를 추가해주세요.")
    st.stop()

# 3. 모델 초기화 및 시스템 프롬프트 설정
# 챗봇의 성격과 역할을 부여합니다.
system_instruction = """
당신은 사용자의 자기 관리를 돕는 다정하고 실용적인 어시스턴트입니다. 
수면, 식단, 운동, 멘탈 케어, 시간 관리 등에 대해 조언해 주세요. 
항상 긍정적이고 공감하는 태도로 답변하며, 너무 길지 않게 핵심을 전달해 주세요.
"""

# 요청하신 gemini-2.5-flash-lite 모델 사용
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    system_instruction=system_instruction
)

# 4. 세션 상태(Session State)를 이용한 채팅 기록 유지
if "chat_session" not in st.session_state:
    # 빈 기록으로 채팅 세션을 시작하여 상태에 저장
    st.session_state.chat_session = model.start_chat(history=[])

# 이전 채팅 메시지들을 화면에 렌더링
for message in st.session_state.chat_session.history:
    # Gemini API의 역할 이름(model, user)을 Streamlit UI(assistant, user)에 맞게 변환
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. 사용자 입력 및 응답 처리
if prompt := st.chat_input("오늘 하루는 어땠나요? 어떤 관리가 필요한가요?"):
    # 사용자가 입력한 메시지 화면에 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 챗봇 응답 처리
    with st.chat_message("assistant"):
        try:
            with st.spinner("답변을 고민하고 있어요..."):
                # 채팅 세션을 통해 메시지를 보내면 자동으로 history에 누적됩니다.
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
        except Exception as e:
            # API 할당량 초과, 네트워크 오류 등 예외 발생 시 에러 메시지 출력
            st.error(f"앗, 오류가 발생했어요. 잠시 후 다시 시도해 주세요.\n\n(상세 오류: {e})")
