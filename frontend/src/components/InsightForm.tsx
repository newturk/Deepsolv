import React, { useState } from 'react';
import { Search, Globe, AlertCircle } from 'lucide-react';

interface InsightFormProps {
  onSubmit: (websiteUrl: string) => void;
}

const InsightForm: React.FC<InsightFormProps> = ({ onSubmit }) => {
  const [websiteUrl, setWebsiteUrl] = useState('');
  const [isValidating, setIsValidating] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!websiteUrl.trim()) {
      setValidationError('Please enter a website URL');
      return;
    }

    // Basic URL validation
    try {
      new URL(websiteUrl);
    } catch {
      setValidationError('Please enter a valid URL');
      return;
    }

    // Clear any previous validation errors
    setValidationError(null);
    
    // Submit the form
    onSubmit(websiteUrl.trim());
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWebsiteUrl(e.target.value);
    // Clear validation error when user types
    if (validationError) {
      setValidationError(null);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Globe className="w-8 h-8 text-primary-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Enter Shopify Store URL
          </h2>
          <p className="text-gray-600">
            Paste the URL of any Shopify store to extract comprehensive insights
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="website-url" className="block text-sm font-medium text-gray-700 mb-2">
              Website URL
            </label>
            <div className="relative">
              <input
                id="website-url"
                type="url"
                value={websiteUrl}
                onChange={handleUrlChange}
                placeholder="https://example.myshopify.com"
                className={`input-field pr-10 ${validationError ? 'border-red-300 focus:ring-red-500' : ''}`}
                disabled={isValidating}
              />
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <Globe className="h-5 w-5 text-gray-400" />
              </div>
            </div>
            {validationError && (
              <div className="flex items-center mt-2 text-sm text-red-600">
                <AlertCircle className="h-4 w-4 mr-1" />
                {validationError}
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={isValidating || !websiteUrl.trim()}
            className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Search className="w-5 h-5" />
            <span>Fetch Insights</span>
          </button>
        </form>

        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-medium text-gray-900 mb-2">What you'll get:</h3>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• Complete product catalog and hero products</li>
            <li>• Privacy, return, and refund policies</li>
            <li>• Frequently asked questions</li>
            <li>• Social media handles and contact information</li>
            <li>• Brand context and important links</li>
            <li>• Competitor analysis (bonus feature)</li>
          </ul>
        </div>

        <div className="mt-4 text-center">
          <p className="text-xs text-gray-500">
            Example stores: memy.co.in, hairoriginals.com, colourpop.com
          </p>
        </div>
      </div>
    </div>
  );
};

export default InsightForm;
