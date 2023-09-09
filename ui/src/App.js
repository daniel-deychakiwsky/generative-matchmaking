import "./App.css";
import { useState } from "react";
import { profiles as allProfiles } from "./all_profiles";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const profiles = Object.entries(allProfiles).map(([key, value]) => ({
  profileKey: key,
  profileData: value,
}));

const base64ToImage = (base64String) => {
  return `data:image/png;base64,${base64String}`;
};

const flattenObjectToRows = (object, prefix = "") => {
  let rows = [];
  for (const [key, value] of Object.entries(object)) {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (typeof value === "object") {
      if (Array.isArray(value)) {
        rows.push({ key: fullKey, value: value.join(", ") });
      } else {
        rows = rows.concat(flattenObjectToRows(value, fullKey));
      }
    } else {
      rows.push({ key: fullKey, value });
    }
  }
  return rows;
};

const ProfileAvatar = ({ src, name, selected, onSelect }) => (
  <div
    style={{
      cursor: "pointer",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "flex-start",
    }}
    onMouseEnter={onSelect}
  >
    <div
      style={{
        borderRadius: "50%",
        width: "170px",
        height: "170px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        border: selected ? "3px solid black" : "3px solid transparent",
        boxSizing: "border-box",
        marginBottom: "10px",
        boxShadow: selected ? "0px 0px 10px 5px rgba(0, 0, 0, 0.2)" : "none", // Added black box-shadow
        backgroundColor: selected ? "rgba(0, 0, 0, 0.1)" : "transparent", // Added black background color
      }}
    >
      <img
        style={{
          borderRadius: "50%",
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
        src={src}
        alt={name}
      />
    </div>
    <p
      style={{
        fontWeight: selected ? "bold" : "normal",
        textAlign: "center",
        maxWidth: "180px",
        wordWrap: "break-word",
      }}
    >
      {name}
    </p>
  </div>
);

const ProfileSection = ({ profileData }) => {
  const combinedCandidateIds = [
    ...profileData.matches.bidirectional_candidate_user_ids,
    ...profileData.matches.unidirectional_candidate_user_ids,
  ];

  const matches = combinedCandidateIds.map((matchProfileId) =>
    profiles.find(({ profileKey }) => profileKey === matchProfileId)
  );
  const [selectedMatch, setSelectedMatch] = useState(null);
  const selectedMatchProfile = selectedMatch
    ? profiles.find((profile) => profile.profileKey === selectedMatch)
        .profileData.profile
    : {};

  const profileRows = flattenObjectToRows(profileData.profile);
  const matchRows = flattenObjectToRows(selectedMatchProfile);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gridColumnGap: "100px",
        alignItems: "flex-start",
        paddingBottom: "10px",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          justifyContent: "center",
          padding: "20px",
        }}
      >
        <h3>
          <b>Profile</b>
        </h3>
        <ProfileAvatar
          src={base64ToImage(profileData.image)}
          name={profileData.profile.name}
          selected={true}
        />
      </div>
      <div style={{ padding: "20px" }}>
        <h3>
          <b>Matches</b>
        </h3>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            gap: "20px",
            alignItems: "center",
            height: "250px",
            width: "1200px",
            overflow: "auto",
          }}
        >
          {matches.map((match) => (
            <ProfileAvatar
              key={match.profileKey}
              src={base64ToImage(match.profileData.image)}
              name={`${match.profileData.profile.name}${
                profileData.matches.bidirectional_candidate_user_ids.includes(
                  match.profileKey
                )
                  ? "*"
                  : ""
              }`}
              selected={selectedMatch === match.profileKey}
              onSelect={() => setSelectedMatch(match.profileKey)}
            />
          ))}
        </div>
      </div>
      <div style={{ gridColumn: "1 / 3" }}>
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th style={{ border: "1px solid black", padding: "8px" }}>
                <b>Attribute</b>
              </th>
              <th
                style={{
                  border: "1px solid black",
                  padding: "8px",
                  width: "50%",
                }}
              >
                <b>Profile Value</b>
              </th>
              <th
                style={{
                  border: "1px solid black",
                  padding: "8px",
                  width: "50%",
                }}
              >
                <b>Match Value</b>
              </th>
            </tr>
          </thead>
          <tbody>
            {profileRows.map((row, index) => (
              <tr key={index} style={{ borderBottom: "1px solid black" }}>
                <td style={{ border: "1px solid black", padding: "8px" }}>
                  {row.key}
                </td>
                <td style={{ border: "1px solid black", padding: "8px" }}>
                  {String(row.value)}
                </td>
                <td style={{ border: "1px solid black", padding: "8px" }}>
                  {String(
                    matchRows.find((matchRow) => matchRow.key === row.key)
                      ?.value || ""
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

function App() {
  return (
    <div>
      {profiles.slice(0, 10).map(({ profileKey, profileData }) => (
        <ProfileSection key={profileKey} profileData={profileData} />
      ))}
    </div>
  );
}

export default App;
