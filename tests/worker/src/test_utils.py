from worker.src.util import extract_profile


def test_extract_profile(profile):
    extracted = extract_profile(profile)
    assert extracted == {
        "created_at": "2020-10-07T13:27:44.758211",
        "username": "_.cryptid.kid.art._",
        "biography": "He/him\nSelf taught \n🇮🇱\nSupport me on ko fi ?:)",
        "followers_count": 192,
        "following_count": 313,
        "full_name": "Xan (Storm Alexander)",
        "id": "11472474315",
        "is_business_account": False,
        "is_joined_recently": False,
        "is_private": False,
        "posts_count": 42,
        "profile_pic_url": "https://instagram.ftzl1-1.fna.fbcdn.net/v/t51.2885-19/s150x150/106587108_280349786537053_1306958651287526582_n.jpg?_nc_ht=instagram.ftzl1-1.fna.fbcdn.net&_nc_ohc=KGaVDavuR4IAX_Zbeek&oh=2a1cca6654e9909028f284ab39e8062f&oe=5FA5DB25",
    }