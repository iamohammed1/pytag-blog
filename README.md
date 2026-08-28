# pytag-blog
# Django Blog App 📝

A full-featured blogging platform built with **Django**, featuring tagging, full-text search, comments, and email sharing — designed as a solid foundation for a production-ready blog.
<img width="1916" height="900" alt="Screenshot 2026-08-28 080807" src="https://github.com/user-attachments/assets/fbee1677-9267-4e79-aa9d-cec91b64f996" />

## ✨ Features

- **Post Listing & Pagination** — Browse published posts with paginated views.
- **Tagging System** — Filter posts by tag using [`django-taggit`](https://github.com/jazzband/django-taggit).
- **Post Detail Pages** — View individual posts with related/similar posts suggested based on shared tags.
- **Comment System** — Readers can leave comments on posts; comments can be moderated via the `active` flag.
- **Share via Email** — Send a post to a friend by email directly from the post detail page.
- **Full-Text Search** — PostgreSQL-powered search (`SearchVector`, `SearchQuery`, `SearchRank`) that ranks results by relevance.
- **SEO-Friendly Sitemap** — Auto-generated sitemap for search engine indexing.

## 🛠️ Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL (required for full-text search features)
- **Tagging:** django-taggit
- **Email:** Django's built-in `send_mail`

## 📂 Project Structure

```
blogapp/
├── models.py       # Post & Comment models
├── views.py        # Post list, detail, share, comment, and search views
├── forms.py        # EmailPostForm, CommentForm, SearchForm
├── urls.py         # URL routing
├── sitemaps.py     # SEO sitemap configuration
└── templates/
    └── blogapp/
        ├── list.html
        ├── detail.html
        ├── share.html
        ├── comment.html
        └── search.html
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/<iamohammed1>/<pytah-blog>.git
   cd <your-repo>
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install django django-taggit psycopg2-binary
   ```

4. Configure your PostgreSQL database in `settings.py`
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Add required apps to `INSTALLED_APPS`
   ```python
   INSTALLED_APPS = [
       ...
       'django.contrib.sitemaps',
       'taggit',
       'blogapp',
   ]
   ```

6. Run migrations
   ```bash
   python manage.py migrate
   ```

7. Create a superuser (to add posts via the admin panel)
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server
   ```bash
   python manage.py runserver
   ```

## 🔗 URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `post_list` | List all published posts |
| `/tag/<tag_slug>/` | `post_list` | List posts filtered by tag |
| `/<year>/<month>/<day>/<slug>/` | `post_detail` | View a single post |
| `/<post_id>/share/` | `post_share` | Share a post via email |
| `/<post_id>/comment/` | `post_comment` | Submit a comment on a post |
| `/search/` | `post_search` | Full-text search across posts |

## 📧 Email Configuration

The `post_share` view uses Django's `send_mail`. For local testing, add this to `settings.py` to print emails to the console instead of sending them:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

For production, configure an SMTP backend (e.g. Gmail, SendGrid, Mailgun).

## 🗺️ Roadmap / Ideas for Improvement

- [ ] Add pagination to search results
- [ ] Add a class-based `PostListView` (already scaffolded, currently commented out)
- [ ] Add rich text editing for post creation
- [ ] Add user authentication for commenting
- [ ] Add unit tests

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Made with ❤️ using Django.
