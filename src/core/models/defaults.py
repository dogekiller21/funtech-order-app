from sqlalchemy import text


class ServerDefault:
    now = text("CURRENT_TIMESTAMP")
    uuid = text("gen_random_uuid()")
    true = "true"
    false = "false"
    zero = "0"
    empty_dict = "{}"


class OnDelete:
    cascade = "CASCADE"
    set_null = "SET NULL"
    restrict = "RESTRICT"
