# Shopify Store Insights Fetcher - Setup Guide

This guide will help you set up and run the Shopify Store Insights Fetcher application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download Git](https://git-scm.com/)

## Quick Start (Windows)

### Option 1: Using Batch Files (Recommended for Windows)

1. **Start Backend Server:**
   - Double-click `start_backend.bat`
   - Wait for dependencies to install and server to start
   - Backend will be available at: http://localhost:8000

2. **Start Frontend (in a new terminal):**
   - Double-click `start_frontend.bat`
   - Wait for dependencies to install and server to start
   - Frontend will be available at: http://localhost:5173

### Option 2: Manual Setup

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your configuration
# Update DATABASE_URL with your MySQL credentials
DATABASE_URL=mysql+mysqlconnector://username:password@localhost/shopify_insights
```

### 3. Set Up MySQL Database

```sql
-- Connect to MySQL and run:
CREATE DATABASE shopify_insights;
CREATE USER 'shopify_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON shopify_insights.* TO 'shopify_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at:
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Main Endpoint:** http://localhost:8000/api/insights

## Frontend Setup

### 1. Install Node.js Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will be available at: http://localhost:5173

## Testing the Application

### 1. Test Backend API

You can test the backend using the interactive API documentation:

1. Open http://localhost:8000/docs in your browser
2. Try the `/api/insights` endpoint with a Shopify store URL
3. Example URLs to test:
   - https://memy.co.in
   - https://hairoriginals.com
   - https://colourpop.com

### 2. Test Frontend

1. Open http://localhost:5173 in your browser
2. Enter a Shopify store URL
3. Click "Fetch Insights" to see the results

### 3. Test with Postman

```http
POST http://localhost:8000/api/insights
Content-Type: application/json

{
  "website_url": "https://memy.co.in"
}
```

## Project Structure

```
deepsolv/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # Pydantic models & database models
│   │   ├── services/       # Business logic
│   │   ├── scrapers/       # Web scraping modules
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── env.example        # Environment configuration
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API calls
│   │   └── types/          # TypeScript types
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── start_backend.bat       # Windows backend starter
├── start_frontend.bat      # Windows frontend starter
└── README.md               # Project documentation
```

## Features Implemented

### ✅ Mandatory Requirements
- **Product Catalog Extraction** - Fetches all products from `/products.json`
- **Hero Products** - Identifies products featured on homepage
- **Policy Information** - Privacy, return, refund policies
- **Brand FAQs** - Frequently asked questions and answers
- **Social Media Handles** - Instagram, Facebook, Twitter, etc.
- **Contact Information** - Emails, phone numbers, addresses
- **Brand Context** - About the brand information
- **Important Links** - Order tracking, contact, blogs, etc.

### ✅ Bonus Features
- **Competitor Analysis** - Framework for competitor identification
- **Database Models** - MySQL-ready database schema
- **LLM Integration** - Prepared for OpenAI integration
- **Modern UI** - Beautiful React frontend with Tailwind CSS

## Troubleshooting

### Common Issues

1. **Backend won't start:**
   - Check if port 8000 is available
   - Ensure Python dependencies are installed
   - Check MySQL connection in .env file

2. **Frontend won't start:**
   - Check if port 5173 is available
   - Ensure Node.js dependencies are installed
   - Check if backend is running

3. **Database connection failed:**
   - Verify MySQL is running
   - Check database credentials in .env
   - Ensure database exists

4. **Scraping errors:**
   - Check internet connection
   - Verify the URL is a Shopify store
   - Some stores may block automated requests

### Error Codes

- **400** - Invalid URL or not a Shopify store
- **500** - Internal server error
- **401** - Website not found (custom error)

## Development

### Adding New Scrapers

1. Create a new scraper class in `backend/app/scrapers/`
2. Inherit from `BaseScraper`
3. Implement required methods
4. Add to `InsightService`

### Customizing the Frontend

1. Modify components in `frontend/src/components/`
2. Update styles in `frontend/src/index.css`
3. Add new API endpoints in `frontend/src/services/api.ts`

### Database Schema Changes

1. Update models in `backend/app/models/database.py`
2. Run database migrations
3. Update Pydantic schemas if needed

## Deployment

### Frontend (Netlify)

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy the `dist/` folder to Netlify

3. Set environment variables:
   - `VITE_API_URL` - Your backend API URL

### Backend

Deploy to platforms like:
- **Heroku** - Easy deployment with Git
- **Railway** - Simple container deployment
- **DigitalOcean** - VPS deployment
- **AWS/GCP** - Cloud deployment

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs in your terminal
3. Check the API documentation at http://localhost:8000/docs
4. Verify all prerequisites are installed correctly

## License

This project is licensed under the MIT License.
