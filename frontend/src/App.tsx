import React, { useState, useEffect } from 'react';
import { StoreInsights } from './types';
import { insightsApi } from './services/api';
import InsightForm from './components/InsightForm';
import InsightResults from './components/InsightResults';
import Header from './components/Header';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [insights, setInsights] = useState<StoreInsights | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState<boolean | null>(null);

  useEffect(() => {
    // Check backend connection on app load
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      await insightsApi.healthCheck();
      setIsConnected(true);
    } catch (error) {
      setIsConnected(false);
      console.error('Backend connection failed:', error);
    }
  };

  const [analyzingUrl, setAnalyzingUrl] = useState<string>('');

  const handleFetchInsights = async (websiteUrl: string) => {
    setLoading(true);
    setError(null);
    setInsights(null);
    setAnalyzingUrl(websiteUrl);

    try {
      const response = await insightsApi.getInsights({ website_url: websiteUrl });
      
      if (response.success && response.data) {
        setInsights(response.data);
      } else {
        setError(response.error || 'Failed to fetch insights');
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
      setAnalyzingUrl('');
    }
  };

  const handleReset = () => {
    setInsights(null);
    setError(null);
  };

  if (isConnected === false) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Backend Connection Failed</h1>
          <p className="text-gray-600 mb-4">
            Unable to connect to the backend server. Please ensure the backend is running on port 8000.
          </p>
          <button 
            onClick={checkBackendConnection}
            className="btn-primary"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {!insights && !loading && (
          <div className="text-center mb-12">
            {/* Hero Section */}
            <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 text-white p-12 mb-12">
              <div className="absolute inset-0 bg-black opacity-10"></div>
              <div className="relative z-10">
                <div className="text-6xl mb-6">🚀</div>
                <h1 className="text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-primary-100">
                  Shopify Store Insights Fetcher
                </h1>
                <p className="text-xl text-primary-100 max-w-3xl mx-auto mb-8 leading-relaxed">
                  Extract comprehensive insights from any Shopify store without using the official API. 
                  Get product catalogs, policies, FAQs, social media handles, and more.
                </p>
                <div className="flex flex-wrap justify-center gap-4 text-sm">
                  <span className="bg-white/20 px-3 py-1 rounded-full">🛍️ Product Catalog</span>
                  <span className="bg-white/20 px-3 py-1 rounded-full">📋 Policies & FAQs</span>
                  <span className="bg-white/20 px-3 py-1 rounded-full">📱 Social Media</span>
                  <span className="bg-white/20 px-3 py-1 rounded-full">🤖 AI Analysis</span>
                </div>
              </div>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              <div className="card hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-l-4 border-l-primary-500">
                <div className="text-3xl mb-3">🔍</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Deep Analysis</h3>
                <p className="text-gray-600">Extract comprehensive data from any Shopify store including products, policies, and social media presence.</p>
              </div>
              
              <div className="card hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-l-4 border-l-green-500">
                <div className="text-3xl mb-3">⚡</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Fast & Efficient</h3>
                <p className="text-gray-600">Advanced web scraping techniques ensure quick and reliable data extraction without API limitations.</p>
              </div>
              
              <div className="card hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-l-4 border-l-blue-500">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Rich Insights</h3>
                <p className="text-gray-600">Get detailed analytics, competitor analysis, and AI-powered insights to understand market positioning.</p>
              </div>
              
              <div className="card hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-l-4 border-l-purple-500">
                <div className="text-3xl mb-3">🎯</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Market Research</h3>
                <p className="text-gray-600">Identify trends, analyze competitors, and discover opportunities in the e-commerce landscape.</p>
              </div>
              
              <div className="card hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-l-4 border-l-orange-500">
                <div className="text-3xl mb-3">🔒</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No API Required</h3>
                <p className="text-gray-600">Access Shopify store data without needing official API keys or authentication requirements.</p>
              </div>
              
              <div className="card hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-l-4 border-l-red-500">
                <div className="text-3xl mb-3">📈</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Business Intelligence</h3>
                <p className="text-gray-600">Transform raw data into actionable insights for business strategy and competitive advantage.</p>
              </div>
            </div>

            {/* How It Works */}
            <div className="bg-white rounded-2xl p-8 shadow-lg mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">How It Works</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl font-bold text-primary-600">1</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Enter Store URL</h3>
                  <p className="text-gray-600">Simply paste the Shopify store URL you want to analyze</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl font-bold text-primary-600">2</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Analysis</h3>
                  <p className="text-gray-600">Our advanced scrapers extract comprehensive data from the store</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl font-bold text-primary-600">3</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Get Insights</h3>
                  <p className="text-gray-600">Receive detailed reports and analysis in an organized format</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {!insights && !loading && (
          <InsightForm onSubmit={handleFetchInsights} />
        )}

        {loading && (
          <div className="text-center py-12">
            <div className="max-w-4xl mx-auto">
              <div className="mb-8">
                <LoadingSpinner />
                <h2 className="text-2xl font-bold text-gray-900 mt-4 mb-2">
                  Analyzing Shopify Store
                </h2>
                <p className="text-gray-600">
                  This may take a few minutes while we extract comprehensive insights...
                </p>
              </div>
              
              {/* Website Preview with Loading Overlay */}
              <div className="relative bg-white rounded-lg shadow-lg overflow-hidden border">
                <div className="bg-gray-100 px-4 py-3 border-b">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <div className="ml-3 text-sm text-gray-600 font-mono">
                      {analyzingUrl || 'Loading...'}
                    </div>
                  </div>
                </div>
                
                <div className="relative">
                  {/* Website Preview */}
                  <div className="w-full h-96 bg-gradient-to-br from-gray-50 to-gray-100 relative overflow-hidden">
                    {/* Header Bar */}
                    <div className="absolute top-0 left-0 right-0 h-12 bg-white border-b flex items-center px-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                        <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      </div>
                      <div className="ml-4 text-sm text-gray-600 font-mono">
                        {analyzingUrl || 'Loading...'}
                      </div>
                    </div>
                    
                    {/* Navigation */}
                    <div className="absolute top-12 left-0 right-0 h-10 bg-gray-100 border-b flex items-center px-4 space-x-6">
                      <div className="w-16 h-4 bg-gray-300 rounded animate-pulse"></div>
                      <div className="w-20 h-4 bg-gray-300 rounded animate-pulse"></div>
                      <div className="w-16 h-4 bg-gray-300 rounded animate-pulse"></div>
                      <div className="w-24 h-4 bg-gray-300 rounded animate-pulse"></div>
                    </div>
                    
                    {/* Main Content */}
                    <div className="absolute top-24 left-0 right-0 bottom-0 p-6">
                      {/* Hero Section */}
                      <div className="mb-6">
                        <div className="w-3/4 h-8 bg-gray-300 rounded mb-3 animate-pulse"></div>
                        <div className="w-1/2 h-6 bg-gray-300 rounded mb-4 animate-pulse"></div>
                        <div className="w-2/3 h-4 bg-gray-300 rounded animate-pulse"></div>
                      </div>
                      
                      {/* Product Grid */}
                      <div className="grid grid-cols-3 gap-4">
                        {[1, 2, 3, 4, 5, 6].map((i) => (
                          <div key={i} className="bg-white rounded-lg p-3 border">
                            <div className="w-full h-20 bg-gray-200 rounded mb-2 animate-pulse"></div>
                            <div className="w-3/4 h-3 bg-gray-200 rounded mb-1 animate-pulse"></div>
                            <div className="w-1/2 h-3 bg-gray-200 rounded animate-pulse"></div>
                          </div>
                        ))}
                      </div>
                      
                      {/* Footer */}
                      <div className="absolute bottom-4 left-6 right-6">
                        <div className="flex space-x-4">
                          <div className="w-16 h-3 bg-gray-200 rounded animate-pulse"></div>
                          <div className="w-20 h-3 bg-gray-200 rounded animate-pulse"></div>
                          <div className="w-16 h-3 bg-gray-200 rounded animate-pulse"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Loading Overlay */}
                  <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
                    <div className="relative">
                      {/* Main Scanning Circle */}
                      <div className="w-32 h-32 border-4 border-primary-500 border-t-transparent rounded-full scan-circle"></div>
                      
                      {/* Inner Scanning Circle */}
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="w-24 h-24 border-2 border-primary-300 border-dashed rounded-full scan-circle" style={{animationDelay: '0.5s'}}></div>
                      </div>
                      
                      {/* Center Scanning Dot */}
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="w-4 h-4 bg-primary-500 rounded-full pulse-dot"></div>
                      </div>
                      
                      {/* Scanning Lines */}
                      <div className="absolute inset-0 w-full h-full">
                        <div className="scan-line w-full h-1 absolute top-1/4"></div>
                        <div className="scan-line w-full h-1 absolute top-1/2" style={{animationDelay: '0.5s'}}></div>
                        <div className="scan-line w-full h-1 absolute top-3/4" style={{animationDelay: '1s'}}></div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Scanning Status */}
                  <div className="absolute bottom-4 left-4 right-4">
                    <div className="bg-white bg-opacity-90 backdrop-blur-sm rounded-lg p-3 shadow-lg">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-700 font-medium">Scanning in progress...</span>
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                          <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        </div>
                      </div>
                      
                      {/* Data Extraction Progress */}
                      <div className="mt-2 space-y-1">
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-600">Products</span>
                          <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                            <div className="h-full bg-primary-500 rounded-full animate-pulse" style={{width: '75%'}}></div>
                          </div>
                        </div>
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-600">Policies</span>
                          <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                            <div className="h-full bg-green-500 rounded-full animate-pulse" style={{width: '60%'}}></div>
                          </div>
                        </div>
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-600">Competitors</span>
                          <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                            <div className="h-full bg-blue-500 rounded-full animate-pulse" style={{width: '45%'}}></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Progress Steps */}
              <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <div className="w-6 h-6 bg-primary-500 rounded-full animate-pulse"></div>
                  </div>
                  <p className="text-sm text-gray-600">Extracting Products</p>
                  <div className="text-xs text-gray-500 mt-1">🔄 Scanning catalog</div>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <div className="w-6 h-6 bg-green-500 rounded-full animate-pulse"></div>
                  </div>
                  <p className="text-sm text-gray-600">Analyzing Policies</p>
                  <div className="text-xs text-gray-500 mt-1">📋 Reading terms</div>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <div className="w-6 h-6 bg-blue-500 rounded-full animate-pulse"></div>
                  </div>
                  <p className="text-sm text-gray-600">Finding Competitors</p>
                  <div className="text-xs text-gray-500 mt-1">🔍 Market research</div>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <div className="w-6 h-6 bg-purple-500 rounded-full animate-pulse"></div>
                  </div>
                  <p className="text-sm text-gray-600">AI Analysis</p>
                  <div className="text-xs text-gray-500 mt-1">🤖 Gemini insights</div>
                </div>
              </div>
              
              {/* Scanning Sound Effect Indicator */}
              <div className="mt-6 text-center">
                <div className="inline-flex items-center space-x-2 bg-gray-100 rounded-full px-4 py-2">
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-gray-600 font-mono">SCANNING...</span>
                  <div className="flex space-x-1">
                    <div className="w-1 h-3 bg-primary-400 rounded-full animate-pulse"></div>
                    <div className="w-1 h-5 bg-primary-500 rounded-full animate-pulse" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-1 h-4 bg-primary-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                    <div className="w-1 h-6 bg-primary-500 rounded-full animate-pulse" style={{animationDelay: '0.3s'}}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="card mb-6 border-red-200 bg-red-50">
            <div className="flex items-center">
              <div className="text-red-500 text-xl mr-3">⚠️</div>
              <div>
                <h3 className="text-red-800 font-medium">Error</h3>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
            <button 
              onClick={handleReset}
              className="btn-secondary ml-auto"
            >
              Try Again
            </button>
          </div>
        )}

        {insights && (
          <InsightResults 
            insights={insights} 
            onReset={handleReset}
          />
        )}
      </main>
    </div>
  );
}

export default App;
