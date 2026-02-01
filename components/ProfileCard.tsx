import React, { useState } from 'react';
import { ArtistProfile } from '../types';

interface ProfileCardProps {
  profile: ArtistProfile;
}

const ProfileCard: React.FC<ProfileCardProps> = ({ profile }) => {
  const [imgError, setImgError] = useState(false);

  // Define fields with optional tooltip
  const fields = [
    { label: 'Birth Date', value: profile.birth_date },
    { 
      label: 'Debut', 
      value: profile.debut_date || 'Unknown', 
      tooltip: profile.debut_title ? `Title: ${profile.debut_title}` : undefined
    },
    { label: 'Agency', value: profile.current_agency_name },
    { label: 'Height', value: profile.height_cm ? `${profile.height_cm} cm` : 'N/A' },
    { label: 'Gender', value: profile.gender },
    { label: 'Status', value: profile.status ?? 'ACTIVE'},
    { label: 'Recent Drama/Movie', value: profile.recent_activity_name },
    { label: 'Recent Activity Category', value: profile.recent_activity_category },
  ];

  return (
    // Removed overflow-hidden to allow tooltips to popup outside the card boundaries
    <div className="bg-gray-800 rounded-xl shadow-lg border border-gray-700 h-full flex flex-col">
      {/* Added rounded-t-xl to match parent corners since overflow is visible */}
      <div className="bg-gradient-to-r from-gray-700 to-gray-800 p-6 border-b border-gray-600 rounded-t-xl">
        <div className="flex items-center gap-6">
          <div className="flex-shrink-0">
             {profile.profile_photo && !imgError ? (
                <img 
                  src={profile.profile_photo} 
                  alt={profile.name} 
                  className="w-24 h-24 rounded-full object-cover border-4 border-gray-600 shadow-md bg-gray-700"
                  onError={() => setImgError(true)}
                />
             ) : (
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center border-4 border-gray-500 text-gray-300 font-bold text-3xl shadow-md">
                   {profile.name.charAt(0)}
                </div>
             )}
          </div>

          <div className="flex-1 min-w-0">
             <div className="flex justify-between items-start">
               <div>
                  <h3 className="text-2xl font-bold text-white flex items-center gap-2 truncate">
                    {profile.name}
                    {profile.is_korean && <span className="text-xs bg-blue-900 text-blue-200 px-2 py-0.5 rounded-full border border-blue-800">KR</span>}
                  </h3>
                  {profile.eng_name && (
                    <p className="text-blue-300/80 text-sm font-medium mt-1">{profile.eng_name}</p>
                  )}
               </div>
               {profile.genre && (
                 <span className="flex-shrink-0 text-xs text-gray-300 uppercase tracking-wider bg-gray-900/40 px-3 py-1 rounded-full border border-gray-600">
                   {profile.genre}
                 </span>
               )}
             </div>
          </div>
        </div>
      </div>
      
      <div className="p-6 flex-1">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-6 mb-6">
           {fields.map((field, idx) => (
             field.value ? (
               <div key={idx} className="flex flex-col group/field">
                 <span className="text-xs text-gray-500 font-bold uppercase tracking-wide mb-1 group-hover/field:text-blue-400 transition-colors">
                    {field.label}
                 </span>
                 
                 {field.tooltip ? (
                   <div className="relative group/tooltip w-fit">
                     <span className="text-gray-200 font-medium text-sm break-words border-l-2 border-gray-700 pl-3 py-0.5 cursor-help border-b border-dotted border-gray-500 hover:border-blue-400">
                       {field.value}
                     </span>
                     {/* Tooltip Content */}
                     <div className="absolute bottom-full left-0 mb-2 w-max max-w-[200px] px-3 py-2 bg-gray-950 text-xs text-blue-100 rounded-md shadow-xl border border-gray-700 opacity-0 group-hover/tooltip:opacity-100 transition-opacity z-50 pointer-events-none transform translate-y-1 group-hover/tooltip:translate-y-0 duration-200">
                        {field.tooltip}
                        <div className="absolute top-full left-4 -mt-1 border-4 border-transparent border-t-gray-700" />
                     </div>
                   </div>
                 ) : (
                   <span className="text-gray-200 font-medium text-sm break-words border-l-2 border-gray-700 pl-3 py-0.5">
                     {field.value}
                   </span>
                 )}
               </div>
             ) : null
           ))}
        </div>

        {profile.wiki_summary && (
          <div className="mt-6 pt-5 border-t border-gray-700">
             <span className="text-xs text-gray-400 font-bold uppercase mb-3 block flex items-center gap-2">
               <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
               Biography Summary
             </span>
             <p className="text-sm text-gray-300 leading-relaxed max-h-48 overflow-y-auto pr-2 custom-scrollbar bg-gray-900/50 p-4 rounded-lg border border-gray-700/50 shadow-inner">
               {profile.wiki_summary}
             </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfileCard;