export interface Product {
  id?: number;
  title: string;
  description?: string;
  price?: string;
  currency?: string;
  image_url?: string;
  product_url?: string;
  available?: boolean;
  tags?: string[];
  category?: string;
}

export interface Policy {
  privacy_policy?: string;
  return_policy?: string;
  refund_policy?: string;
  shipping_policy?: string;
  terms_of_service?: string;
}

export interface FAQ {
  question: string;
  answer: string;
  category?: string;
}

export interface SocialHandle {
  platform: string;
  handle: string;
  url?: string;
}

export interface ContactInfo {
  emails: string[];
  phone_numbers: string[];
  addresses: string[];
  contact_form_url?: string;
}

export interface ImportantLink {
  title: string;
  url: string;
  description?: string;
}

export interface Competitor {
  name: string;
  website_url: string;
  description?: string;
  insights?: StoreInsights;
}

export interface StoreInsights {
  brand_name: string;
  website_url: string;
  products: Product[];
  hero_products: Product[];
  policies: Policy;
  faqs: FAQ[];
  social_handles: SocialHandle[];
  contact_info: ContactInfo;
  brand_context?: string;
  important_links: ImportantLink[];
  competitors: Competitor[];
  scraped_at: string;
  total_products: number;
  store_theme?: string;
  currency?: string;
  language?: string;
}

export interface InsightResponse {
  success: boolean;
  data?: StoreInsights;
  error?: string;
  message?: string;
  processing_time?: number;
}

export interface InsightRequest {
  website_url: string;
}
