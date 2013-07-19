def custom_callback(__kvlang__, idmap, *largs, **kwargs):
    idmap['args'] = largs
    exec(__kvlang__.co_value, idmap)