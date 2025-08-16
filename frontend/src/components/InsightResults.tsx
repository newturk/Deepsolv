import React, { useState } from 'react';
import { StoreInsights } from '../types';
import { RotateCcw, ExternalLink, Mail, Phone, MapPin, Globe, ChevronDown } from 'lucide-react';
import LLMAnalysis from './LLMAnalysis';

interface InsightResultsProps {
  insights: StoreInsights;
  onReset: () => void;
}

const InsightResults: React.FC<InsightResultsProps> = ({ insights, onReset }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [productsToShow, setProductsToShow] = useState(24);

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'products', label: 'Products', icon: '🛍️' },
    { id: 'policies', label: 'Policies', icon: '📋' },
    { id: 'faqs', label: 'FAQs', icon: '❓' },
    { id: 'social', label: 'Social & Contact', icon: '📱' },
    { id: 'links', label: 'Important Links', icon: '🔗' },
    { id: 'competitors', label: 'Competitors', icon: '🏆' },
    { id: 'llm-analysis', label: 'AI Analysis', icon: '🤖' },
  ];

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const loadMoreProducts = () => {
    setProductsToShow(prev => Math.min(prev + 24, insights.products.length));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{insights.brand_name}</h1>
          <p className="text-gray-600 mt-1">{insights.website_url}</p>
          <p className="text-sm text-gray-500 mt-1">
            Analyzed on {formatDate(insights.scraped_at)}
          </p>
        </div>
        <button onClick={onReset} className="btn-secondary flex items-center space-x-2">
          <RotateCcw className="w-4 h-4" />
          <span>Analyze Another Store</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <div className="text-2xl font-bold text-primary-600">{insights.total_products}</div>
          <div className="text-sm text-gray-600">Total Products</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-600">{insights.hero_products.length}</div>
          <div className="text-sm text-gray-600">Hero Products</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-blue-600">{insights.faqs.length}</div>
          <div className="text-sm text-gray-600">FAQs</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-purple-600">{insights.social_handles.length}</div>
          <div className="text-sm text-gray-600">Social Handles</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="min-h-96">
                 {activeTab === 'overview' && (
           <div className="space-y-6">
             {insights.brand_context && (
               <div className="card">
                 <h3 className="text-lg font-semibold text-gray-900 mb-3">About {insights.brand_name}</h3>
                 <p className="text-gray-700 leading-relaxed">{insights.brand_context}</p>
               </div>
             )}

             {/* Hero Products Section */}
             {insights.hero_products.length > 0 && (
               <div className="card">
                 <h3 className="text-lg font-semibold text-gray-900 mb-4">Featured Products ({insights.hero_products.length})</h3>
                 <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                   {insights.hero_products.map((product, index) => (
                     <ProductCard key={index} product={product} />
                   ))}
                 </div>
               </div>
             )}

             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
               <div className="card">
                 <h3 className="text-lg font-semibold text-gray-900 mb-3">Store Information</h3>
                 <div className="space-y-2 text-sm">
                   {insights.store_theme && (
                     <div className="flex justify-between">
                       <span className="text-gray-600">Theme:</span>
                       <span className="font-medium">{insights.store_theme}</span>
                     </div>
                   )}
                   {insights.currency && (
                     <div className="flex justify-between">
                       <span className="text-gray-600">Currency:</span>
                       <span className="font-medium">{insights.currency}</span>
                     </div>
                   )}
                   {insights.language && (
                     <div className="flex justify-between">
                       <span className="text-gray-600">Language:</span>
                       <span className="font-medium">{insights.language}</span>
                     </div>
                   )}
                 </div>
               </div>

               <div className="card">
                 <h3 className="text-lg font-semibold text-gray-900 mb-3">Quick Stats</h3>
                 <div className="space-y-2 text-sm">
                   <div className="flex justify-between">
                     <span className="text-gray-600">Products:</span>
                     <span className="font-medium">{insights.total_products}</span>
                   </div>
                   <div className="flex justify-between">
                     <span className="text-gray-600">FAQs:</span>
                     <span className="font-medium">{insights.faqs.length}</span>
                   </div>
                   <div className="flex justify-between">
                     <span className="text-gray-600">Social Handles:</span>
                     <span className="font-medium">{insights.social_handles.length}</span>
                   </div>
                   <div className="flex justify-between">
                     <span className="text-gray-600">Important Links:</span>
                     <span className="font-medium">{insights.important_links.length}</span>
                   </div>
                 </div>
               </div>
             </div>
           </div>
         )}

        {activeTab === 'products' && (
          <div className="space-y-6">
            {insights.hero_products.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Featured Products ({insights.hero_products.length})</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {insights.hero_products.map((product, index) => (
                    <ProductCard key={index} product={product} />
                  ))}
                </div>
              </div>
            )}

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">All Products ({insights.total_products})</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {insights.products.slice(0, productsToShow).map((product, index) => (
                  <ProductCard key={index} product={product} />
                ))}
              </div>
              {insights.products.length > productsToShow && (
                <div className="text-center mt-6">
                  <button
                    onClick={loadMoreProducts}
                    className="btn-secondary flex items-center gap-2 mx-auto"
                  >
                    <ChevronDown className="w-4 h-4" />
                    Load More Products
                  </button>
                  <p className="text-sm text-gray-500 mt-2">
                    Showing {productsToShow} of {insights.products.length} products
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'policies' && (
          <div className="space-y-6">
            {Object.entries(insights.policies).map(([key, value]) => {
              if (!value) return null;
              return (
                <div key={key} className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3 capitalize">
                    {key.replace('_', ' ')}
                  </h3>
                  <div className="prose max-w-none">
                    <p className="text-gray-700 leading-relaxed">{value}</p>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {activeTab === 'faqs' && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Frequently Asked Questions</h3>
            {insights.faqs.length > 0 ? (
              <div className="space-y-4">
                {insights.faqs.map((faq, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">{faq.question}</h4>
                    <p className="text-gray-700">{faq.answer}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No FAQs found</p>
            )}
          </div>
        )}

        {activeTab === 'social' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Social Media Handles</h3>
              {insights.social_handles.length > 0 ? (
                <div className="space-y-3">
                  {insights.social_handles.map((handle, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <span className="font-medium text-gray-900">{handle.platform}</span>
                        <p className="text-sm text-gray-600">@{handle.handle}</p>
                      </div>
                      {handle.url && (
                        <a
                          href={handle.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary-600 hover:text-primary-700"
                        >
                          <ExternalLink className="w-4 h-4" />
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No social media handles found</p>
              )}
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
              <div className="space-y-4">
                {insights.contact_info.emails.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                      <Mail className="w-4 h-4 mr-2" />
                      Email Addresses
                    </h4>
                    <div className="space-y-1">
                      {insights.contact_info.emails.map((email, index) => (
                        <a
                          key={index}
                          href={`mailto:${email}`}
                          className="block text-primary-600 hover:text-primary-700 text-sm"
                        >
                          {email}
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {insights.contact_info.phone_numbers.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                      <Phone className="w-4 h-4 mr-2" />
                      Phone Numbers
                    </h4>
                    <div className="space-y-1">
                      {insights.contact_info.phone_numbers.map((phone, index) => (
                        <a
                          key={index}
                          href={`tel:${phone}`}
                          className="block text-primary-600 hover:text-primary-700 text-sm"
                        >
                          {phone}
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {insights.contact_info.addresses.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                      <MapPin className="w-4 h-4 mr-2" />
                      Addresses
                    </h4>
                    <div className="space-y-1">
                      {insights.contact_info.addresses.map((address, index) => (
                        <p key={index} className="text-sm text-gray-700">{address}</p>
                      ))}
                    </div>
                  </div>
                )}

                {insights.contact_info.contact_form_url && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                      <Globe className="w-4 h-4 mr-2" />
                      Contact Form
                    </h4>
                    <a
                      href={insights.contact_info.contact_form_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:text-primary-700 text-sm"
                    >
                      {insights.contact_info.contact_form_url}
                    </a>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'links' && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Important Links</h3>
            {insights.important_links.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {insights.important_links.map((link, index) => (
                  <a
                    key={index}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-gray-900">{link.title}</h4>
                        {link.description && (
                          <p className="text-sm text-gray-600">{link.description}</p>
                        )}
                      </div>
                      <ExternalLink className="w-4 h-4 text-gray-400" />
                    </div>
                  </a>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No important links found</p>
            )}
          </div>
        )}

        {activeTab === 'competitors' && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Competitor Analysis</h3>
            {insights.competitors.length > 0 ? (
              <div className="space-y-4">
                {insights.competitors.map((competitor, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-gray-900">{competitor.name}</h4>
                        <a
                          href={competitor.website_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary-600 hover:text-primary-700 text-sm"
                        >
                          {competitor.website_url}
                        </a>
                        {competitor.description && (
                          <p className="text-gray-700 mt-2">{competitor.description}</p>
                        )}
                      </div>
                      <ExternalLink className="w-4 h-4 text-gray-400" />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No competitors found</p>
            )}
          </div>
        )}

        {activeTab === 'llm-analysis' && (
          <LLMAnalysis insights={insights} />
        )}
      </div>
    </div>
  );
};

// Product Card Component
const ProductCard: React.FC<{ product: any }> = ({ product }) => {
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      {product.image_url && (
        <div className="aspect-square bg-gray-100 rounded-lg mb-3 overflow-hidden">
          <img
            src={product.image_url}
            alt={product.title}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.currentTarget.style.display = 'none';
            }}
          />
        </div>
      )}
      <h4 className="font-medium text-gray-900 mb-2 line-clamp-2">{product.title}</h4>
      {product.price && (
        <p className="text-lg font-semibold text-primary-600 mb-2">
          {product.price} {product.currency}
        </p>
      )}
      {product.description && (
        <p className="text-sm text-gray-600 line-clamp-3">{product.description}</p>
      )}
      {product.product_url && (
        <a
          href={product.product_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-primary-600 hover:text-primary-700 text-sm mt-2"
        >
          View Product
          <ExternalLink className="w-3 h-3 ml-1" />
        </a>
      )}
    </div>
  );
};

export default InsightResults;
