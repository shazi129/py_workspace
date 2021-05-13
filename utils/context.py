#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @file context
# @brief
# @author vinowan
# @date 2019-05-15


class Context:
    """
    作为一个记录上下文环境的Namespace
    基本的用法如下：

    ctx = Context()
    ctx.a = 1
    ctx.update({'b': 2})
    print(ctx.b)

    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def update(self, other):
        self.__dict__.update(other)

    def __str__(self) -> str:
        return "%s" % self.__dict__

if __name__ == "__main__":
    ctx = Context()
    ctx.a = 1
    ctx.update({'b': 2})
    print(ctx.b)
    print(ctx)