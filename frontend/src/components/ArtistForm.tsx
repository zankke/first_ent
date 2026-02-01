import { useState, useEffect, ChangeEvent, FormEvent } from 'react';
import { Instagram, Youtube, Link } from 'lucide-react';

interface ArtistData {
  id?: number;
  name: string;
  birth_date: string;
  height_cm: string | number;
  debut_date: string;
  genre: string;
  agency_id: string | number;
  nationality: string;
  is_korean: boolean | number;
  gender: string;
  status: string;
  category_id: string | number;
  platform: string;
  social_media_url: string;
  guarantee_krw: string | number;
  brand_input?: string; // Add brand_input
  profile_photo?: string;
}

interface ArtistFormProps {
  isOpen: boolean;
  onClose: () => void;
  onArtistAdded: () => void;
  artist: ArtistData | null;
}

const ArtistForm = ({ isOpen, onClose, onArtistAdded, artist }: ArtistFormProps) => {
  const [profilePhotos, setProfilePhotos] = useState<File[] | null>(null);
  const [imagePreviews, setImagePreviews] = useState<string[]>([]);
  const [formData, setFormData] = useState<ArtistData>({
    name: '',
    birth_date: '',
    height_cm: '', // number
    debut_date: '',
    genre: '',
    agency_id: '',
    nationality: '',
    is_korean: true,
    gender: 'WOMAN',
    status: '',
    category_id: '',
    platform: '',
    social_media_url: '',
    guarantee_krw: '', // New field
    brand_input: '', // Added field
  });

  useEffect(() => {
    if (artist) {
      setFormData({
        name: artist.name || '',
        birth_date: artist.birth_date ? artist.birth_date.split('T')[0] : '',
        height_cm: artist.height_cm || '',
        debut_date: artist.debut_date ? artist.debut_date.split('T')[0] : '',
        genre: artist.genre || 'DRAMA',
        agency_id: artist.agency_id || '',
        nationality: artist.nationality || '',
        is_korean: artist.is_korean === undefined ? true : Boolean(artist.is_korean), // Handle potential number/boolean mismatch
        gender: artist.gender || 'WOMAN',
        status: artist.status || '',
        category_id: artist.category_id || '',
        platform: artist.platform || '',
        social_media_url: artist.social_media_url || '',
        guarantee_krw: artist.guarantee_krw !== null && artist.guarantee_krw !== undefined ? String(artist.guarantee_krw) : '',
        brand_input: artist.brand_input || '',
      });
      if (artist.profile_photo) {
        setImagePreviews([artist.profile_photo]);
      }
    } else {
      setFormData({
        name: '',
        birth_date: '',
        height_cm: '',
        debut_date: '',
        genre: '',
        agency_id: '',
        nationality: '',
        is_korean: true,
        gender: 'WOMAN',
        status: '',
        category_id: '',
        platform: '',
        social_media_url: '',
        guarantee_krw: '',
        brand_input: '',
      });
      setImagePreviews([]);
    }
    return () => {
      imagePreviews.forEach(preview => URL.revokeObjectURL(preview));
    };
  }, [artist, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { id, name, value, type } = e.target;
    // Handle checkbox separately since it's only on HTMLInputElement
    const checked = (e.target as HTMLInputElement).checked;

    if (name === 'status') {
      setFormData((prev) => ({ ...prev, status: value }));
    } else if (name === 'platform') {
      setFormData((prev) => ({ ...prev, platform: value }));
    } else if (name === 'is_korean') {
      setFormData((prev) => ({
        ...prev,
        is_korean: value === 'true',
        nationality: value === 'true' ? 'KOREAN' : prev.nationality,
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [id]: type === 'checkbox' ? checked : value,
      }));
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      setProfilePhotos(files);

      setImagePreviews(prev => {
        prev.forEach(preview => URL.revokeObjectURL(preview));
        return files.map(file => URL.createObjectURL(file));
      });
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const data = new FormData();
    (Object.keys(formData) as Array<keyof ArtistData>).forEach(key => {
      // Skip undefined or null values
      if (formData[key] === undefined || formData[key] === null) return;

      if (key === 'is_korean') {
        data.append(key, formData[key] ? '1' : '0');
      } else if (key === 'height_cm') {
        data.append(key, formData[key] ? parseInt(String(formData[key]), 10).toString() : '');
      } else if (key === 'guarantee_krw') {
        data.append(key, formData[key] !== '' ? parseInt(String(formData[key]), 10).toString() : '');
      } else {
        data.append(key, String(formData[key]));
      }
    });

    if (profilePhotos) {
      for (let i = 0; i < profilePhotos.length; i++) {
        data.append('profile_photos', profilePhotos[i]);
      }
    }

    const url = artist?.id
      ? `/api/artists/${artist.id}`
      : '/api/artists';
    const method = artist ? 'PUT' : 'POST';

    try {
      const response = await fetch(url, {
        method,
        body: data, // FormData 사용 시 Content-Type 헤더는 브라우저가 자동으로 설정
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Network response was not ok');
      }

      onArtistAdded();
      onClose();
    } catch (error: any) {
      alert(`저장 중 오류 발생: ${error.message}`);
      console.error('Error saving artist:', error);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-900 text-gray-100 rounded-2xl shadow-xl w-full max-w-3xl p-8 max-h-screen overflow-y-auto">
        <h2 className="text-2xl font-bold mb-6">{artist ? '아티스트 수정' : '새 아티스트 추가'}</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
        
           {/* 프로필 사진 (Profile Photo) */}
           <div className="p-6 bg-gray-800 rounded-2xl shadow-inner">
            <h3 className="text-xl font-semibold mb-4">프로필 사진</h3>
            <div>
              <label htmlFor="profile_photos" className="block text-sm font-medium text-gray-300">프로필 사진(multiple)</label>
              <input
                type="file"
                id="profile_photos"
                multiple
                onChange={handleFileChange}
                className="mt-1 block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-2xl file:border-0 file:text-sm file:font-semibold file:bg-orange-500 file:text-white hover:file:bg-orange-600 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent"
              />
              <div className="mt-2 flex flex-wrap gap-2">
                {imagePreviews.map((src, index) => (
                  <img key={index} src={src} alt="Profile Preview" className="w-24 h-24 object-cover rounded-md" />
                ))}
              </div>
            </div>
          </div>       
        
          {/* 기본 정보 (Basic Information) */}
          <div className="p-6 bg-gray-800 rounded-2xl shadow-inner">
            <h3 className="text-xl font-semibold mb-4 text-gray-200">기본 정보</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-300">이름 <span className="text-red-500">*</span></label>
                <input type="text" id="name" value={formData.name} onChange={handleChange} required className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent" />
              </div>
              <div>
                <label htmlFor="birth_date" className="block text-sm font-medium text-gray-300">생년월일 <span className="text-red-500">*</span></label>
                <input type="date" id="birth_date" value={formData.birth_date} onChange={handleChange} required className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent" />
              </div>
              <div>
                <label htmlFor="gender" className="block text-sm font-medium text-gray-300">성별</label>
                <select id="gender" value={formData.gender} onChange={handleChange} className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent">
                  <option value="WOMAN">여성</option>
                  <option value="MEN">남성</option>
                  <option value="EXTRA">기타</option>
                </select>
              </div>
              <div>
                <label htmlFor="nationality" className="block text-sm font-medium text-gray-300">국적</label>
                <input
                  type="text"
                  id="nationality"
                  value={formData.is_korean ? 'KOREAN' : formData.nationality}
                  onChange={handleChange}
                  className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>
              <div className="col-span-1 md:col-span-2">
                <div className="flex items-center space-x-4">
                  <label htmlFor="is_korean_true" className="block text-sm text-gray-300">
                      <input
                        id="is_korean_true"
                        type="radio"
                        name="is_korean"
                        value="true"
                        checked={Boolean(formData.is_korean)}
                        onChange={handleChange}
                        className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300 rounded"
                      />
                      <span className="ml-2">내국인</span>
                    </label>
                    <label htmlFor="is_korean_false" className="block text-sm text-gray-300">
                      <input
                        id="is_korean_false"
                        type="radio"
                        name="is_korean"
                        value="false"
                        checked={!Boolean(formData.is_korean)}
                        onChange={handleChange}
                        className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300 rounded"
                      />
                    <span className="ml-2">외국인</span>
                  </label>
                </div>
              </div>
              <div>
                <label htmlFor="height_cm" className="block text-sm font-medium text-gray-300">키 (cm)</label>
                <input type="number" id="height_cm" value={formData.height_cm} onChange={handleChange} className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent" />
              </div>
              <div>
                <label htmlFor="debut_date" className="block text-sm font-medium text-gray-300">데뷔일</label>
                <input
                  type="date"
                  id="debut_date"
                  value={formData.debut_date || new Date().toISOString().substring(0, 10)}
                  onChange={handleChange}
                  className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>
              <div>
                <label htmlFor="guarantee_krw" className="block text-sm font-medium text-gray-300">모델료(원)</label>
                <input type="number" id="guarantee_krw" value={formData.guarantee_krw} onChange={handleChange} className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent" />
              </div>
              <div>
                <label htmlFor="category_id" className="block text-sm font-medium text-gray-300">카테고리</label>
                <select id="category_id" value={formData.category_id} onChange={handleChange} className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent">
                <option value="">모델 카테고리</option>
                <option value="1">일반모델(성인)</option>
                <option value="2">일반모델(아동)</option>
                <option value="3">일반모델(노인)</option>
                <option value="4">패션모델</option>
                <option value="5">배우</option>
                <option value="6">아동모델</option>
                <option value="7">전문 외국인 모델</option>
                <option value="8">Influencer</option>
                <option value="9">Celebrity</option>
                <option value="10">SINGER</option>
                </select>
              </div>
              <div>
                <label htmlFor="genre" className="block text-sm font-medium text-gray-300">장르</label>
                <select id="genre" value={formData.genre} onChange={handleChange} className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent">
                  <option value="DRAMA">드라마</option>
                  <option value="MOVIE">영화</option>
                  <option value="CF">광고</option>
                  <option value="ETC">기타</option>
                  <option value="PROMOTION">홍보</option>
                  <option value="BROADCAST">방송</option>
                  <option value="YOUTUBE">유투브</option>
                </select>
              </div>

            <div>
              <label className="block text-sm font-medium text-gray-300">BRAND</label>
              <div className="mt-1">
                <input
                  type="text"
                  placeholder="(예:나이키) Activity name/brand name"
                  className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent"
                  value={formData.brand_input}
                  onChange={handleChange}
                  id="brand_input"
                />
              </div>
            </div>

              <div className="col-span-1 md:col-span-2">
                <label className="block text-sm font-medium text-gray-300">상태</label>
                <div className="mt-1 flex space-x-4">
                  <div className="flex items-center">
                    <input
                      id="status_active"
                      type="radio"
                      name="status"
                      value="ACTIVE"
                      checked={formData.status === 'ACTIVE'}
                      onChange={handleChange}
                      className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300"
                    />
                    <label htmlFor="status_active" className="ml-2 block text-sm text-gray-300">활동중</label>
                  </div>
                  <div className="flex items-center">
                    <input
                      id="status_resting"
                      type="radio"
                      name="status"
                      value="RESTING"
                      checked={formData.status === 'RESTING'}
                      onChange={handleChange}
                      className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300"
                    />
                    <label htmlFor="status_resting" className="ml-2 block text-sm text-gray-300">휴식중</label>
                  </div>
                  <div className="flex items-center">
                    <input
                      id="status_other"
                      type="radio"
                      name="status"
                      value="OTHER"
                      checked={formData.status === 'OTHER'}
                      onChange={handleChange}
                      className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300"
                    />
                    <label htmlFor="status_other" className="ml-2 block text-sm text-gray-300">기타</label>
                  </div>
                </div>
              </div>
            </div>
          </div>



          {/* 소셜 미디어 (Social Media) */}
          <div className="p-6 bg-gray-800 rounded-2xl shadow-inner">
            <h3 className="text-xl font-semibold mb-4 text-gray-200">소셜 미디어</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="col-span-1 md:col-span-2">
                <label className="block text-sm font-medium text-gray-300 mb-2 sr-only">PLATFORM</label>
                <div className="flex flex-wrap gap-4">
                  <label htmlFor="platform_instagram" className="flex items-center cursor-pointer">
                    <input
                      id="platform_instagram"
                      type="radio"
                      name="platform"
                      value="Instagram"
                      checked={formData.platform === 'Instagram'}
                      onChange={handleChange}
                      className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300"
                    />
                    <Instagram className="ml-2 h-5 w-5 text-gray-300" />
                    <span className="ml-2 text-sm text-gray-300">Instagram</span>
                  </label>
                  <label htmlFor="platform_youtube" className="flex items-center cursor-pointer">
                    <input
                      id="platform_youtube"
                      type="radio"
                      name="platform"
                      value="YouTube"
                      checked={formData.platform === 'YouTube'}
                      onChange={handleChange}
                      className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300"
                    />
                    <Youtube className="ml-2 h-5 w-5 text-gray-300" />
                    <span className="ml-2 text-sm text-gray-300">YouTube</span>
                  </label>
                  <label htmlFor="platform_tiktok" className="flex items-center cursor-pointer">
                    <input
                      id="platform_tiktok"
                      type="radio"
                      name="platform"
                      value="TikTok"
                      checked={formData.platform === 'TikTok'}
                      onChange={handleChange}
                      className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300"
                    />
                    <Link className="ml-2 h-5 w-5 text-gray-300" />
                    <span className="ml-2 text-sm text-gray-300">TikTok</span>
                  </label>
                  <label htmlFor="platform_other" className="flex items-center cursor-pointer">
                    <input
                      id="platform_other"
                      type="radio"
                      name="platform"
                      value="Other"
                      checked={formData.platform === 'Other'}
                      onChange={handleChange}
                      className="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300"
                    />
                    <span className="ml-2 text-sm text-gray-300">기타</span>
                  </label>
                </div>
              </div>
              <div>
                <label htmlFor="social_media_url" className="block text-sm font-medium text-gray-300">LINK(URL)</label>
                <input type="url" id="social_media_url" value={formData.social_media_url} onChange={handleChange} placeholder="https://..." className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent" />
              </div>
            </div>
          </div>


          {/* 소속사 정보 (Agency Information) */}
          <div className="p-6 bg-gray-800 rounded-2xl shadow-inner">
            <h3 className="text-xl font-semibold mb-4 text-gray-200">소속사 정보</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="agency_id" className="block text-sm font-medium text-gray-300">소속사 ID</label>
                <input type="number" id="agency_id" value={formData.agency_id} onChange={handleChange} className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-2xl shadow-sm p-2 focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 focus:border-transparent" />
              </div>
            </div>
          </div>

          <div className="flex justify-end space-x-4 mt-6">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-600 rounded-md hover:bg-gray-500 text-white">취소</button>
            <button type="submit" className="px-4 py-2 rounded-md text-white" style={{ backgroundColor: 'rgb(237 113 4)' }}>{artist ? '수정' : '추가'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ArtistForm
