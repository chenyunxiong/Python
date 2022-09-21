import asyncio
import sys
import typing

from mxget import exceptions
from mxget.provider import netease

_SONG_REQUEST_LIMIT = 1000


async def get_playlist(playlist_id: typing.Union[int, str]) -> typing.List[dict]:
    async with netease.NetEase() as client:
        resp = await client.get_playlist_raw(playlist_id)
        try:
            total = resp['playlist']['trackCount']
            tracks = resp['playlist']['tracks']
            track_ids = resp['playlist']['trackIds']
        except KeyError:
            raise exceptions.DataError('get playlist: no data')

        if total == 0:
            raise exceptions.DataError('get playlist: no data')

        if total > _SONG_REQUEST_LIMIT:
            async def patch_tracks(*args: typing.Union[int, str]):
                return await client.get_song_raw(*args)

            tasks = []
            for i in range(_SONG_REQUEST_LIMIT, total, _SONG_REQUEST_LIMIT):
                j = i + _SONG_REQUEST_LIMIT
                if j > total:
                    j = total
                song_ids = [track_ids[k]['id'] for k in range(i, j)]
                tasks.append(asyncio.ensure_future(patch_tracks(*song_ids)))

            await asyncio.gather(*tasks)
            for task in tasks:
                if not task.exception():
                    tracks.extend(task.result().get('songs', []))

        song_ids = [s['id'] for s in tracks]
        resp = await client.get_song_url_raw(*song_ids)
        data = resp.get('data')
        if data is None or not data:
            raise exceptions.DataError('get song url: no data')

        code_map = dict()
        for i in data:
            code_map[i['id']] = i['code']

        for s in tracks:
            s['code'] = code_map.get(s['id'])

        return tracks


def filter_grey_songs_form_playlist(playlist_id: typing.Union[int, str]):
    """获取网易云音乐歌单变灰歌曲列表，使用前请临时将歌单设为公开"""
    loop = asyncio.get_event_loop()
    try:
        resp = loop.run_until_complete(get_playlist(playlist_id))
    except exceptions.ClientError as e:
        print(e)
        sys.exit(1)

    grey_songs = [song for song in resp if song.get('code') == 404]
    for i, v in enumerate(grey_songs):
        artist = '/'.join([a['name'].strip() for a in v['ar']])
        print('[{:02d}] {} - {} - {} - {}'.format(i + 1, v['name'], artist, v['al']['name'], v['id']))


def main():
    if len(sys.argv) < 2:
        playlist_id = input('Playlist ID: ')
    else:
        playlist_id = sys.argv[-1]

    filter_grey_songs_form_playlist(playlist_id)


if __name__ == '__main__':
    main()