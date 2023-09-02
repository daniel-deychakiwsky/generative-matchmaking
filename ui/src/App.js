import './App.css';
import { useMemo } from 'react';
import axios from 'axios';

const parseProfile = (profile) => {
  const { name, age, bio, distance_mi, photos } = profile;
  const image = photos[0].url;
  return { name, age, bio, distance_mi, image };
}

function App() {
  // Load all data from /profiles into an object

  const profileNamesAndImages = useMemo(async () => {
    const data = await axios.get('http://localhost:8003')

    console.log({ data })
    // return Object.keys(profiles).slice(0, 10).map((id) => {
    //   // the images are in base64 format, convert them to work as an img src
    //   const image = `data:image/png;base64,${profiles[id].image}`;
    //   const matches = profiles[id].matches;
    //   return { name: profiles[id].profile.name, image }
    // }
    // );
  }, []);

  return (
    <div className="App">
      {profileNamesAndImages.map((profile) => (
        <header className="App-header">
          <img src={profile.image} alt="logo" />
          <p>
            {profile.name}
          </p>
        </header>
      ))}
    </div>
  );
}

export default App;
