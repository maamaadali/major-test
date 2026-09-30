import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os
import base64
import time

# تنظیمات اصلی صفحه
st.set_page_config(
    page_title="سامانه جامع انتخاب رشته | گروه مشاوره خیلی سبز لنجان",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# استایل اختصاصی برند خیلی سبز
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');

    html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, label, button, input {
        font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    :root {
        --ks-green: #00A859;
        --ks-green-dark: #007A3D;
        --ks-red: #E31E24;
        --ks-yellow: #FFD200;
        --ks-bg: #F8FAF8;
    }

    /* کادرهای ورودی شکیل و تمیز */
    .stTextInput>div>div>input {
        border-radius: 10px !important;
        border: 2px solid #D5E8D5 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        color: #1B365D !important;
        background-color: #FAFCFA !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00A859 !important;
        box-shadow: 0 0 0 2px rgba(0, 168, 89, 0.25) !important;
    }

    /* پیام خطای کوچک زیر کادر */
    .input-error-msg {
        color: #E31E24 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        margin-top: -8px !important;
        margin-bottom: 8px !important;
    }

    /* دکمه‌های اصلی خیلی سبز */
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(135deg, #00A859 0%, #008F4C 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(0, 168, 89, 0.35) !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 168, 89, 0.5) !important;
        background: linear-gradient(135deg, #E31E24 0%, #C41217 100%) !important;
    }

    /* سربرگ اختصاصی */
    .brand-header {
        background: white;
        border-radius: 20px;
        padding: 20px 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 2px solid #EAF5EA;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* کارت‌های رشته‌ها */
    .major-card {
        background: white;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 16px;
        border-right: 6px solid #00A859;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    .major-card:hover {
        transform: translateX(-4px);
    }
    .major-card-top {
        border-right: 6px solid #E31E24 !important;
        background: #FFFDFD;
    }

    /* برچسب پذیرش */
    .badge-riazi {
        background: #E8F0FE;
        color: #1967D2;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-tajrobi {
        background: #E6F4EA;
        color: #137333;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-ensani {
        background: #F3E8FD;
        color: #6B21A8;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-moshtarak {
        background: #FEF7E0;
        color: #B06000;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* تب‌های استریم‌لیت */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0 !important;
        font-weight: 700 !important;
        padding: 10px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #EAF5EA !important;
        color: #00A859 !important;
    }

    /* گزینه‌های رادیویی کاملاً خوانا در تم تیره و روشن */
    div[data-testid="stRadio"] [role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1.5px solid #00A859 !important;
        border-radius: 10px !important;
        padding: 6px 16px !important;
        margin-left: 10px !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label * {
        color: #111827 !important;
        font-weight: 800 !important;
    }

    /* پاورقی اختصاصی */
    .brand-footer {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        margin-top: 50px;
        border-top: 3px solid #00A859;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.03);
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

def fa_to_en_digits(text):
    """تبدیل خودکار ارقام فارسی و عربی به انگلیسی"""
    fa_digits = "۰۱۲۳۴۵۶۷۸۹"
    ar_digits = "٠١٢٣٤٥٦٧٨٩"
    en_digits = "0123456789"
    trans = str.maketrans(fa_digits + ar_digits, en_digits * 2)
    return str(text).strip().translate(trans)

def cosine_similarity(v1, v2):
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

@st.cache_data
def load_data(excel_path="ماتریس_انتخاب_رشته_دانشگاه.xlsx"):
    if not os.path.exists(excel_path):
        return None, None, None
    xls = pd.ExcelFile(excel_path)
    sheet_names = xls.sheet_names
    
    df_r = pd.read_excel(excel_path, sheet_name="ماتریس_ریاضی_فیزیک") if "ماتریس_ریاضی_فیزیک" in sheet_names else None
    df_t = pd.read_excel(excel_path, sheet_name="ماتریس_علوم_تجربی") if "ماتریس_علوم_تجربی" in sheet_names else None
    df_e = pd.read_excel(excel_path, sheet_name="ماتریس_علوم_انسانی") if "ماتریس_علوم_انسانی" in sheet_names else None
    
    def clean_df(df):
        if df is None: return None
        df = df.dropna(subset=["نام رشته دانشگاهی"])
        valid_types = ["اختصاصی ریاضی", "اختصاصی تجربی", "اختصاصی انسانی", "مشترک"]
        df = df[df["نوع پذیرش"].astype(str).str.strip().isin(valid_types)].copy()
        chapters = df.columns[3:].tolist()
        for col in chapters:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(1.0)
        return df

    df_r = clean_df(df_r)
    df_t = clean_df(df_t)
    df_e = clean_df(df_e)
    return df_r, df_t, df_e

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_candidates = ["logo.jpg", "logo.png", "image_2f36ae.jpg", "kheilisabz_logo.jpg"]
logo_base64 = None
for candidate in logo_candidates:
    b64 = get_base64_image(candidate)
    if b64:
        logo_base64 = b64
        break

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "student_info" not in st.session_state:
    st.session_state.student_info = {}
if "step" not in st.session_state:
    st.session_state.step = "login"

df_riazi, df_tajrobi, df_ensani = load_data()

# ۱. سربرگ اختصاصی خیلی سبز
logo_html = ""
if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" style="height: 80px; width: auto; border-radius: 12px; object-fit: contain;">'
else:
    logo_html = '<div style="font-size: 3rem;">🍏❤️</div>'

st.markdown(f"""
<div class="brand-header">
    <div style="flex: 1; text-align: right;">
        <h2 style="color: #00A859; margin: 0; font-weight: 800; font-size: 1.7rem;">گروه مشاوره خیلی سبز لنجان</h2>
        <p style="color: #555; margin: 5px 0 0 0; font-size: 1rem; font-weight: 500;">
            سامانه هوشمند و تخصصی هدایت تحصیلی و اولویت‌بندی رشته‌های دانشگاهی (ریاضی، تجربی، انسانی)
        </p>
    </div>
    <div style="text-align: left; padding-left: 10px;">
        {logo_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ۲. صفحه لاگین با کد فعال‌سازی ۸۵۰۰
if not st.session_state.authenticated:
    st.markdown("### 🔐 ورود به پنل اختصاصی انتخاب رشته داوطلب")
    st.info("برای استفاده از سامانه، مشخصات خود و کد فعال‌سازی اختصاصی را وارد نمایید.")

    col1, col2 = st.columns(2)
    with col1:
        st_name = st.text_input("👤 نام و نام خانوادگی داوطلب (اجباری):", placeholder="مثال: محمدعلی ایزدی")
        st_phone = st.text_input("📱 شماره تماس همراه (اجباری):", placeholder="مثال: 09130660326")
    with col2:
        st_school = st.text_input("🏫 نام مدرسه / شعبه آموزشگاه:", placeholder="مثال: خیلی سبز لنجان")
        st_code = st.text_input("🔑 کد فعال‌سازی اختصاصی:", type="password", placeholder="کد ۴ رقمی مشاور")

    st_track = st.radio(
        "🎯 گروه آزمایشی شما:",
        ["ریاضی فیزیک", "علوم تجربی", "علوم انسانی"],
        horizontal=True
    )

    if st.button("🚀 ورود به سامانه و شروع نمره‌دهی سرفصل‌ها"):
        if not st_name.strip():
            st.error("⚠️ لطفاً نام و نام خانوادگی خود را وارد کنید.")
        elif not st_phone.strip():
            st.error("⚠️ لطفاً شماره تماس همراه را وارد کنید تا در سربرگ کارنامه ثبت شود.")
        elif st_code.strip() != "8500":
            st.error("⛔ کد فعال‌سازی وارد شده صحیح نمی‌باشد! لطفاً با گروه مشاوره خیلی سبز لنجان (09130660326) تماس بگیرید.")
        else:
            st.session_state.authenticated = True
            st.session_state.student_info = {
                "name": st_name.strip(),
                "phone": st_phone.strip(),
                "school": st_school.strip() if st_school.strip() else "خیلی سبز لنجان",
                "track": st_track
            }
            st.session_state.step = "test"
            st.rerun()

# ۳. صفحه نمره‌دهی به سرفصل‌ها با کادرهای عددی
elif st.session_state.step == "test":
    info = st.session_state.student_info
    track = info["track"]
    if track == "ریاضی فیزیک":
        df = df_riazi
    elif track == "علوم تجربی":
        df = df_tajrobi
    else:
        df = df_ensani
    
    if df is None:
        st.error("فایل اکسل ماتریس پیدا نشد یا برگه مربوطه در فایل وجود ندارد. لطفاً فایل 'ماتریس_انتخاب_رشته_دانشگاه.xlsx' را بررسی کنید.")
        st.stop()

    chapters = df.columns[3:].tolist()

    categorized = {}
    for ch in chapters:
        lesson, ch_title = ch.split(" | ") if " | " in ch else ("عمومی", ch)
        categorized.setdefault(lesson, []).append((ch, ch_title))

    st.markdown(f"#### سلام {info['name']} عزیز! 👋")
    st.markdown(f"""
    برای هر یک از سرفصل‌های دروس رشته **{track}**، میزان علاقه خود را به صورت یک **عدد صحیح بین ۱ تا ۱۰** در کادر مربوطه وارد کنید:
    * **شرایط عدد:** فقط عدد صحیح از **۱** (کمترین علاقه) تا **۱۰** (بیشترین علاقه).
    * در صورت تایپ مقادیر نامعتبر، راهنما در زیر همان کادر نشان داده می‌شود.
    """)

    tabs = st.tabs([f"📚 {lesson} ({len(items)} فصل)" for lesson, items in categorized.items()])
    
    ratings = {}
    has_validation_error = False

    for tab, (lesson, items) in zip(tabs, categorized.items()):
        with tab:
            st.markdown(f"##### سرفصل‌های درس {lesson}:")
            c1, c2 = st.columns(2)
            for i, (full_key, ch_title) in enumerate(items):
                target_col = c1 if i % 2 == 0 else c2
                with target_col:
                    default_val = st.session_state.get(f"input_{full_key}", "5")
                    val_input = st.text_input(
                        f"📌 {ch_title}:",
                        value=default_val,
                        key=f"input_{full_key}",
                        max_chars=2,
                        help="فقط عدد صحیح از ۱ تا ۱۰ وارد کنید."
                    )
                    clean_str = fa_to_en_digits(val_input)
                    
                    is_valid = False
                    if clean_str.isdigit():
                        int_val = int(clean_str)
                        if 1 <= int_val <= 10:
                            is_valid = True
                            ratings[full_key] = int_val
                    
                    if not is_valid:
                        st.markdown(
                            "<div class='input-error-msg'>⚠️ شرایط ورود: فقط عدد صحیح بین ۱ تا ۱۰ مجاز است.</div>",
                            unsafe_allow_html=True
                        )
                        has_validation_error = True

    st.markdown("---")
    
    # دکمه محاسبه با تایمر و انیمیشن هوشمند ۶ تا ۸ ثانیه‌ای
    if st.button("🔍 محاسبه و تحلیل ۲۰ رشته دانشگاهی متناسب با علایق من"):
        if has_validation_error:
            st.error("⛔ لطفاً کادرهایی که خطای ورودی دارند را اصلاح کنید. همه نمرات باید عدد صحیح بین ۱ تا ۱۰ باشند.")
        else:
            status_box = st.empty()
            progress_bar = st.progress(0)
            
            steps = [
                (15, "📥 در حال جمع‌آوری و اعتبارسنجی نمرات علاقه‌مندی داوطلب...", 1.2),
                (35, "🧠 بردارسازی تمایلات فردی و انطباق با پایگاه داده دروس پایه دانشگاهی...", 1.5),
                (60, "🔍 اجرای الگوریتم پیشرفته شباهت کسینوسی بر کلیه رشته‌های دانشگاهی...", 1.8),
                (85, "🎯 استخراج سرفصل‌های هم‌پوشان و نگاشت دلایل علمی اولویت‌بندی...", 1.5),
                (100, "✨ محاسبات نهایی با موفقیت انجام شد! در حال صدور کارنامه...", 1.0)
            ]
            
            for pct, msg, sleep_dur in steps:
                status_box.info(f"**{msg}**")
                progress_bar.progress(pct)
                time.sleep(sleep_dur)
                
            status_box.empty()
            progress_bar.empty()
            
            st.session_state.ratings = ratings
            st.session_state.step = "results"
            st.rerun()

# ۴. داشبورد نتایج ۲۰ رشته برتر و کارنامه رسمی
elif st.session_state.step == "results":
    info = st.session_state.student_info
    track = info["track"]
    if track == "ریاضی فیزیک":
        df = df_riazi
    elif track == "علوم تجربی":
        df = df_tajrobi
    else:
        df = df_ensani

    chapters = df.columns[3:].tolist()
    ratings = st.session_state.ratings

    user_vec = np.array([float(ratings[ch]) for ch in chapters])

    results = []
    for _, row in df.iterrows():
        major_name = row["نام رشته دانشگاهی"]
        adm_type = row["نوع پذیرش"]
        major_vec = row[3:].values.astype(float)
        
        sim = cosine_similarity(user_vec, major_vec)
        pct = round(sim * 100, 2)
        
        overlap = user_vec * major_vec
        top_indices = np.argsort(overlap)[::-1]
        reasons = []
        for idx in top_indices:
            if user_vec[idx] >= 7 and major_vec[idx] >= 7:
                reasons.append((chapters[idx], int(user_vec[idx]), int(major_vec[idx])))
            if len(reasons) >= 3:
                break
                
        results.append({
            "major": major_name,
            "type": adm_type,
            "percent": pct,
            "reasons": reasons
        })

    results.sort(key=lambda x: x["percent"], reverse=True)
    top_20 = results[:20]

    st.success(f"🎉 تحلیل علایق تحصیلی داوطلب محترم **{info['name']}** با موفقیت تکمیل شد.")

    tab_cards, tab_report = st.tabs([
        "🏆 مشاهده کارت‌های تحلیلی و نمودار ۲۰ رشته برتر",
        "📄 مشاهده و چاپ مستقیم کارنامه رسمی (خیلی سبز لنجان)"
    ])

    # ------------------- تب ۱: کارت‌ها و نمودارها -------------------
    with tab_cards:
        col_cards, col_stats = st.columns([3, 2])
        
        with col_cards:
            for rank, item in enumerate(top_20, 1):
                is_top3 = rank <= 3
                card_class = "major-card major-card-top" if is_top3 else "major-card"
                
                if item["type"] == "اختصاصی ریاضی":
                    badge_class = "badge-riazi"
                elif item["type"] == "اختصاصی تجربی":
                    badge_class = "badge-tajrobi"
                elif item["type"] == "اختصاصی انسانی":
                    badge_class = "badge-ensani"
                else:
                    badge_class = "badge-moshtarak"
                
                reasons_html = ""
                if item["reasons"]:
                    reasons_html = "<div style='margin-top: 8px; font-size: 0.88rem; color: #444;'>"
                    reasons_html += "<b>💡 سرفصل‌های هم‌پوشان و کلیدی:</b><br>"
                    for ch_title, u_s, m_w in item["reasons"]:
                        reasons_html += f"• {ch_title} <span style='color:#00A859;'>(علاقه: {u_s} | اهمیت: {m_w})</span><br>"
                    reasons_html += "</div>"
                else:
                    reasons_html = "<div style='font-size: 0.85rem; color: #777; margin-top: 6px;'>• تطابق کلی بر اساس پروفایل متوازن نمرات</div>"

                medal = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
                
                st.markdown(f"""
                <div class="{card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.25rem; font-weight: 800; color: #1B365D;">
                            {medal} {item['major']}
                        </span>
                        <span class="{badge_class}">{item['type']}</span>
                    </div>
                    <div style="margin: 8px 0;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.95rem; font-weight: 700; color: #00A859;">
                            <span>میزان تطابق:</span>
                            <span>{item['percent']:.1f}٪</span>
                        </div>
                        <div style="background: #EAF5EA; border-radius: 10px; height: 10px; width: 100%; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #00A859, #E31E24); width: {item['percent']}%; height: 100%;"></div>
                        </div>
                    </div>
                    {reasons_html}
                </div>
                """, unsafe_allow_html=True)

        with col_stats:
            st.markdown("#### 📊 نمودار مقایسه‌ای ۱۰ رشته اول:")
            chart_df = pd.DataFrame({
                "رشته": [x["major"] for x in top_20[:10]][::-1],
                "درصد تطابق": [x["percent"] for x in top_20[:10]][::-1]
            })
            st.bar_chart(chart_df.set_index("رشته"), color="#00A859")

            st.markdown("---")
            if st.button("🔄 آزمون مجدد برای داوطلب دیگر"):
                st.session_state.authenticated = False
                st.session_state.step = "login"
                st.rerun()

    # ------------------- تب ۲: کارنامه رسمی تک‌صفحه‌ای استاندارد -------------------
    with tab_report:
        table_rows = ""
        for idx, itm in enumerate(top_20, 1):
            reasons_str = "، ".join([r[0].split(" | ")[-1] for r in itm["reasons"]]) if itm["reasons"] else "تطابق میانگین سرفصل‌ها"
            table_rows += f"""
            <tr>
                <td style="text-align:center; padding:2.5px 4px; border:1px solid #ddd;">{idx}</td>
                <td style="padding:2.5px 6px; border:1px solid #ddd; font-weight:bold;">{itm['major']}</td>
                <td style="text-align:center; padding:2.5px 4px; border:1px solid #ddd;">{itm['type']}</td>
                <td style="text-align:center; padding:2.5px 4px; border:1px solid #ddd; color:#00A859; font-weight:bold;">{itm['percent']:.1f}٪</td>
                <td style="padding:2.5px 6px; border:1px solid #ddd; font-size:10px;">{reasons_str}</td>
            </tr>
            """

        logo_img_report = f'<img src="data:image/jpeg;base64,{logo_base64}" style="height: 52px; width: auto; object-fit: contain;">' if logo_base64 else '🍏'

        report_html = f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="utf-8">
    <title>کارنامه انتخاب رشته - {info['name']}</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
        
        @page {{
            size: A4 portrait;
            margin: 5mm 8mm 5mm 8mm !important;
        }}
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
        body {{
            font-family: 'Vazirmatn', Tahoma, sans-serif;
            direction: rtl;
            margin: 0;
            padding: 5px;
            background: #ffffff;
            color: #222;
        }}
        .report-box {{
            border: 2px solid #00A859;
            border-radius: 12px;
            padding: 8px 12px;
            margin: 0 auto;
            max-width: 820px;
            page-break-inside: avoid !important;
        }}
        .btn-print {{
            background: #00A859;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            font-family: inherit;
            font-weight: bold;
            margin-bottom: 10px;
            box-shadow: 0 2px 8px rgba(0,168,89,0.3);
        }}
        .btn-print:hover {{
            background: #E31E24;
        }}
        table.data-table {{
            width: 100%;
            border-collapse: collapse;
            text-align: right;
            font-size: 10.5px;
            page-break-inside: avoid !important;
        }}
        table.data-table th {{
            background: #00A859 !important;
            color: white !important;
            padding: 3px 5px;
            border: 1px solid #ccc;
            font-size: 11px;
            text-align: center;
        }}
        table.data-table td {{
            padding: 2.2px 5px;
            border: 1px solid #ddd;
            line-height: 1.15;
        }}
        @media print {{
            .btn-print, .no-print {{
                display: none !important;
            }}
            body {{
                padding: 0 !important;
                margin: 0 !important;
            }}
            .report-box {{
                border: 2px solid #00A859 !important;
                padding: 6px 10px !important;
            }}
        }}
    </style>
</head>
<body>
    <center class="no-print">
        <button class="btn-print" onclick="window.print()">🖨️ چاپ مستقیم کارنامه تک‌صفحه‌ای یا ذخیره PDF</button>
    </center>
    
    <div class="report-box" id="printable-report">
        <!-- سربرگ کارنامه -->
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #E31E24; padding-bottom:6px; margin-bottom:6px;">
            <div>
                <h2 style="color:#00A859; margin:0; font-size:17px; font-weight:800;">کارنامه جامع هدایت تحصیلی و اولویت‌بندی رشته‌های دانشگاهی</h2>
                <h4 style="color:#444; margin:3px 0 0 0; font-size:13px; font-weight:600;">گروه مشاوره و برنامه‌ریزی خیلی سبز لنجان</h4>
            </div>
            <div style="text-align:left;">
                {logo_img_report}
            </div>
        </div>
        
        <!-- نوار اطلاعات داوطلب -->
        <table style="width:100%; margin-bottom:6px; background:#F8FAF8; border:1px solid #E2EFE2; border-radius:6px; padding:4px; font-size:11px;">
            <tr>
                <td style="padding:2px 4px;"><b>نام داوطلب:</b> {info['name']}</td>
                <td style="padding:2px 4px;"><b>گروه آزمایشی:</b> {info['track']}</td>
                <td style="padding:2px 4px;"><b>شماره تماس:</b> <span style="direction:ltr; display:inline-block;">{info['phone']}</span></td>
                <td style="padding:2px 4px;"><b>مدرسه / مرکز:</b> {info['school']}</td>
            </tr>
        </table>

        <!-- جدول ۲۰ رشته برتر -->
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width:5%;">رتبه</th>
                    <th style="width:30%; text-align:right;">عنوان رشته دانشگاهی</th>
                    <th style="width:18%;">نوع پذیرش</th>
                    <th style="width:12%;">درصد شباهت</th>
                    <th style="width:35%; text-align:right;">مهم‌ترین فصول محرک علاقه</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>

        <!-- پاورقی کارنامه و محل امضا -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; padding-top:6px; border-top:1px solid #eee; font-size:10.5px;">
            <div>
                <b>مهر و تاییدیه مشاور ارشد:</b> ............................................
            </div>
            <div style="text-align:left;">
                📞 تماس: <b>09130660326</b> | اینستاگرام: <b>@kheilisabze_lenjan</b>
            </div>
        </div>
    </div>
</body>
</html>"""

        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            st.download_button(
                label="📥 دانلود فایل کارنامه رسمی (HTML آماده چاپ تک‌صفحه‌ای)",
                data=report_html,
                file_name=f"کارنامه_خیلی_سبز_{info['name']}.html",
                mime="text/html"
            )
        with col_b2:
            st.info("💡 برای چاپ فوری، دکمه سبز رنگ بالای پیش‌نمایش زیر را بزنید یا کلیدهای Ctrl + P را فشار دهید.")

        components.html(report_html, height=720, scrolling=True)

# ۵. پاورقی ثابت برند خیلی سبز لنجان
st.markdown(f"""
<div class="brand-footer">
    <div style="font-size: 1.15rem; font-weight: 800; color: #00A859; margin-bottom: 8px;">
        🍏 گروه مشاوره و برنامه‌ریزی خیلی سبز لنجان
    </div>
    <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; font-size: 0.98rem; color: #333;">
        <div>📞 <b>شماره تماس:</b> <a href="tel:09130660326" style="color:#00A859; text-decoration:none;">09130660326</a></div>
        <div>📸 <b>اینستاگرام:</b> <a href="https://instagram.com/kheilisabze_lenjan" target="_blank" style="color:#E31E24; text-decoration:none; font-weight:bold;">@kheilisabze_lenjan</a></div>
        <div>✈️ <b>طراح و توسعه‌دهنده:</b> <a href="https://t.me/mmd1ali1" target="_blank" style="color:#0088cc; text-decoration:none; font-weight:bold;">@mmd1ali1</a></div>
    </div>
    <div style="font-size: 0.85rem; color: #888; margin-top: 10px;">
        تمامی حقوق مادی و معنوی این سامانه متعلق به «گروه مشاوره خیلی سبز لنجان» می‌باشد.
    </div>
</div>
""", unsafe_allow_html=True)
