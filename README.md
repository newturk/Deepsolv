# Shopify Store Insights Fetcher

A comprehensive application that fetches insights from Shopify stores without using the official Shopify API. The application extracts product catalogs, policies, FAQs, contact information, and more from any Shopify store.

## Features

### Mandatory Features
- **Product Catalog Extraction**: Fetches complete product listings from `/products.json`
- **Hero Products**: Identifies products featured on the homepage
- **Policy Information**: Extracts Privacy Policy, Return & Refund policies
- **Brand FAQs**: Scrapes frequently asked questions and answers
- **Social Media Handles**: Finds Instagram, Facebook, TikTok, and other social links
- **Contact Information**: Extracts email addresses and phone numbers
- **Brand Context**: Gathers information about the brand
- **Important Links**: Order tracking, Contact Us, Blogs, etc.

### Bonus Features
- **Competitor Analysis**: Identifies and analyzes competitor stores
- **Database Persistence**: MySQL storage for all extracted data
- **LLM Integration**: Uses AI to structure and organize scraped data

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **BeautifulSoup4**: HTML parsing and web scraping
- **Selenium**: Dynamic content extraction
- **Pydantic**: Data validation and serialization
- **MySQL**: Database for data persistence
- **OpenAI**: LLM integration for data structuring

### Frontend
- **React**: Modern UI framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server

## Project Structure

```
deepsolv/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   ├── scrapers/       # Web scraping modules
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API calls
│   │   └── types/          # TypeScript types
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Setup Instructions

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Database Setup**:
   ```bash
   # Configure MySQL connection in .env
   # Run database migrations
   alembic upgrade head
   ```

4. **Start Backend Server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Development Server**:
   ```bash
   npm run dev
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## API Endpoints

### POST `/api/insights`
Fetches insights from a Shopify store URL.

**Request Body**:
```json
{
  "website_url": "https://example.myshopify.com"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "brand_name": "Example Brand",
    "products": [...],
    "policies": {...},
    "faqs": [...],
    "social_handles": {...},
    "contact_info": {...},
    "brand_context": "...",
    "important_links": [...]
  }
}
```

## Usage Examples

### Testing with Postman
1. Send POST request to `http://localhost:8000/api/insights`
2. Include `website_url` in request body
3. View structured insights response

### Frontend Interface
1. Open `http://localhost:5173` in browser
2. Enter Shopify store URL
3. Click "Fetch Insights" to get results

## Deployment

### Netlify Frontend
1. Build the frontend: `npm run build`
2. Deploy `dist/` folder to Netlify
3. Configure environment variables

### Backend Hosting
- Deploy to platforms like Heroku, Railway, or DigitalOcean
- Ensure MySQL database is accessible
- Configure CORS for frontend domain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
