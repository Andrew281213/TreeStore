import itertools
import operator


class TreeStore:
	def __init__(self, data):
		self.items = {item["id"]: item for item in data}
		self.childs = {
			cid: [item["id"] for item in data]
			for cid, data in itertools.groupby(self.items.values(), operator.itemgetter("parent"))
		}
	
	def getAll(self):
		return list(self.items.values())
	
	def getItem(self, idx):
		return self.items.get(idx)
	
	def getChildren(self, idx):
		return [self.getItem(child_id) for child_id in self.childs.get(idx, [])]
	
	def getAllParents(self, idx):
		item = self.getItem(idx)
		if item is None:
			return []
		parent = self.getItem(item["parent"])
		if parent is None:
			return []
		return [parent] + self.getAllParents(parent["id"])


if __name__ == '__main__':
	items = [
		{"id": 1, "parent": "root"},
		{"id": 2, "parent": 1, "type": "test"},
		{"id": 3, "parent": 1, "type": "test"},
		{"id": 4, "parent": 2, "type": "test"},
		{"id": 5, "parent": 2, "type": "test"},
		{"id": 6, "parent": 2, "type": "test"},
		{"id": 7, "parent": 4, "type": None},
		{"id": 8, "parent": 4, "type": None}
	]
	ts = TreeStore(items)
	print("getItem(7):", ts.getItem(7) == {"id": 7, "parent": 4, "type": None})
	# {"id":7,"parent":4,"type":None}
	print(
		"getChildren(4):",
		ts.getChildren(4) == [{"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]
	)
	# [{"id":7,"parent":4,"type":None},{"id":8,"parent":4,"type":None}]
	print("getChildren(5):", ts.getChildren(5) == [])
	# []
	print(
		"getAllParents(7):",
		ts.getAllParents(7) == [
			{"id": 4, "parent": 2, "type": "test"}, {"id": 2, "parent": 1, "type": "test"}, {"id": 1, "parent": "root"}
		]
	)
	# [{"id":4,"parent":2,"type":"test"},{"id":2,"parent":1,"type":"test"},{"id":1,"parent":"root"}]
