# Boutique — Luxury E-Commerce Django Project

<p align="center">
  <strong>Qualità senza compromessi.</strong>
</p>

<p align="center">
  A refined, multi-language luxury e-commerce web application built with Django, featuring an elegant Italian-branded storefront with interactive search, favorites, and shopping cart functionality.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0-092E20?logo=django" alt="Django 6.0" />
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap" alt="Bootstrap 5.3" />
  <img src="https://img.shields.io/badge/Languages-5-orange" alt="5 Languages" />
</p>

---

## ✨ Features

### 🛍️ Product Management
- **Full CRUD** — Create, read, update, and delete products
- **Image uploads** — Upload product images with live preview
- **Categories** — 15 luxury categories pre-loaded (Uomo, Donna, Accessori, Luxury, etc.)
- **Code-gated admin** — Products can only be added/modified/deleted after entering access code `2005zakaria`
- **Category management** — Dedicated page to create and browse categories (admin-only)
- **Admin exit** — One-click button to leave admin mode from any page

### 🌍 Multi-Language Support
- **5 languages** — Italian, English, French, Spanish, German
- **Session-based switching** — Language saved via cookie for seamless UX
- **Complete translations** — All templates, models, and messages translated

### 🎨 Luxury UI/UX
- **Elegant design** — Warm neutral palette (cream, sand, linen, taupe, bark)
- **Typography** — Cormorant Garamond (display) + DM Sans (body)
- **Responsive** — Fully responsive with mobile navigation
- **Animations** — Hero text fade-up, scroll-triggered section reveals, stats counter animation, card hover effects, image zoom, nav shrink on scroll
- **Toast notifications** — Slide-in toast messages for cart/favorites/newsletter actions
- **Back to top** — Floating button appears on scroll

### 🔍 Interactive Features
- **Search overlay** — Full-screen search with blur backdrop + Enter key navigates to filtered product page
- **Server-side search** — Global search queries product name, description, and category
- **Favorites panel** — Slide-in panel with localStorage persistence + toast feedback
- **Shopping cart** — Cart panel with quantity +/- adjust, subtotal per item, total calculation + toast feedback
- **Badge counters** — Live counts on favorites and cart icons
- **Quick-add cart** — Add-to-cart button overlays product card images on hover

### 📧 Contact Form
- **Full form** — Name, surname, email, phone, subject, message
- **Validation** — Required field validation with error messages
- **Success feedback** — Confirmation message with 24-hour response promise
- **Info cards** — Address, email, business hours, and social links displayed alongside the form

---

## 📁 Project Structure

```
ecommerce/
├── ecommerce/                  ← Main Django configuration
│   ├── __init__.py
│   ├── settings.py             ← Project settings with i18n config
│   ├── urls.py                 ← Root URL routing
│   ├── wsgi.py                 ← WSGI application
│   └── asgi.py                 ← ASGI application
├── myapp/
│   ├── templates/
│   │   └── myapp/
│   │       ├── layout.html              ← Base template (navbar, footer, overlays)
│   │       ├── home.html                ← Homepage with hero + featured products
│   │       ├── lista_prodotti.html      ← Product catalog with search & filters
│   │       ├── dettaglio_prodotto.html  ← Product detail page (image, cart, related)
│   │       ├── form_prodotti.html       ← Product add/edit form (code-gated)
│   │       ├── gestione_categorie.html  ← Category management (admin-only)
│   │       └── contatti.html            ← Contact form page
│   ├── models.py               ← Categoria & Prodotto models with image support
│   ├── views.py                ← All view logic (home, products, contact)
│   ├── urls.py                 ← App URL routing
│   ├── admin.py                ← Admin panel configuration
│   └── migrations/             ← Database migrations
├── locale/                     ← Translation files
│   ├── it/LC_MESSAGES/         ← Italian (source language)
│   ├── en/LC_MESSAGES/         ← English translations
│   ├── fr/LC_MESSAGES/         ← French translations
│   ├── es/LC_MESSAGES/         ← Spanish translations
│   └── de/LC_MESSAGES/         ← German translations
├── media/                      ← User-uploaded product images
├── venv/                       ← Python virtual environment
├── db.sqlite3                  ← SQLite database
├── manage.py                   ← Django management script
└── README.md                   ← This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

### 1. Clone or download the project

```bash
cd ecommerce
```

### 2. Create and activate virtual environment

```bash
py -3.12 -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install django pillow polib
```

| Package | Purpose |
|---------|---------|
| `django` | Web framework |
| `pillow` | Image processing for product uploads |
| `polib` | Translation file compilation |

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Seed luxury categories (optional)

```python
python manage.py shell
```

```python
from myapp.models import Categoria

categories = [
    ('Uomo', 'Collezione maschile elegante e sofisticata'),
    ('Donna', 'Collezione femminile raffinata e moderna'),
    ('Accessori', 'Dettagli che fanno la differenza'),
    ('Scarpe', 'Calzature di lusso per ogni occasione'),
    ('Nuovi Arrivi', 'Le ultime novità della stagione'),
    ('Offerte', 'Offerte esclusive su prodotti selezionati'),
    ('Collezione Primavera', 'Ispirata alla rinascita e alla leggerezza'),
    ('Collezione Estate', 'Stile e comfort per la stagione calda'),
    ('Elegante', 'Per le occasioni speciali e gli eventi'),
    ('Casual', 'Comfort e stile per ogni giorno'),
    ('Sport', 'Performance e design per gli attivi'),
    ('Luxury', 'Il meglio della produzione artigianale'),
    ('Best Seller', 'I più amati dai nostri clienti'),
    ('Edizione Limitata', 'Pezzi unici e introvabili'),
    ('Tendenze 2026', 'Ciò che definirà lo stile di quest\'anno'),
]

for nome, desc in categories:
    Categoria.objects.get_or_create(nome=nome, defaults={'descrizione': desc})
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 📄 Available Pages

| URL | Description | Access |
|-----|-------------|--------|
| `/` | Homepage with hero section, stats, and featured products | Public |
| `/prodotti/` | Full product catalog with live search, category filter, and quick-add cart | Public |
| `/prodotti/<id>/` | Product detail page with image zoom, quantity selector, add-to-cart, related products | Public |
| `/prodotti/nuovo/` | Add new product form with image upload | Code `2005zakaria` |
| `/prodotti/modifica/<id>/` | Edit existing product | Code `2005zakaria` |
| `/categorie/` | Browse and create categories | Code `2005zakaria` |
| `/esci-admin/` | Exit admin mode | Admin only |
| `/contatti/` | Contact form with info cards and social links | Public |
| `/admin/` | Django admin panel | Superuser |

---

## 🌐 Supported Languages

| Code | Language | Example Navigation |
|------|----------|-------------------|
| `it` | Italiano | Pagina Iniziale, Prodotti, Categorie, Contatti |
| `en` | English | Home, Products, Categories, Contact |
| `fr` | Français | Accueil, Produits, Catégories, Contact |
| `es` | Español | Inicio, Productos, Categorías, Contacto |
| `de` | Deutsch | Startseite, Produkte, Kategorien, Kontakt |

**To switch languages:** Click the globe icon (🌐) in the top-right navigation bar and select your preferred language. The choice is saved in a cookie.

---

## 🗄️ Database Models

### Categoria (Category)
| Field | Type | Description |
|-------|------|-------------|
| `nome` | CharField(100) | Category name |
| `descrizione` | TextField | Category description (optional) |

### Prodotto (Product)
| Field | Type | Description |
|-------|------|-------------|
| `nome` | CharField(200) | Product name |
| `descrizione` | TextField | Product description |
| `quantita` | PositiveIntegerField | Stock quantity |
| `prezzo` | DecimalField | Price (EUR) |
| `immagine` | ImageField | Product image (optional) |
| `categoria` | ForeignKey → Categoria | Product category |
| `data_inserimento` | DateTimeField | Date added |
| `data_aggiornamento` | DateTimeField | Last updated |

---

## 🎨 Design System

### Color Palette
| Token | Hex | Usage |
|-------|-----|-------|
| `--cream` | `#F7F4EF` | Page background |
| `--sand` | `#EDE9E1` | Secondary backgrounds |
| `--linen` | `#D9D3C7` | Borders, subtle elements |
| `--taupe` | `#9C9084` | Secondary text |
| `--bark` | `#5C5040` | Dark accents |
| `--ink` | `#1E1B17` | Primary text, buttons |
| `--accent` | `#8B6F47` | Highlights, links |
| `--accent-lt` | `#C4A882` | Subtle highlights |
| `--white` | `#FFFFFF` | Card backgrounds |
| `--danger` | `#B04040` | Error states, delete |

### Typography
| Font | Weight | Usage |
|------|--------|-------|
| Cormorant Garamond | 300-500 | Headings, prices, display text |
| DM Sans | 300-500 | Body text, labels, navigation |

---

## 🔧 Configuration

### Key Settings (`ecommerce/settings.py`)

```python
# Languages
LANGUAGES = [
    ('it', 'Italiano'),
    ('en', 'English'),
    ('fr', 'Français'),
    ('es', 'Español'),
    ('de', 'Deutsch'),
]

# Media files (product images)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Localization
LANGUAGE_CODE = 'it'
TIME_ZONE = 'Europe/Rome'
LOCALE_PATHS = [BASE_DIR / 'locale']
```

### Middleware Order (important for i18n)
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # ← Must be after sessions
    'django.middleware.common.CommonMiddleware',
    ...
]
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 6.0.4 | Web framework |
| Pillow | 12.2.0 | Image processing |
| Bootstrap | 5.3.3 | UI components (CDN) |
| Bootstrap Icons | 1.11.3 | Icon library (CDN) |
| Google Fonts | — | Cormorant Garamond + DM Sans (CDN) |

---

## 🛠️ Development

### Running the server
```bash
venv\Scripts\activate
python manage.py runserver
```

### Creating new migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Compiling translations
```bash
# After adding {% trans %} tags to templates:
python -c "import polib; [polib.pofile(f'locale/{lang}/LC_MESSAGES/django.po').save_as_mofile(f'locale/{lang}/LC_MESSAGES/django.mo') for lang in ['it','en','fr','es','de']]"
```

### Accessing the admin panel
1. Go to **http://127.0.0.1:8000/admin/**
2. Log in with the superuser credentials you created
3. Manage products, categories, and users

---

## 📱 Interactive Features

### Search Overlay
- Click the 🔍 search icon in the navbar
- Full-screen overlay with blur backdrop
- Auto-focuses input field
- **Press Enter** to navigate to `/prodotti/?q=<query>` with server-side filtered results
- Closes with Escape key or clicking outside

### Favorites Panel
- Click the ❤️ heart icon in the navbar
- Slide-in panel from the right
- Items stored in `localStorage` (persists across sessions)
- Red badge counter shows number of favorites
- Toast notification on add/remove

### Shopping Cart
- Click the 🛒 bag icon in the navbar
- Slide-in panel with item list, **quantity +/- adjust buttons**, subtotal per item, and total
- Items stored in `localStorage`
- Toast notification on add
- Supports quantity management and removal
- Red badge counter shows total items (aggregates quantities)
- **Quick-add**: hover product cards in catalog to show an add-to-cart button overlay

### Product Detail Page
- **Image zoom** — CSS scale effect on hover (crosshair cursor)
- **Quantity selector** — +/- buttons before adding to cart
- **Add to Cart** — Primary button with toast confirmation
- **Add to Favorites** — Heart toggle button with toast
- **Related products** — Up to 4 products from the same category

### Admin Mode
- Enter code `2005zakaria` on the **Add Product** page to unlock admin features
- Admin sees: Add Product, Categories, Unlock/Edit/Delete buttons throughout the site
- **Exit admin** button available on every admin-protected page and in the nav

### Toast Notifications
- Slide-in from top-right, auto-dismiss after 2.5 seconds
- Shown for add-to-cart, add-to-favorites, newsletter signup

### Scroll Animations
- **Hero**: Staggered fade-up animation on page load (subtitle → title → CTA)
- **Sections**: Fade-up + translateY on scroll via `IntersectionObserver`
- **Stats**: Number counter animation (0 → target) when stats bar scrolls into view
- **Nav**: Shrinks from 68px → 56px on scroll down

### Back to Top
- Floating circle button appears after scrolling 300px
- Smooth-scrolls to top on click

### Announcement Bar
- Dismissible announcement bar with &times; button
- Preference saved to `localStorage` (stays hidden across sessions)

### JavaScript API
```javascript
// Add item to cart (with toast notification)
addToCart('Product Name', 29.99, 1);

// Add item to favorites (with toast notification)
addToFavorites('Product Name', 'Category');

// Show a custom toast
showToast('Your message', 'bi-check-circle');

// Open panels programmatically
toggleSearch();
toggleFavorites();
toggleCart();
```

---

## 📝 License

This project is for educational and portfolio purposes.

---

## 📄 Interactive Features (Detailed)

### Footer
- **Newsletter signup** — Email input with toast confirmation
- **Social icons** — Instagram, Facebook, Pinterest with hover effects
- **Payment icons** — Visa, Mastercard, PayPal displayed in copyright bar

---

## 👨‍💻 Author

Built with ❤️ using Django, Bootstrap, and Italian craftsmanship.
