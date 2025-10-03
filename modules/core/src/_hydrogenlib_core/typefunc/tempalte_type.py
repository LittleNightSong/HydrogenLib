class Template:
    def __init__(self, **dct):
        self._template = dct

    @property
    def template(self):
        return self._template.copy()


def template_match(dic, template):
    from . import dict_func as dictx
    if dictx.is_sub_dict(template, dic) and dictx.is_parent_dict(template, dic):
        return True
    else:
        return False


def template_sort(dic, tem):
    # 修改字典使字典符合模板
    for i in tem.template:
        if i not in dic:
            dic[i] = tem.template[i]
    return dic


def template_sub(template: Template, data: dict):
    if data is None:
        return False
    from . import dict_func
    return dict_func.is_sub_dict(template.template, data)
