import os

os.environ["DATABASE_URL"] = 'postgresql:///cupcakes_test'

from unittest import TestCase

from app import app
from models import db, Cupcake

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        """Test getting all cupcakes."""
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [{
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }]
            })

    def test_get_cupcake(self):
        """Test getting cupcake."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })



    def test_create_cupcake(self):
        """Test create cupcake."""
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            cupcake_id = resp.json['cupcake']['id']

            # don't know what ID we'll get, make sure it's an int
            self.assertIsInstance(cupcake_id, int)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": cupcake_id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_patch_cupcake(self):
        """Test patch cupcake info."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(url, json={
                        "size": "UpdatedSize2",
                        "rating": 5,
                        })

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "UpdatedSize2",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })

    def test_patch_entire_cupcake(self):
        """Test patch all cupcake info."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(url, json={
                        "flavor": "UpdatedTestFlavor2",
                        "size": "UpdatedSize2",
                        "rating": 5,
                        "image_url": "https://natashaskitchen.com/wp-content/uploads/2020/05/Vanilla-Cupcakes-3.jpg"
                    })

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "UpdatedTestFlavor2",
                    "size": "UpdatedSize2",
                    "rating": 5,
                    "image_url": "https://natashaskitchen.com/wp-content/uploads/2020/05/Vanilla-Cupcakes-3.jpg"
                }
            })

    def test_patch_nonexistent_cupcake(self):
        """Test patch nonexistent cupcake."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{1000}"
            resp = client.patch(url, json={
                        "size": "UpdatedSize2",
                        "rating": 5
                    })

            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake(self):
        """Test delete cupcake."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(int(resp.json['deleted']), self.cupcake_id)
            self.assertEqual(Cupcake.query.count(), 0)


    def test_delete_nonexistent_cupcake(self):
        """Test delete nonexists cupcake. Should get 404."""
        with app.test_client() as client:
            url = "/api/cupcakes/10000"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)


