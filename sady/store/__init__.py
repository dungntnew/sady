import os
import json
import jsonpickle


class Track(object):
    fields = ('id',  # unique track sound cloud track id
              'title',  # track title
              'playback_count',  # playback count
              'genre',  # track genre
              'synced',  # where track downloaded
              'local_uri',  # path to local track file (None if not synced)
              'stream_url',  # sound cloud stream url
              'download_url',  # sound cloud download url
              )

    def __init__(self, *argv, **kwargs):
        self.__set_default__()

        if argv and len(argv):
            obj = argv[0]
            if not isinstance(obj, Track):
                raise ValueError('cannot instance with: %s' % obj.__class__)

            for field in self.fields:
                if hasattr(obj, field):
                    val = getattr(obj, field)
                    setattr(self, field, val)
        else:
            if kwargs:
                for k, v in kwargs.items():
                    if k in self.fields:
                        setattr(self, k, v)

    def __set_default__(self):
        for field in self.fields:
            setattr(self, field, None)

    def get_track_id(self):
        return getattr(self, 'id', None)

    def update(self, **kwargs):
        """
        :param kwargs: dict of attr
        :return: total field updated
        """
        effected = 0
        if kwargs:
            for k, v in kwargs.items():
                if k in self.fields and v:
                    effected += 1
                setattr(self, k, v)
        return effected

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class TrackList(object):
    def __init__(self, data_uri, playlist_uri):
        """
        load list of track from local file by data_url
        :param data_uri: path to data file (use jsonpickle format)
        :param playlist_uri: path to playlist file(raw text format)
        """
        self.data_uri = data_uri
        self.playlist_uri = playlist_uri
        self.tracks = []
        self.__load_from_disk()

    def __load_from_disk(self):
        """
        load track data from disk
        (do nothing if have any error)
        :return:
        """
        with open(self.data_uri, 'r') as data_file:
            raw_data = data_file.read()
            if raw_data and 'py/object' in raw_data:
                self.tracks = jsonpickle.decode(raw_data)

    def __save_to_disk(self):
        """
        save track data to disk
        :return:
        """
        with open(self.data_uri, 'w') as data_file:
            raw_data = jsonpickle.encode(self.tracks)
            if raw_data and 'py/object' in raw_data:
                data_file.write(raw_data)

    def __write_to_playlist_file(self):
        """
        extract track data to playlist file
        :return:
        """
        local_uris = [track.local_uri for track in self.tracks if track.synced]
        if local_uris:
            with open(self.playlist_uri, 'a') as playlist_file:
                playlist_file.write('\n'.join(local_uris))

    def flush(self):
        self.__save_to_disk()
        self.__write_to_playlist_file()

    def __clean(self):
        with open(self.playlist_uri, 'r') as f:
            track_file_paths = f.readlines()
            for track_name in track_file_paths:
                os.remove(track_name)
        with open(self.playlist_uri, 'w+'):
            pass

    def track_by_id(self, track_id):
        """
        get track by id
        :param track_id:
        :return: None if not exists
        """
        for track in self.tracks:
            if str(track_id) == str(track.get_track_id()):
                return track
        return None

    def exists(self, track_id):
        """
        test where track id exist in tracks database
        :param track_id:
        :return: False if not exists
        """
        return self.track_by_id(track_id) is not None

    def add(self, track, flush=True):
        if not isinstance(track, Track):
            raise ValueError('cannot add a %s to track list' % track.__class__)

        if not self.exists(track.get_track_id()):
            self.tracks.append(track)
            if flush:
                self.__save_to_disk()
                self.__write_to_playlist_file()

    def add_all(self, tracks, flush=True):
        for track in tracks:
            self.add(track, False)
        if flush:
            self.__save_to_disk()
            self.__write_to_playlist_file()

    def update(self, track_id, flush=True, **kwargs):
        track = self.track_by_id(track_id)
        if track:
            updated = track.update(**kwargs)
            if updated and flush:
                self.__save_to_disk()
                self.__write_to_playlist_file()

    def top_tracks(self, size=20):
        return self.tracks[:size]

    def __repr__(self):
        return 'data_uri: %s\n' \
               'playlist_uri: %s\n' \
               'track count: %s\n' % (self.data_uri, self.playlist_uri, len(self.tracks))
