def test_Choices_ordering():
    from .test_app.choices import COLOR_TYPE
    for c in COLOR_TYPE:
        members = list(COLOR_TYPE)
        index = members.index(c)
        for i, mem in enumerate(members):
            assert (i < index) == (mem < c)
            assert (i == index) == (mem == c)
            assert (i > index) == (mem > c)
