import streamlit as st
import google.generativeai as genai
import PIL.Image
import random
import time

st.set_page_config(page_title="AI - KIENENTTI", page_icon="🚪", layout="centered")

# ==========================================
# 🚪 TRẠM TRUNG CHUYỂN (CHỌN PHIÊN BẢN)
# ==========================================
if "da_vao_trong" not in st.session_state:
    st.title("🚪 CỔNG VÀO AI - KIENENTTI")
    st.info("📱 Điện thoại của bạn thuộc hệ nào?")
    
    # NÚT 1: NHẢY SANG BẢN VIP (Sếp dán link web xịn của sếp vào đây nhé)
    link_vip = "https://thay-bang-link-app-xin-cua-sep.streamlit.app"
    st.link_button("🚀 MÁY XỊN (Android 7+ hoặc iOS 16.4+)", link_vip, use_container_width=True)
    
    st.markdown("---")
    
    # NÚT 2: Ở LẠI BẢN CLASSIC
    if st.button("⏳ MÁY ĐỜI CŨ (iPhone cũ chưa update)", use_container_width=True):
        st.session_state.da_vao_trong = True
        st.rerun()
    st.stop()

# ==========================================
# 🛡️ BÊN TRONG BẢN CLASSIC (CHO MÁY YẾU)
# ==========================================
now = int(time.time())
auth_code = st.query_params.get("auth")
auth_time = st.query_params.get("ts")

is_logged_in = False
if auth_code == "kienentti123" and auth_time:
    if now - int(auth_time) < 86400: is_logged_in = True
    else: st.query_params.clear() 

if not is_logged_in:
    st.title("🛡️ CỔNG BẢO MẬT (BẢN CLASSIC)")
    mk = st.text_input("🔑 Nhập mật khẩu sếp cấp:", type="password")
    if mk == "kienentti123":
        st.query_params["auth"] = "kienentti123"
        st.query_params["ts"] = str(now)
        st.rerun()
    elif mk: st.error("❌ Sai mật khẩu!")
    st.stop()

# --- SẢNH CHỜ CLASSIC ---
try: all_keys = st.secrets["DANH_SACH_KEY"]
except:
    st.error("⚠️ Sếp chưa nạp Key!")
    st.stop()

if "ai_persona" not in st.session_state:
    st.title("✨ TRUNG TÂM AI (BẢN CLASSIC)")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 GỌI ENTTI2", use_container_width=True):
            st.session_state.ai_name = "Entti2"
            st.session_state.ai_persona = "Bạn tên là Entti2. Bạn là trợ lý học tập cực kỳ thông minh."
            st.session_state.ai_model = "gemini-2.5-flash"
            st.session_state.messages = [] 
            st.rerun()
    with col2:
        if st.button("👼 GỌI KEM", use_container_width=True):
            st.session_state.ai_name = "Kem"
            st.session_state.ai_persona = "Bạn tên là Kem. Siêu hiền lành, ham ăn, dễ khóc nhè."
            st.session_state.ai_model = "gemini-2.5-flash-lite"
            st.session_state.messages = []
            st.rerun()
    st.stop()

# --- PHÒNG CHAT CLASSIC ---
st.title(f"✨ {st.session_state.ai_name} đang nghe lệnh!")
if st.button("⬅️ Trở lại sảnh chờ"):
    del st.session_state.ai_persona
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

file_anh = st.file_uploader("📸 Đính kèm ảnh (Tùy chọn):", type=['png', 'jpg', 'jpeg'])
user_input = st.chat_input(f"Nhắn cho {st.session_state.ai_name}...")

if user_input or file_anh:
    with st.chat_message("user"):
        if file_anh: st.image(file_anh, width=200)
        if user_input: st.write(user_input)
            
    st.session_state.messages.append({"role": "user", "content": user_input if user_input else "🖼️ [Sếp đã gửi ảnh]"})

    with st.chat_message("assistant"):
        try:
            genai.configure(api_key=random.choice(all_keys))
            model = genai.GenerativeModel(st.session_state.ai_model, system_instruction=st.session_state.ai_persona)
            prompt_parts = []
            if user_input: prompt_parts.append(user_input)
            if file_anh:
                prompt_parts.append(PIL.Image.open(file_anh))
                if not user_input: prompt_parts.append("Phân tích ảnh này.")
            
            res = model.generate_content(prompt_parts)
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e: st.error(f"❌ Lỗi: {str(e)}")