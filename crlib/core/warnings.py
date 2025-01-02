def warning(func):
    "Warning functions decorator"

    def warning_wrapper(*a, **kw):
        if not hasattr(warning, "warning"):
            setattr(warning, "warning", False)
        if hasattr(warning, "name_exceptions") and func.__name__ in getattr(
            warning, "name_exceptions"
        ):
            pass
        elif getattr(warning, "warning", False):
            return func(*a, **kw)

    return warning_wrapper


def disable():
    setattr(warning, "warning", False)


def enable():
    setattr(warning, "warning", True)


def add_name_exceptions(*func_names):
    if not hasattr(warning, "name_exceptions") or not isinstance(
        getattr(warning, "name_exceptions"), list
    ):
        setattr(warning, "name_exceptions", [])
    getattr(warning, "name_exceptions").extend(func_names)


def remove_name_exceptions(*func_names):
    if hasattr(warning, "name_exceptions"):
        if not func_names:
            getattr(warning, "name_exceptions").clear()
        setattr(
            warning,
            "name_exceptions",
            list(i for i in getattr(warning, "name_exceptions") if not i in func_names),
        )


@warning
def warn(text: str, warn_text: str = "WARNING: ", color_code: str = "93"):
    print(
        f"\033[{color_code}{'m' if color_code[-1]!='m' else ''}{warn_text+text}\033[0m"
    )


enable()
