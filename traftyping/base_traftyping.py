import trafaret as t

from typing import Callable, TypeVar, List, Type


STD_TYPES = {
    int: t.Int,
    str: t.String,
    list: t.List(t.Any),
    List: t.List(t.Any)
}


class ConstructTrafError(ValueError):
    pass


def construct_traf(f: Callable, prev_classes=()):
    def create_type_arg(type_arg):
        if type_arg:
            if type_arg in STD_TYPES:
                return STD_TYPES[type_arg]
            elif getattr(type_arg, "_gorg", None) == List:
                return t.List(
                    *map(
                        lambda t_a: create_type_arg(t_a),
                        type_arg.__args__)
                )
            else:
                if isinstance(type_arg, type) and getattr(type_arg, '__init__', False):
                    if type_arg.__class__ in prev_classes:
                        raise ConstructTrafError(f"Can't init recursion class \"{type_arg.__class__}\"")
                    else:
                        return construct_traf(type_arg.__init__, prev_classes + (type_arg.__class__,))

            raise ConstructTrafError(f"Can't find type arg {name_arg}")
        else:
            return t.Any

    return t.Dict({
        name_arg: create_type_arg(f.__annotations__.get(name_arg, None)) \
        for name_arg in filter(lambda a: a != "self", f.__code__.co_varnames)
    })


def init_cls_from_trafareted_dict(cls: type, d: dict):
    for k in d.keys():
        if isinstance(d[k], dict):
            k_cls = cls.__init__.__annotations__[k]

            d[k] = init_cls_from_trafareted_dict(k_cls, d[k])
        elif isinstance(d[k], list):
            for i in range(len(d[k])):

                if isinstance(d[k][i], dict):
                    k_cls = list(
                        filter(
                            lambda t: isinstance(t, type),
                            cls.__init__.__annotations__[k].__args__
                        )
                    )[0]

                    d[k][i] = init_cls_from_trafareted_dict(k_cls, d[k][i])

    return cls(**d)


T = TypeVar('T')


class MetaBaseTraftyping(type):
    @property
    def trafaret(cls):
        if not(getattr(cls, '_trafaret', None)):
            cls._trafaret = construct_traf(cls.__init__)

        return cls._trafaret

    def init_from_dict(cls: T, d: dict) -> Type[T]:
        trafateted_d: dict = cls.trafaret(d)

        return init_cls_from_trafareted_dict(cls, trafateted_d)


class BaseTraftyping(metaclass=MetaBaseTraftyping):
    trafaret: t.Dict

