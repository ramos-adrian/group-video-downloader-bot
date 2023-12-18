import json

import pytest

from src.utils import get_file_size, is_video_url


@pytest.fixture
def example_youtube_url():
    return 'https://www.youtube.com/watch?v=0ewGL1NpD84'


@pytest.fixture
def example_youtube_info_sanitized():
    with open('tests/example_youtube_info_sanitized.json', 'r') as f:
        data = json.load(f)
    return data


def test_get_file_size(example_youtube_info_sanitized):
    assert get_file_size(example_youtube_info_sanitized) == 1130771


def test_get_file_size_not_found(example_youtube_info_sanitized):
    del example_youtube_info_sanitized['filesize_approx']
    with pytest.raises(Exception):
        get_file_size(example_youtube_info_sanitized)


def test_is_youtube_or_facebook_url(example_youtube_url):
    for url in ['https://www.youtube.com/watch?v=0ewGL1NpD84',
                'https://youtu.be/0ewGL1NpD84',
                'https://www.facebook.com/9gag/videos/10155790963006840']:
        assert is_video_url(url)


def test_is_youtube_or_facebook_url_invalid(example_youtube_url):
    for url in ['https://www.google.com',
                'https://www.imgur.com',
                'https://www.yahoo.com']:
        assert not is_video_url(url)