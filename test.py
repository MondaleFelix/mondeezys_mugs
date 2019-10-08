from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_mug_id = ObjectId("5d55cffc4a3d4031f42827a3")

sample_mug = {
	"mug_name" : "Test Mug",
	"description" : "This is some cool mug!",
	"price": "3",
	"color" : "pink"
}

sample_form_data = {
	"mug_name" : sample_mug["mug_name"],
	"description" : sample_mug["description"],
	"price": sample_mug["price"],
	"color": sample_mug["color"]
}


class MugsTests(TestCase):
	def setUp(self):
		self.client = app.test_client()

		app.config["TESTING"] = True

	def test_index(self):
		result = self.client.get('/')
		self.assertEqual(result.status, "200 OK")
		self.assertIn(b'Mug', result.data)

	def test_new(self):
		result = self.client.get("mugs/new")
		self.assertEqual(result.status, "200 OK")
		self.assertIn(b"New Mug", result.data)

	@mock.patch("pymongo.collection.Collection.find_one")
	def test_show_mug(self, mock_find):
		mock_find.return_value = sample_mug

		result = self.client.get(f"/mugs/{sample_mug_id}")
		self.assertEqual(result.status, "200 OK")
		self.assertIn(b"Test Mug", result.data)

	@mock.patch("pymongo.collection.Collection.find_one")
	def test_edit_mug(self, mock_find):
		mock_find.return_value = sample_mug

		result = self.client.get(f"/mugs/{sample_mug_id}/edit")
		self.assertEqual(result.status, "200 OK")
		self.assertIn(b"Test Mug", result.data)

	@mock.patch("pymongo.collection.Collection.insert_one")
	def test_submit_mug(self, mock_insert):

		result = self.client.post("/mugs", data = sample_form_data)

		self.assertEqual(result.status, "302 FOUND")
		mock_insert.assert_called_with(sample_mug)

	@mock.patch("pymongo.collection.Collection.update_one")
	def test_update_mug(self, mock_update):
		result = self.client.post(f'/mugs/{sample_mug_id}' , data = sample_form_data)

		self.assertEqual(result.status, "302 FOUND")
		mock_update.assert_called_with({"_id" : sample_mug_id}, {"$set": sample_mug})

	@mock.patch("pymongo.collection.Collection.delete_one")
	def test_delete_mug(self, mock_delete):
		form_data = {"_method": "DELETE"}
		result = self.client.post(f"/mugs/{sample_mug_id}/delete", data = form_data)
		self.assertEqual(result.status, "302 FOUND")
		mock_delete.assert_called_with({"_id" : sample_mug_id})



if __name__ == '__main__':
    unittest_main()		