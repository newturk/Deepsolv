import React, { useState } from 'react';
import { StoreInsights } from '../types';
import { Brain, Sparkles, TrendingUp, Target, Users, ShoppingBag } from 'lucide-react';

interface LLMAnalysisProps {
  insights: StoreInsights;
}

interface AnalysisSection {
  title: string;
  icon: React.ReactNode;
  content: string;
  color: string;
}

const LLMAnalysis: React.FC<LLMAnalysisProps> = ({ insights }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<AnalysisSection[]>([]);

  const analyzeWithGemini = async () => {
    setIsAnalyzing(true);
    
    try {
      // Prepare data for analysis
      const analysisData = {
        brandName: insights.brand_name,
        totalProducts: insights.products?.length || 0,
        heroProducts: insights.hero_products?.length || 0,
        socialHandles: insights.social_handles?.length || 0,
        contactInfo: insights.contact_info,
        policies: insights.policies,
        faqs: insights.faqs?.length || 0,
        importantLinks: insights.important_links?.length || 0,
        brandContext: insights.brand_context
      };

      // Call Gemini API
      const apiKey = (import.meta as any).env?.VITE_GEMINI_API_KEY || 'AIzaSyCToQEGVaCvjy1W5jg5l8oFjz8Wubstq1A';
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: `Analyze this Shopify store data and provide comprehensive insights in the following format:
              
Store Analysis for ${analysisData.brandName}:

1. **Brand Overview** (brand positioning, unique value proposition, target audience demographics, age categories, brand personality)
2. **Market Analysis** (market scope, industry trends, market size estimation, competitive landscape, target market segments)
3. **Product Strategy** (product assortment analysis, pricing strategy, product differentiation, inventory insights, seasonal trends)
4. **Customer Experience** (policies evaluation, FAQ coverage, contact methods, customer service approach)
5. **Digital Presence** (social media strategy, online visibility, engagement metrics, digital marketing approach)
6. **Trends & Popularity** (recent hot topics, trending products, social media buzz, viral opportunities, emerging trends)
7. **Business Intelligence** (revenue potential, market opportunities, growth areas, operational insights, strategic recommendations)

Data: ${JSON.stringify(analysisData, null, 2)}

Provide detailed, actionable insights focusing on market scope, preferred age categories, popularity factors, recent trends, and business intelligence that would be valuable for comprehensive business analysis.`
            }]
          }]
        })
      });

      if (!response.ok) {
        throw new Error('Failed to analyze with Gemini');
      }

      const data = await response.json();
      const analysisText = data.candidates[0].content.parts[0].text;

      // Parse the analysis into sections
      const sections = parseAnalysis(analysisText);
      setAnalysis(sections);

    } catch (error) {
      console.error('Error analyzing with Gemini:', error);
      // Fallback to basic analysis
      setAnalysis(generateBasicAnalysis());
    } finally {
      setIsAnalyzing(false);
    }
  };

  const parseAnalysis = (text: string): AnalysisSection[] => {
    const sections: AnalysisSection[] = [];
    const sectionData = [
      { title: 'Brand Overview', icon: <Target className="w-5 h-5" />, color: 'bg-blue-50 border-blue-200' },
      { title: 'Market Analysis', icon: <Brain className="w-5 h-5" />, color: 'bg-indigo-50 border-indigo-200' },
      { title: 'Product Strategy', icon: <ShoppingBag className="w-5 h-5" />, color: 'bg-green-50 border-green-200' },
      { title: 'Customer Experience', icon: <Users className="w-5 h-5" />, color: 'bg-purple-50 border-purple-200' },
      { title: 'Digital Presence', icon: <TrendingUp className="w-5 h-5" />, color: 'bg-orange-50 border-orange-200' },
      { title: 'Trends & Popularity', icon: <Sparkles className="w-5 h-5" />, color: 'bg-pink-50 border-pink-200' },
      { title: 'Business Intelligence', icon: <Target className="w-5 h-5" />, color: 'bg-yellow-50 border-yellow-200' }
    ];

    // Simple parsing - in a real app you'd want more sophisticated parsing
    const lines = text.split('\n');
    let currentSection = '';
    let currentContent = '';

    for (const line of lines) {
      if (line.includes('**') && line.includes('**')) {
        if (currentSection && currentContent) {
          const section = sectionData.find(s => s.title === currentSection);
          if (section) {
            sections.push({
              ...section,
              content: currentContent.trim()
            });
          }
        }
        currentSection = line.replace(/\*\*/g, '').trim();
        currentContent = '';
      } else if (line.trim() && currentSection) {
        currentContent += line.trim() + ' ';
      }
    }

    // Add the last section
    if (currentSection && currentContent) {
      const section = sectionData.find(s => s.title === currentSection);
      if (section) {
        sections.push({
          ...section,
          content: currentContent.trim()
        });
      }
    }

    return sections.length > 0 ? sections : generateBasicAnalysis();
  };

  const generateBasicAnalysis = (): AnalysisSection[] => {
    return [
      {
        title: 'Brand Overview',
        icon: <Target className="w-5 h-5" />,
        content: `${insights.brand_name} appears to be a Shopify store with ${insights.products?.length || 0} products. The brand focuses on providing quality products to their customers with a target audience spanning multiple age groups.`,
        color: 'bg-blue-50 border-blue-200'
      },
      {
        title: 'Market Analysis',
        icon: <Brain className="w-5 h-5" />,
        content: `The store operates in a competitive e-commerce landscape with significant market scope. The ${insights.total_products || 0} products suggest a substantial market presence and potential for growth.`,
        color: 'bg-indigo-50 border-indigo-200'
      },
      {
        title: 'Product Strategy',
        icon: <ShoppingBag className="w-5 h-5" />,
        content: `The store offers ${insights.hero_products?.length || 0} featured products, suggesting a curated approach to product selection with strategic pricing and positioning.`,
        color: 'bg-green-50 border-green-200'
      },
      {
        title: 'Customer Experience',
        icon: <Users className="w-5 h-5" />,
        content: `Customer service is supported through ${insights.contact_info?.emails?.length || 0} contact methods and ${insights.faqs?.length || 0} FAQ items, indicating a focus on customer satisfaction.`,
        color: 'bg-purple-50 border-purple-200'
      },
      {
        title: 'Digital Presence',
        icon: <TrendingUp className="w-5 h-5" />,
        content: `The brand maintains ${insights.social_handles?.length || 0} social media channels for digital engagement and marketing, showing strong online presence.`,
        color: 'bg-orange-50 border-orange-200'
      },
      {
        title: 'Trends & Popularity',
        icon: <Sparkles className="w-5 h-5" />,
        content: `The store's product variety and social media presence suggest they're keeping up with current trends and maintaining relevance in their market.`,
        color: 'bg-pink-50 border-pink-200'
      },
      {
        title: 'Business Intelligence',
        icon: <Target className="w-5 h-5" />,
        content: `With ${insights.total_products || 0} total products and comprehensive customer support, this store shows strong business fundamentals and potential for expansion.`,
        color: 'bg-yellow-50 border-yellow-200'
      }
    ];
  };

  return (
    <div className="space-y-6">
      {/* Coming Soon Banner */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-blue-600" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-blue-900">Advanced LLM Analysis Coming Soon! 🚀</h3>
            <p className="text-sm text-blue-700 mt-1">
              We're working on enhanced AI-powered insights with deeper market analysis, trend predictions, and competitive intelligence.
            </p>
          </div>
          <div className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
            BETA
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Brain className="w-6 h-6 text-indigo-600" />
          AI-Powered Analysis
        </h2>
        <button
          onClick={analyzeWithGemini}
          disabled={isAnalyzing}
          className="btn-primary flex items-center gap-2"
        >
          {isAnalyzing ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Analyzing...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              Analyze with Gemini
            </>
          )}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {analysis.map((section, index) => (
          <div
            key={index}
            className={`p-6 rounded-lg border ${section.color} hover:shadow-md transition-shadow`}
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-lg bg-white shadow-sm">
                {section.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-800">
                {section.title}
              </h3>
            </div>
            <p className="text-gray-700 leading-relaxed">
              {section.content}
            </p>
          </div>
        ))}
      </div>

      {analysis.length === 0 && !isAnalyzing && (
        <div className="text-center py-12">
          <Brain className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Ready for AI Analysis
          </h3>
          <p className="text-gray-500 mb-4">
            Click "Analyze with Gemini" to get AI-powered insights about this store.
          </p>
        </div>
      )}
    </div>
  );
};

export default LLMAnalysis;
