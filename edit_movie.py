from moviepy.editor import *
import datetime


def now():
    return datetime.datetime.now()


def get_time_video(video, options):
    start = options['start_time'].replace('오전', 'AM').replace('오후', 'PM')
    start = datetime.datetime.strptime(start, '%Y-%m-%d %p %I:%M:%S')
    end = start + datetime.timedelta(seconds=video.end)
    return start, end


def get_clip_time(time_v, time_tr, option):
    s = max(time_tr[0] -
            datetime.timedelta(seconds=option['prev_sec']), time_v[0])
    e = min(time_tr[1] +
            datetime.timedelta(seconds=option['after_sec']), time_v[1])
    return s, e


def get_clip_secs(t_video_s, t_clip):
    delta_start = (t_clip[0] - t_video_s).total_seconds()
    delta_end = (t_clip[1] - t_video_s).total_seconds()
    return delta_start, delta_end


def make_file_name(tr):
    if tr['구분'] == '매수':
        tr['결과'] = '익절' if tr['체결가'] < tr['청산가'] else '손절'
    else:
        tr['결과'] = '익절' if tr['체결가'] > tr['청산가'] else '손절'

    return f"{tr['주문시간'].strftime('%y%m%d-%H%M%S')}-{tr['종목코드']}-{tr['구분']}-{tr['결과']}"


def make_txt_clip(video, tr):
    time_s = tr['주문시간'].strftime('%H:%M:%S')
    time_e = tr['청산시간'].strftime('%H:%M:%S')
    txt = f"{tr['종목명']}\n{tr['구분']} {tr['결과']}\n진입 {time_s} {tr['체결가']}\n청산 {time_e} {tr['청산가']}"

    # txt_clip = TextClip(txt, color='white', fontsize=24)
    # txt_color = txt_clip.on_color(size=(video.w, txt_clip.h-10),
    #                               color=(0, 0, 0), pos=(6, 'center'), col_opacity=0.6)
    # return txt_color
    return txt


def edit_video(video, transactions, options):
    clip = VideoFileClip(video)

    time_video_start, time_video_end = get_time_video(clip, options)
    folder_name = time_video_start.strftime('%y%m%d')

    for i, tr in enumerate(transactions):
        if not options['check_boxes'][i]:
            continue

        formatter = '%y/%m/%d %H:%M:%S'
        tr['주문시간'] = datetime.datetime.strptime(tr['주문시간'], formatter)
        tr['청산시간'] = datetime.datetime.strptime(tr['청산시간'], formatter)

        if tr['주문시간'] > time_video_end or tr['청산시간'] < time_video_start:
            continue

        time_clip_from, time_clip_to = get_clip_time(
            (time_video_start, time_video_end), (tr['주문시간'], tr['청산시간']), options)

        time_clip_sec_start, time_clip_sec_end = get_clip_secs(
            time_video_start, (time_clip_from, time_clip_to))

        file_name = make_file_name(tr)
        sub_clip = clip.subclip(time_clip_sec_start, time_clip_sec_end)
        # txt_clip = make_txt_clip(sub_clip, tr)
        # print(txt_clip)
        # print()
        # result_video = CompositeVideoClip([sub_clip, txt_clip])
        # result_video.write_videofile(f'{file_name}.mp4')
        sub_clip.write_videofile(f'{file_name}.mp4')

    clip.close()
