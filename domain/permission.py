class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

    def __setattr__(self, key, value):
        raise AttributeError(f'Cannot set value: {value} to {key}')
