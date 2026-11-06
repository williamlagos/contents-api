import io
import json

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from contents.api.models import Content, ContentStatus, MediaAsset


class ContentsAPITestCase(TestCase):
    """Integration test suite for the modernized Django Ninja Contents API."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testeditor",
            email="editor@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="Editor",
        )
        self.sample_content = Content.objects.create(
            title="Introduction to Headless CMS",
            content="A complete modern architecture with Django Ninja and React.",
            summary="Overview of headless CMS architecture",
            author="Test Editor",
            category="Engineering",
            status=ContentStatus.PUBLISHED,
        )

    def test_root_health_check(self):
        """Verify root health check endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("health"), "OK")
        self.assertEqual(data.get("service"), "contents-api")

    def test_openapi_docs_endpoint(self):
        """Verify Swagger/OpenAPI documentation is served."""
        response = self.client.get("/api/docs")
        self.assertEqual(response.status_code, 200)

    def test_api_health_endpoint(self):
        """Verify /api/health returns system status."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["health"], "OK")
        self.assertEqual(data["status"], "operational")
        self.assertEqual(data["framework"], "django-ninja")

    def test_contents_crud_workflow(self):
        """Verify full CRUD lifecycle for Content items via Django Ninja."""
        # 1. List contents
        res = self.client.get("/api/contents/")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        self.assertGreaterEqual(len(items), 1)
        self.assertEqual(items[0]["title"], self.sample_content.title)
        self.assertEqual(items[0]["slug"], self.sample_content.slug)

        # 2. Count contents
        res = self.client.get("/api/contents/count")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["count"], 1)

        # 3. Create content
        new_payload = {
            "title": "Decentralized Publishing",
            "content": "Exploring ActivityPub and federated social networks.",
            "summary": "Deep dive into ActivityPub protocol",
            "author": "Alice",
            "category": "Social",
            "status": "published",
            "tags": ["activitypub", "federation"],
        }
        res = self.client.post(
            "/api/contents/",
            data=json.dumps(new_payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        created = res.json()
        self.assertEqual(created["title"], new_payload["title"])
        self.assertEqual(created["slug"], "decentralized-publishing")
        self.assertEqual(created["category"], "Social")
        created_id = created["id"]

        # Verify count incremented
        res = self.client.get("/api/contents/count")
        self.assertEqual(res.json()["count"], 2)

        # 4. Get content by id
        res = self.client.get(f"/api/contents/{created_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["author"], "Alice")

        # 5. Get content by slug
        res = self.client.get("/api/contents/slug/decentralized-publishing")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["title"], "Decentralized Publishing")

        # 6. Patch content
        patch_payload = {
            "title": "Updated Decentralized Publishing",
            "category": "Decentralization",
        }
        res = self.client.patch(
            f"/api/contents/{created_id}",
            data=json.dumps(patch_payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["title"], "Updated Decentralized Publishing")
        self.assertEqual(res.json()["category"], "Decentralization")

        # 7. Delete content
        res = self.client.delete(f"/api/contents/{created_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["message"], "Content deleted successfully")

        # Verify 404 after deletion
        res = self.client.get(f"/api/contents/{created_id}")
        self.assertEqual(res.status_code, 404)

    def test_content_filtering(self):
        """Verify content filtering by category, status, and search."""
        Content.objects.create(
            title="Draft Secrets",
            content="Top secret unpublished content",
            author="Bob",
            status="draft",
            category="Internal",
        )

        # Filter by status
        res = self.client.get("/api/contents/?status=draft")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Draft Secrets")

        # Filter by category
        res = self.client.get("/api/contents/?category=Engineering")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], self.sample_content.title)

        # Search filter
        res = self.client.get("/api/contents/?search=secret")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Draft Secrets")

    def test_media_assets_pipeline(self):
        """Verify media upload, listing, registration, and deletion."""
        # 1. Register remote media URL
        payload = {
            "title": "Cloud Banner",
            "file_url": "https://storage.googleapis.com/contents-bucket/banner.webp",
            "file_name": "banner.webp",
            "mime_type": "image/webp",
            "file_size": 10240,
            "alt_text": "Modern cloud banner",
        }
        res = self.client.post(
            "/api/media/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        media_id = res.json()["id"]

        # 2. Get media by id
        res = self.client.get(f"/api/media/{media_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["title"], "Cloud Banner")

        # 3. List media
        res = self.client.get("/api/media/")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.json()), 1)

        # 4. Upload multipart file
        dummy_file = SimpleUploadedFile(
            "test_image.png",
            b"fake-png-image-binary-data",
            content_type="image/png",
        )
        res = self.client.post(
            "/api/media/upload",
            data={"file": dummy_file, "alt_text": "Test image upload"},
        )
        self.assertEqual(res.status_code, 201)
        uploaded = res.json()
        self.assertEqual(uploaded["file_name"], "test_image.png")
        self.assertEqual(uploaded["mime_type"], "image/png")
        uploaded_id = uploaded["id"]

        # 5. Delete media
        res = self.client.delete(f"/api/media/{uploaded_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["message"], "Media asset deleted successfully")

    def test_plethora_cms_router(self):
        """Verify Plethora spreadable and playable endpoints."""
        # Create spreadable
        payload = {
            "name": "!announcement",
            "content": "Exciting new headless CMS features launched!",
            "spreaded": "efforia",
        }
        res = self.client.post(
            "/api/cms/spreadables",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["name"], "!announcement")
        self.assertEqual(res.json()["token"], "!")

        # List spreadables
        res = self.client.get("/api/cms/spreadables")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.json()), 1)

        # Create playable
        playable_payload = {
            "name": "!arcade_demo",
            "description": "Retro browser shooter game demo",
            "token": "TOK_DEMO_01",
            "category": 3,
            "credit": 50,
            "visual": "cover.png",
        }
        res = self.client.post(
            "/api/cms/playables",
            data=json.dumps(playable_payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["token"], "TOK_DEMO_01")

        # List playables
        res = self.client.get("/api/cms/playables")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.json()), 1)

    def test_social_router(self):
        """Verify ActivityPub social federation endpoints."""
        res = self.client.get("/api/social/actors")
        self.assertEqual(res.status_code, 200)
        actors = res.json()
        self.assertGreaterEqual(len(actors), 1)

        res = self.client.get("/api/social/actors/testeditor")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["username"], "testeditor")

        activity_payload = {
            "actor": "testeditor",
            "type": "Note",
            "content": "Federated greetings from Contents CMS!",
        }
        res = self.client.post(
            "/api/social/activities",
            data=json.dumps(activity_payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn("queued for federation", res.json()["message"])

    def test_shop_router(self):
        """Verify multi-rail commerce endpoints."""
        res = self.client.get("/api/shop/products")
        self.assertEqual(res.status_code, 200)
        products = res.json()
        self.assertEqual(len(products), 3)

        checkout_payload = {
            "product_id": 1,
            "payment_method": "stripe",
        }
        res = self.client.post(
            "/api/shop/checkout",
            data=json.dumps(checkout_payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        order = res.json()
        self.assertTrue(order["order_id"].startswith("ord_"))
        self.assertEqual(order["status"], "pending_payment")
        self.assertEqual(order["amount"], 29.0)

    def test_feeds_router(self):
        """Verify AI discovery feeds and search endpoints."""
        res = self.client.get("/api/feeds/trending")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/feeds/chronological")
        self.assertEqual(res.status_code, 200)

        search_payload = {"query": "headless", "top_k": 3}
        res = self.client.post(
            "/api/feeds/search",
            data=json.dumps(search_payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        matches = res.json()
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["title"], self.sample_content.title)
