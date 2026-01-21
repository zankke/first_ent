export interface ArtistProfile {
  name: string;
  eng_name?: string;
  birth_date?: string;
  height_cm?: number;
  debut_date?: string;
  debut_title?: string;
  recent_activity_category?: string;
  recent_activity_name?: string;
  genre?: string;
  current_agency_name?: string;
  nationality?: string;
  is_korean?: boolean;
  gender?: 'WOMAN' | 'MEN' | 'NA' | 'EXTRA' | 'FOREIGN';
  status?: 'ACTIVE' | 'INACTIVE' | 'PAUSED' | 'RETIRED' | 'UNKNOWN';
  platform?: string;
  social_media_url?: string;
  profile_photo?: string; // We might get a URL from search
  guarantee_krw?: number;
  wiki_summary?: string;
}

export interface SearchResult {
  profile: ArtistProfile;
  sqlQuery: string;
  pythonScript: string;
  sources: Array<{ title: string; uri: string }>;
}

export interface LoadingState {
  status: 'idle' | 'searching' | 'analyzing' | 'generating' | 'complete' | 'error';
  message: string;
}
