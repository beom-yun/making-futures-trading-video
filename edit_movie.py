from moviepy.editor import *
import datetime


def now():
    return datetime.datetime.now()


def get_time_video(video, transactions, options):
    start = options['start_time'].replace('오전', 'AM').replace('오후', 'PM')
    start = datetime.datetime.strptime(start, '%Y-%m-%d %p %I:%M:%S')
    end = start + datetime.timedelta(seconds=video.end)
    return start, end


def edit_video(video, transactions, options):
    clip = VideoFileClip(video)

    time_video_start, time_video_end = get_time_video(
        clip, transactions, options)
    print('time_video', time_video_start, '->', time_video_end)

    for i, tr in enumerate(transactions):
        if not options['check_boxes'][i]:
            continue
        # print(tr)
        formatter = '%y/%m/%d %H:%M:%S'
        time_from = datetime.datetime.strptime(tr['주문시간'], formatter)
        time_to = datetime.datetime.strptime(tr['청산시간'], formatter)
        print('진입', time_from, '청산', time_to)

        if time_from > time_video_end or time_to < time_video_start:
            continue

        time_clip_from = max(
            time_from - datetime.timedelta(seconds=options['prev_sec']), time_video_start)
        time_clip_to = min(
            time_to + datetime.timedelta(seconds=options['after_sec']), time_video_end)
        print(time_clip_from, '~', time_clip_to)
        print()

    clip.close()
    # for i, tr in enumerate(transactions):
    #     if not options['check_boxes'][i]:
    #         continue
    #     print(i, tr, options['check_boxes'][i])
    #     formatter = '%y/%m/%d %H:%M:%S'
    #     time_from = datetime.datetime.strptime(tr['주문시간'], formatter)
    #     time_to = datetime.datetime.strptime(tr['청산시간'], formatter)
    #     print(time_from, '->', time_to)
    #     print()

    # clip = VideoFileClip(video).subclip(10, 25)

    # print('clip', clip)
    # print('start', clip.start)
    # print('end', clip.end)

    # clip.close()
