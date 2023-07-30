import datetime
import time

import streamlit as st
import random
import requests
import json
import pandas as pd

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])

if page == 'users':
    st.title('ユーザー登録画面')

    # フォームを作成
    with st.form(key='user'):
        # user_id: int = random.randint(0, 10)
        user_name: str = st.text_input('ユーザー名', max_chars=12)
        data = {
            # 'user_id': user_id,
            'user_name': user_name,
        }
        submit = st.form_submit_button(label='登録')

    # フォームが送信されたら以下を実行
    if submit:
        # st.write('以下の内容で送信しました')
        # st.json(data)
        # st.write('以下のレスポンスが返ってきました')
        res = requests.post('http://localhost:8000/users', data=json.dumps(data))
        if res.status_code == 200:
            st.success('登録しました')
        st.write(res.status_code)
        st.json(res.json())

elif page == 'rooms':
    st.title('会議室登録画面')

    # フォームを作成
    with st.form(key='room'):
        # room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('会議名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        data = {
            # 'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity,
        }
        submit = st.form_submit_button(label='登録')

    # フォームが送信されたら以下を実行
    if submit:
        # st.write('以下の内容で送信しました')
        # st.json(data)
        # st.write('以下のレスポンスが返ってきました')
        res = requests.post('http://localhost:8000/rooms', data=json.dumps(data))
        if res.status_code == 200:
            st.success('会議室を登録しました')
        st.write(res.status_code)
        st.json(res.json())

elif page == 'bookings':
    st.title('会議室予約画面')

    # ユーザー一覧を取得
    users = requests.get('http://localhost:8000/users').json()
    # ユーザー名をキー、ユーザーIDを値とする辞書を作成
    users_name = {}
    for user in users:
        users_name[user['user_name']] = user['user_id']
    # ユーザーIDをキー、ユーザー名を値とする辞書を作成
    users_id = {}
    for user in users:
        users_id[user['user_id']] = user['user_name']

    st.write("### 会議室一覧")
    # 会議室一覧を取得
    rooms = requests.get('http://localhost:8000/rooms').json()
    # 会議室名をキー、会議室ID、キャパシティーを値とする辞書を作成
    rooms_name = {}
    for room in rooms:
        rooms_name[room['room_name']] = {
            "room_id": room['room_id'],
            "capacity": room['capacity'],
        }
    # 会議室IDをキー、会議室名、キャパシティーを値とする辞書を作成
    rooms_id = {}
    for room in rooms:
        rooms_id[room['room_id']] = {
            "room_name": room['room_name'],
            "capacity": room['capacity'],
        }
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)

    to_user_name = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]['room_name']
    to_room_capacity = lambda x: rooms_id[x]['capacity']
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')

    # 予約一覧を取得
    bookings = requests.get('http://localhost:8000/bookings').json()
    if len(bookings) > 0:
        st.write("### 予約一覧")
        df_bookings = pd.DataFrame(bookings)
        # 特定の列に関数を適用する
        df_bookings['user_id'] = df_bookings['user_id'].map(to_user_name)
        df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
        df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
        df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)
        df_bookings = df_bookings.rename(columns={
            'user_id': '予約者名',
            'room_id': '会議室',
            'booked_num': '予約人数',
            'start_datetime': '開始日時',
            'end_datetime': '終了日時'
        })
        st.table(df_bookings)
    else:
        st.write('予約はありません')

    # フォームを作成
    with st.form(key='booking'):
        # booking_id: int = random.randint(0, 10)
        user_name: str = st.selectbox('予約者名', list(users_name.keys()))
        room_name: int = st.selectbox('会議室名', list(rooms_name.keys()))
        booked_num: int = st.number_input('予約人数', step=1)
        date = st.date_input('日付', min_value=datetime.date.today())
        start_time = st.time_input('開始時刻', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('終了時刻', value=datetime.time(hour=17, minute=0))
        submit = st.form_submit_button(label='予約')

    # フォームが送信されたら以下を実行
    if submit:
        # start_dateとstart_timeを組み合わせてdatetime型にする
        # datetime型はJSONに変換できないので、isoformat()で文字列に変換する
        data = {
            # 'booking_id': booking_id,
            'user_id': users_name[user_name],
            'room_id': rooms_name[room_name]['room_id'],
            'booked_num': booked_num,
            'start_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute,
            ).isoformat(),
            'end_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute,
            ).isoformat()
        }
        # validation
        # 予約人数が定員を超えていないかチェックする
        capacity = rooms_name[room_name]['capacity']
        if capacity < booked_num:
            st.error(f'{room_name}の定員は{capacity}名です。定員を{booked_num - capacity}名超えています。')
            st.stop()
        # 予約開始時刻が終了時刻より前かチェックする
        if start_time >= end_time:
            st.error('終了時刻は開始時刻より後にしてください')
            st.stop()
        # 予約時刻が9~20時かチェックする
        if start_time < datetime.time(hour=9, minute=0) or end_time > datetime.time(hour=20, minute=0):
            st.error('利用可能時間は9:00 ~ 20:00です')
            st.stop()

        # st.write('以下の内容で送信しました')
        # st.json(data)
        # st.write('以下のレスポンスが返ってきました')
        res = requests.post('http://localhost:8000/bookings', data=json.dumps(data))
        if res.status_code == 200:
            st.success('会議室を予約しました')
            # 予約一覧の表示を更新するために5秒後にページをリロードする
            time.sleep(5)
            st.experimental_rerun()
        elif res.status_code == 400 and res.json()['detail'] == 'already booked':
            st.error('指定の時間は既に予約が入っています')
        st.write(res.status_code)
        st.json(res.json())
