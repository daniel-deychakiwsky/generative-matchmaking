import './App.css';
import { useMemo, useState, useEffect } from 'react';
import axios from 'axios';
import { profiles as allProfiles } from './all_profiles'
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const profiles = Object.entries(allProfiles).map(([key, value]) => ({ profileKey: key, profileData: value }));

const base64ToImage = (base64String) => {
  return `data:image/png;base64,${base64String}`
}

const getProfile = (profileId) => {
  return profiles.find(({ profileKey }) => profileKey === profileId)
}
function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '300px' }}>
      {profiles.map(({ profileKey, profileData }) => {

        const matches = profileData.matches.ranked.map((matchProfileId) => getProfile(matchProfileId));

        return (
          <div key={profileKey} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <img src={base64ToImage(profileData.image)} alt="logo" />
              <p>
                <b>{profileData.profile.name}</b>
              </p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'row' }}>
              {matches.map(({ profileKey, profileData }) => (
                <div key={profileKey + 'match'} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <img src={base64ToImage(profileData.image)} alt="logo" />
                  <p>
                    {profileData.profile.name}
                  </p>
                  {/* Add content for each matched profile here */}
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default App;
