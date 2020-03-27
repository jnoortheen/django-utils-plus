def build_attrs(**attrs) -> str:
    return " ".join(
        [
            (str(k) + ('="' if v else '') + str(v) + ('"' if v else ''))
            for k, v in attrs.items()]
    )


def script_tag(**attrs) -> str:
    return "<script " + build_attrs(**attrs) + "></script>"


def link_css_tag(**attrs) -> str:
    attrs['rel'] = "stylesheet"
    attrs['type'] = "text/css"
    return "<link " + build_attrs(**attrs) + "/>"
