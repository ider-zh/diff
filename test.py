import unittest
from deep_diff import diff
import datetime
import time
class MyTestCase1(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_feature_eq_dict(self):
        dic1 = {'a':1}
        dic2 = {'a':1}
        ret = diff(dic1,dic2)
        assert not ret,ret


    def test_feature_eq_set(self):
        dic1 = set((1,3,2))
        dic2 = set((1,2,3))
        ret = diff(dic1,dic2)
        assert not ret,ret


    def test_feature_eq_list(self):
        dic1 = [1,2,3]
        dic2 = [1,2,3]
        ret = diff(dic1,dic2)
        assert not ret,ret

    def test_feature_diff_dict(self):
        dic1 = {'a':1}
        dic2 = {'a':1,'b':2}
        ret = diff(dic1,dic2)
        assert ret == [{'kind': 'N', 'path': ['b'], 'rhs': 2}],ret
        dic1 = {'a':1,'b':2}
        dic2 = {'a':1}
        ret = diff(dic1,dic2)
        assert ret == [{'kind': 'D', 'path': ['b'], 'lhs': 2}],ret

    def test_feature_diff_set(self):
        dic1 = {1,2,3,4,5}
        dic2 = {6,5,4,3,2}
        ret = diff(dic1,dic2)
        assert ret==[ {'kind': 'D', 'path': [], 'lhs': {1}},{'kind': 'N', 'path': [], 'rhs': {6}}],ret

    def test_feature_diff_list(self):
        dic1 = [1,2,3,4,5]
        dic2 = [1,3,3,4]
        ret = diff(dic1,dic2)
        assert ret==[{'kind': 'E', 'path': [1], 'lhs': 2, 'rhs': 3}, {'kind': 'A', 'path': [], 'item': {'kind': 'D', 'lhs': 5}, 'index': 4}],ret


    def test_feature_mulit_1(self):
        dic1 = [1,{'a':1,'b':1},3,4]
        dic2 = [1,{'a':1},3,4]
        ret = diff(dic1,dic2)
        assert ret==[{'kind': 'D', 'path': [1, 'b'], 'lhs': 1}],ret


    def test_feature_mulit_2(self):
        dic1 = {'a':1,'b':[1,2,3],'c':{1,2},'d':{'a':1},'f':[0,{1,2,3}]}
        dic2 = {'a':1,'b':[2,3],'c':{2,3},'d':{'a':1,'b':2},'f':[0,{2,3}]}
        ret = diff(dic1,dic2)
        assert ret==[{'kind': 'E', 'path': ['b',0], 'lhs': 1, 'rhs': 2}, 
                    {'kind': 'E', 'path': ['b', 1], 'lhs': 2, 'rhs': 3}, 
                    {'kind': 'A', 'path': ['b'], 'item': {'kind': 'D', 'lhs': 3}, 'index': 2}, 
                    {'kind': 'D', 'path': ['c'], 'lhs': {1}}, 
                    {'kind': 'N', 'path': ['c'], 'rhs': {3}}, 
                    {'kind': 'N', 'path': ['d', 'b'], 'rhs': 2},
                    {'kind': 'D', 'path': ['f', 1], 'lhs': {1}}
                    ],ret

    def test_feature_mulit_2(self):
        dic1 = {'a':[],'b':False}
        dic2 = {'a':None,'b':None}
        ret = diff(dic1,dic2)
        assert ret==[{'kind': 'E', 'path': ['a'], 'lhs': [], 'rhs': None}, {'kind': 'E', 'path': ['b'], 'lhs': False, 'rhs': None}],ret

if __name__ == '__main__':
    unittest.main()