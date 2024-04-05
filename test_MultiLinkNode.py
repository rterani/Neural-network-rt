"""Testing for Asst Five"""
import pytest
from enum import Enum

#
# DO NOT MODIFY THIS CODE
#
try:
    import Neurode
except:
    pytest.fail("Neurode.py file is not present")


@pytest.fixture()
def implemented_MultiLinkNode():
    class implemented_mln(Neurode.MultiLinkNode):
        def _process_new_neighbor(self, node, side: Neurode.MultiLinkNode.Side):
            pass
    return implemented_mln


def test_MultiLinkNode():
    try:
        Neurode.MultiLinkNode
    except TypeError:
        pytest.fail("Is the MultiLinkNode class defined?")


def test_MultiLinkNode_is_ABC():
    try:
        Neurode.MultiLinkNode()
        pytest.fail("Is MultiLinkNode an Abstract Base Class?")
    except TypeError:
        pass


def test_Side(implemented_MultiLinkNode):
    my_node = implemented_MultiLinkNode()
    assert isinstance(my_node.Side, type(Enum)), \
        ("Is Side defined as an Enum?")
    try:
        my_node.Side.UPSTREAM
        my_node.Side.DOWNSTREAM
    except TypeError:
        pytest.fail("Are Side.UPSTREAM and Side.Downstream defined?")
    assert my_node.Side.UPSTREAM is not my_node.Side.DOWNSTREAM


def test_reporting_nodes(implemented_MultiLinkNode):
    my_node = implemented_MultiLinkNode()

    assert isinstance(my_node._reporting_nodes, dict), \
        ("Is _reporting_nodes defined as a dictionary")
    try:
        my_node._reporting_nodes[my_node.Side.UPSTREAM]
        my_node._reporting_nodes[my_node.Side.DOWNSTREAM]
    except:
        pytest.fail("Does _reporting_nodes have an entry for UPSTREAM "
                    "and DOWNSTREAM?")
    assert my_node._reporting_nodes[my_node.Side.UPSTREAM] \
        == 0, \
        "Is each entry of _reporting_nodes initially set to zero?"
    assert my_node._reporting_nodes[my_node.Side.DOWNSTREAM] \
           == 0, \
        "Is each entry of _reporting_nodes initially set to zero?"


def test_initial_reference_value(implemented_MultiLinkNode):
    my_node = implemented_MultiLinkNode()

    assert isinstance(my_node._reference_value, dict), \
        ("Is _reference_value defined as a dictionary")
    try:
        my_node._reference_value[my_node.Side.UPSTREAM]
        my_node._reference_value[my_node.Side.DOWNSTREAM]
    except:
        pytest.fail("Does _reference_value have an entry for UPSTREAM "
                    "and DOWNSTREAM?")
    assert my_node._reference_value[my_node.Side.UPSTREAM] \
           == 0, \
        "Is each entry of _reference_value initially set to zero?"
    assert my_node._reference_value[my_node.Side.DOWNSTREAM] \
           == 0, \
        "Is each entry of _reference_value initially set to zero?"


def test_copy_vs_deepcopy(implemented_MultiLinkNode):
    my_node = implemented_MultiLinkNode()
    # create two mutable objects as placeholders for nodes
    item_a = [1]
    item_b = [2]
    node_list = [item_a, item_b]
    my_node.reset_neighbors(node_list, my_node.Side.UPSTREAM)
    assert my_node._neighbors[my_node.Side.UPSTREAM] is not node_list, \
        ("After calling reset_neighbors, the _neighbors list is the same "
         "object as the list that was passed into the function. This gives "
         "the client access to _neighbors that it should not have")
    assert my_node._neighbors[my_node.Side.UPSTREAM][0] is item_a, \
        ("After calling reset_neighbors, the nodes in _neighbors should "
         "be the same objects as the nodes that were passed in (not "
         "copies)")
    assert my_node._neighbors[my_node.Side.DOWNSTREAM] == [], \
        ("After calling reset_neighbors with UPSTREAM data, DOWNSTREAM "
         "was changed")
    my_node.reset_neighbors(node_list, my_node.Side.DOWNSTREAM)
    assert my_node._neighbors[my_node.Side.DOWNSTREAM] is not node_list, \
        ("After calling reset_neighbors, the _neighbors list is the same "
         "object as the list that was passed into the function. This gives "
         "the client access to _neighbors that it should not have")
    assert my_node._neighbors[my_node.Side.DOWNSTREAM][0] is item_a, \
        ("After calling reset_neighbors, the nodes in _neighbors should "
         "be the same objects as the nodes that were passed in (not "
         "copies)")


def test_final_reference_value(implemented_MultiLinkNode):
    my_node = implemented_MultiLinkNode()
    # create three immutable objects as placeholders for nodes
    item_a = (1,)
    item_b = (2,)
    item_c = (3,)
    node_list_one = [item_a, item_b]
    node_list_two = [item_a, item_b, item_c]
    my_node.reset_neighbors(node_list_one, my_node.Side.UPSTREAM)
    assert my_node._reference_value[my_node.Side.UPSTREAM] == 3, \
        "UPSTREAM _reference_value is incorrect after loading two nodes"
    assert my_node._reference_value[my_node.Side.DOWNSTREAM] == 0, \
        ("DOWNSTREAM _reference_value was changed after loading "
         "UPSTREAM nodes")
    my_node.reset_neighbors(node_list_two, my_node.Side.DOWNSTREAM)
    assert my_node._reference_value[my_node.Side.DOWNSTREAM] == 7, \
        "UPSTREAM _reference_value is incorrect after loading two nodes"
    assert my_node._reference_value[my_node.Side.UPSTREAM] == 3, \
        ("DOWNSTREAM _reference_value was changed after loading "
         "UPSTREAM nodes")


def test_neighbors_reset_before_loading_new_nodes(implemented_MultiLinkNode):
    my_node = implemented_MultiLinkNode()
    # create three immutable objects as placeholders for nodes
    item_a = (1,)
    item_b = (2,)
    item_c = (3,)
    node_list_one = [item_a, item_b]
    node_list_two = [item_c]
    my_node.reset_neighbors(node_list_one, my_node.Side.UPSTREAM)
    my_node.reset_neighbors(node_list_two, my_node.Side.UPSTREAM)
    assert item_a not in my_node._neighbors[my_node.Side.UPSTREAM]
    assert my_node._reference_value[my_node.Side.UPSTREAM] == 1, \
        ("UPSTREAM _reference_value is incorrect after calling "
         "reset_neighbors a second time")
    assert my_node._reference_value[my_node.Side.DOWNSTREAM] == 0, \
        ("DOWNSTREAM _reference_value was changed after loading "
         "UPSTREAM nodes")
