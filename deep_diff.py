'''deep diff dict list set'''

from collections import OrderedDict


def diff_set(set1,set2):
    diff_post = []
    rd = set1 - set2
    ld = set2 - set1
    if rd:
        diff_post.append({'kind':'D','path':[],'lhs':rd,})
    if ld:
        diff_post.append({'kind':'N','path':[],'rhs':ld,})
    return diff_post

def diff_list(list1, list2):
    diff_post = []
    for i,(a,b) in enumerate(list(zip(list1,list2))):
        router(a,b,diff_post,i)
    if len(list1) > len(list2):
        for i in range(len(list2),len(list1)):
            diff_post.append({'kind':'A','path':[],"item": {'kind':'D','lhs':list1[i]},'index':i})
    elif len(list1) < len(list2):
        for i in range(len(list1),len(list2)):
            diff_post.append({'kind':'A','path':[],"item": {'kind':'N','rhs':list2[i]},'index':i})
    return diff_post

def diff_dict(d1, d2):
    diff_post = []
    for e in sorted(list(set(d1.keys()) - set(d2.keys()))):
        diff_post.append({'kind':'D','path':[e],"lhs": d1[e]})
    for e in sorted(list(set(d2.keys()) - set(d1.keys()))):
        diff_post.append({'kind':'N','path':[e],"rhs": d2[e]})
    for k, v1 in sorted(d1.items()):
        if k in d2:
            v2 = d2[k]
            router(v1,v2,diff_post,k)
    return diff_post


def router(dict1,dict2,diff_post,k=None):
    if isinstance(dict1,dict) and isinstance(dict2,dict):
        ret_list = diff_dict(dict1, dict2)
        if k !=None:
            list(map(lambda x:x['path'].insert(0,k),ret_list))
        diff_post.extend(ret_list)

    elif isinstance(dict1,list) and isinstance(dict2,list):
        ret_list = diff_list(dict1, dict2)
        if k !=None:
            list(map(lambda x:x['path'].insert(0,k),ret_list))
        diff_post.extend(ret_list)

    elif isinstance(dict1,set) and isinstance(dict2,set):
        ret_list = diff_set(dict1, dict2)
        if k !=None:
            list(map(lambda x:x['path'].insert(0,k),ret_list))
        diff_post.extend(ret_list)

    elif dict1 != dict2:
        if k !=None:
            diff_post.append({'kind':'E','path':[k],'lhs':dict1,'rhs':dict2})
        else:
            diff_post.append({'kind':'E','path':[],'lhs':dict1,'rhs':dict2})


def diff(dict1, dict2):
    def order_element(element):
        if isinstance(element,list):
            return [order_element(el) for el in element]
        elif isinstance(element, dict):
            return OrderedDict([(key, order_element(v)) for key, v in sorted(element.items())])
        else:
            return element

        if dict1 == dict2:
            return None

    diff_post = []
    d1 = order_element(dict1)
    d2 = order_element(dict2)
    router(d1,d2,diff_post)
    return diff_post
