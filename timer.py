import streamlit as st
import time

st.set_page_config(
    page_title='위니브 타이머',
    page_icon='⏱️',
    layout='centered'
)

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h1 style="font-size: 3rem; font-weight: bold;">위니브 타이머</h1>
    <p style="color: #888; font-size: 0.8rem;">작업 리듬을 만들어주는 음악 타이머</p>
</div>
""", unsafe_allow_html=True) 

if 'timer_running' not in st.session_state:
    st.session_state.timer_running=False
if 'timer_paused' not in st.session_state:
    st.session_state.timer_paused=False
if 'start_time' not in st.session_state:
    st.session_state.start_time=None #왜 None값으로 저장하는지 설명해줬는데 놓쳤다.
if 'total_pause_time' not in st.session_state:
    st.session_state.total_pause_time=0
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds=70
if 'timer_completed' not in st.session_state:
    st.session_state.timer_completed=False
if 'show_celebration' not in st.session_state:
    st.session_state.show_celebration=False
if 'remaining_seconds' not in st.session_state:
    st.session_state.remaining_seconds=70
if 'pause_start_time' not in st.session_state:
    st.session_state.pause_start_time=None
if 'select_music' not in st.session_state:
    st.session_state.select_music='없음' # none이라고 해서 오류가 났던거임.
if 'music_auto_play' not in st.session_state:
    st.session_state.music_auto_play=True
    

def update_timer():
    if st.session_state.timer_running and not st.session_state.timer_paused: #타이머가 실행중
        current_time=time.time()
        elapsed= current_time-st.session_state.start_time-st.session_state.total_pause_time
        remaining= st.session_state.total_seconds-int(elapsed)

        if remaining<=0:
            st.session_state.remaining_seconds=0
            st.session_state.timer_running=False
            st.session_state.timer_completed=True
            st.session_state.show_celebration=True
        else:
            st.session_state.remaining_seconds=remaining 

def get_timer_status():
    #타이머가 완료되었을때
    if st.session_state.timer_completed:
        return "completed"
    #타이머가 진행중이고 정지 버튼을 누르지 않았을 때
    elif st.session_state.timer_running and not st.session_state.timer_paused:
        return "completed"
    #타이머 정지 버튼을 눌렀을 때
    elif st.session_state.timer_paused:
        return "paused"
    #그외
    else:
        return "stopped"

def format_time(second): 
    hours= second//3600
    minutes= (second%3600)//60 # %는 나머지
    seconds= second%60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" #00:35:00 한자리 숫자만 출력되는 경우 그 앞 빈자리에 0을 채워넣어라!

def set_timer_duration(minutes):
    st.session_state.total_seconds = minutes*60
    st.session_state.remaining_seconds=minutes*60

def reset_timer():

    st.session_state.timer_running=False
    st.session_state.timer_paused=False
    st.session_state.start_time=None 
    st.session_state.total_pause_time=0
    st.session_state.timer_completed=False
    st.session_state.show_celebration=False
    st.session_state.pause_start_time=None
    st.session_state.music_auto_play=True

update_timer()
current_status = get_timer_status()

col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="timer-display">', unsafe_allow_html=True)
     
    #프로그레스 바를 만들어줌.
    if st.session_state.total_seconds>=0:
        progress=st.session_state.remaining_seconds/st.session_state.total_seconds
        progress=max(0, min(1,progress)) #진행률이 0~1사이의 값만 출력이 되도록  진행률이 1을 넘지 못하게
    else:
        progress=0 #진행률바가 비도록
    
    st.progress(float(progress)) #혹시 몰라 float자료형으로 변환

    status_col1, status_col2, status_col3=st.columns(3) #타이머 레이아웃도 3등분으로 해줌.
    with status_col1:
        if current_status=="running":
            st.markdown('**타이머**', help="타이머가 실행중입니다!")
        elif current_status=="paused":
            st.markdown('**타이머**', help="타이머가 일시 정지 되었습니다!")
        elif current_status=="copleted":
            st.markdown('**타이머**', help="타이머가 완료되었습니다!")
        else:
            st.markdown('**타이머**', help="타이머가 대기중입니다!")
    with status_col3:
        st.markdown(f"<p style='text-align:right;'><strong>{int(progress*100)}%</strong></p>",unsafe_allow_html=True)
        # text-align:right 오른쪽으로 붙을 수 있게 숫자가

    

    st.markdown("""<style>
    .stColumns > div {
        display: flex;
        justify-content: center;
        align-items: center;
    }
        </style>
    """, unsafe_allow_html=True)
    

    #타이머 컬러 변경되도록
    timer_color=""
    if st.session_state.remaining_seconds<=60:
        timer_color="#ff4444"
    else:
        timer_color="var(--primary-text-color)"

    #남은 시간을 포맷해서 뿌려줬다?
    st. markdown(f"""<div class='timer-time' style='text-align:center; color:{timer_color};font-size: 4rem; font-weight: bold; margin: 2rem 0;'> 
        {format_time(st.session_state.remaining_seconds)}
    </div>
    """, unsafe_allow_html=True)

    # margin 공백 

    if st.session_state.total_seconds>0:
        col1, col2=st.columns(2)
        with col1:
            st.metric("설정시간", format_time(st.session_state.total_seconds)) #metric 지표를 보여줄 때(출력할 때 )많이 사용
        with col2:
            elapsed = st.session_state.total_seconds-st.session_state.remaining_seconds
            st.metric("경과시간",format_time(elapsed))

    if st.session_state.timer_completed and st.session_state.show_celebration:
        st.balloons()
        st.success("타이머가 완료되었습니다! 목표 시간을 달성했습니다!")

    # #만약, timer_running 타이머가 진행중이고(True), timer_paused=False일때
    # reamining_seconds가 10초 이하이고 0초보다 클때
    # Error 10초 이하 남았습니다. st.error
    # 남은 시간이 60초 이하이고 0초보다 클때
    # warning 1분 이하 남았습니다. 
    if st.session_state.timer_running and not st.session_state.timer_paused:
        if st.session_state.remaining_seconds<=10 and st.session_state.remaining_seconds>0:
            st.error("10초 이하 남았습니다.")
        elif st.session_state.remaining_seconds<=60 and st.session_state.remaining_seconds>0:
            st.warning("1분 이하 남았습니다.")





    btn1, btn2, btn3= st.columns(3) #비율 [0.3,0.3,0.4]

    with btn1:
        if not st.session_state.timer_running and not st.session_state.timer_paused:
            if st.button("▶️",help="시작", type="primary"):
                st.session_state.timer_running=True
                st.session_state.start_time=time.time() #현재 시각 저장
                st.session_state.total_pause_time=0 #정지버튼 눌렀을 때 시간을 계산해준다?
                st.session_state.timer_completed=False
                st.success("타이머가 시작되었습니다!")
                st.rerun()

        elif st.session_state.timer_running and not st.session_state.timer_paused:
            if st.button("⏸️",help="일시정지", type="primary"):
                st.session_state.timer_paused=True
                st.session_state.pause_start_time= time.time()
                st.info("타이머가 일시정지되었습니다.")
                st.rerun()
        elif st.session_state.timer_paused:
            if st.button("▶️",help="재개", type="primary"):
                st.session_state.timer_paused=False
                if st.session_state.pause_start_time:
                    pause_duration= time.time()-st.session_state.pause_start_time
                    st.session_state.total_pause_time += pause_duration #중지된 시간을 계속 더하는 것?
                    st.session_state.pause_start_time=None
                st.success("타이머가 재개되었습니다!")
                st.rerun()
    with btn2:
         if st.button("🔁",help="리셋"):
            st.session_state.timer_running=False
            st.session_state.timer_paused=False
            st.session_state.start_time=None 
            st.session_state.total_pause_time=0
            st.session_state.total_seconds=25*60
            st.session_state.timer_completed=False
            st.session_state.show_celebration=False
            st.session_state.remaining_seconds=25*60
            st.session_state.pause_start_time=None
            st.info("타이머가 리셋되었습니다.")
            st.rerun()
    with btn3:
       if st.button("1분 추가",help="1분 추가"):
        st.session_state.remaining_seconds+=60
        st.session_state.total_seconds+=60
        if st.session_state.timer_completed:
            st.session_state.timer_completed=False
            st.session_state.show_celebration=False
        st.toast("1분이 추가되었습니다!") #toast(깜빡이는 알림 팝업 알림처럼)
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True) 



    #배경음악 설정 UI 만들기
    #select box = ['없음', '1', '2', '3']
    #st.toggle('음악 자동 재생')
    #음악 다운로드해서 깃허브 올려준다(압축 풀고)

    st.markdown("**🎵 배경음악**")
    st.markdown("**음악 선택**")

      # 배경음악 리스트
    background_music = {
        "없음": None,
        "Bubblegum Code-2": "./music/Bubblegum Code-2.mp3",
        "Bubblegum Code": "./music/Bubblegum Code.mp3",
        "Code in the Moonlight": "./music/Code in the Moonlight.mp3",
        "Gentle Streams": "./music/Gentle Streams.mp3",
        "Late Night Thoughts": "./music/Late Night Thoughts.mp3",
        "Soft Light Waves": "./music/Soft Light Waves.mp3"
    }

    select_music=st.selectbox(
        "음악을 선택하세요:", 
        options=list(background_music.keys()),
        index=list(background_music.keys()).index(st.session_state.select_music),
        label_visibility="collapsed"
        )

    st.session_state.select_music = select_music

    if st.session_state.select_music!='없음':
        try:
            audio_file_path= background_music[st.session_state.select_music]
            st.audio(audio_file_path, format='audio/mpeg'
            ,loop=True, autoplay=st.session_state.music_auto_play)
        except Exception as e:
            st.warning(f"음악 파일을 찾을 수 없습니다:{audio_file_path}")

    auto_play = st.toggle("음악 자동재생",value=st.session_state.music_auto_play)
    st.session_state.music_auto_play=auto_play

with col_right:
    # 타이머 프리셋 데이터
    timer_presets = {
        "5분": 5,
        "15분": 15,
        "25분": 25,
        "30분": 30,
        "45분": 45,
        "60분": 60
    }

    st.markdown("**타이머 설정**")
    st.markdown("**빠른 타이머 설정**", help="자주 사용하는 시간으로 빠르게 설정하세요.")

    p1, p2, p3=st.columns(3)

   
    preset_buttons = [
        (p1,["5분","30분"]),
        (p2,["15분","45분"]),
        (p3,["25분","60분"])
    ]

    #순회하면서 만들거
    for col, p in preset_buttons:
        with col:
            for preset in p:
                if st.button(preset,key=f"preset_{preset}"):
                    minutes = timer_presets[preset]
                    set_timer_duration(minutes)
                    reset_timer()
                    st.toast(f"{preset} 설정 완료")
                    time.sleep(0.5)
                    st.rerun()

    st.divider()

    
    c1,c2 = st.columns([0.8,0.2])

    with c1:
        st.markdown("**사용자 설정(분)**")
    with c2:
        st.markdown(f"<p style='text-align:right;'><strong> {st.session_state.total_seconds//60}분</strong></p>",
        unsafe_allow_html=True)

    slider_m =st.slider("타이머 시간", 1,120,st.session_state.total_seconds//60,
    help="1분부터 120분까지 설정 가능합니다.")

    if st.button('설정 적용', type="primary"):
        set_timer_duration(slider_m)
        reset_timer()
        st.toast(f"{slider_m}분 설정완료!")
        time.sleep(0.5)
        st.rerun()

    st.divider()

   
    st.markdown("**⏱️타이머 상세 설정(시:분:초)**")

    col1,col2,col3= st.columns(3)
    with col1:
        st.markdown("**시간**")
        hours=st.number_input("시간",min_value=0, max_value=23, value=st.session_state.total_seconds//3600)
    with col2:
        st.markdown("**분**")
        minutes = st.number_input("분", min_value=0, max_value=59, value=(st.session_state.total_seconds%3600)//60)
    with col3:
        st.markdown("**초**")
        seconds = st.number_input("초", min_value=0, max_value=59, value=(st.session_state.total_seconds%60))


    if st.button("⚙️상세설정 적용", type="primary"):
        st.session_state.total_seconds = hours * 3600 + minutes * 60 + seconds
        st.session_state.remaining_seconds = st.session_state.total_seconds
        reset_timer()
        st.rerun()

st.divider()
st.markdown(f"<p style='text-align:center;'><strong> @Juyeon All rights reserved</strong></p>",
unsafe_allow_html=True)

if st.session_state.timer_running and not st.session_state.timer_paused and not st.session_state.timer_completed:
        time.sleep(1) #1초에 1번씩 재실행
        st.rerun()