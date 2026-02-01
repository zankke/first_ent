import { GoogleGenAI, Type, Schema } from "@google/genai";
import { SearchResult } from '../types';

const apiKey = process.env.API_KEY;

if (!apiKey) {
  console.error("API_KEY is not defined in the environment variables.");
}

const ai = new GoogleGenAI({ apiKey: apiKey || '' });

const ARTIST_SCHEMA_DEF = `
CREATE TABLE Artists (
id bigint NOT NULL AUTO_INCREMENT,
name varchar(100) NOT NULL,
eng_name varchar(100) DEFAULT NULL,
birth_date date DEFAULT NULL,
height_cm int DEFAULT NULL,
debut_date date DEFAULT NULL,
debut_title varchar(200) DEFAULT NULL,
recent_activity_category varchar(100) DEFAULT NULL,
recent_activity_name varchar(200) DEFAULT NULL,
genre varchar(100) DEFAULT NULL,
agency_id bigint DEFAULT NULL,
current_agency_name varchar(100) DEFAULT NULL,
nationality varchar(100) DEFAULT NULL,
is_korean tinyint(1) DEFAULT '1',
gender enum('WOMAN','MEN','NA','EXTRA','FOREIGN') DEFAULT NULL,
status enum('ACTIVE','INACTIVE','PAUSED','RETIRED','UNKNOWN') DEFAULT 'ACTIVE',
category_id bigint DEFAULT NULL,
platform varchar(50) DEFAULT NULL,
social_media_url varchar(255) DEFAULT NULL,
profile_photo varchar(255) DEFAULT NULL,
guarantee_krw bigint DEFAULT NULL,
wiki_summary text COMMENT 'Wikipedia Summary',
PRIMARY KEY (id)
);
`;

const responseSchema: Schema = {
  type: Type.OBJECT,
  properties: {
    searchStatus: {
      type: Type.STRING,
      enum: ["SUCCESS", "AMBIGUOUS", "NOT_FOUND"],
      description: "Result status."
    },
    statusMessage: {
      type: Type.STRING,
      description: "Explanation for status."
    },
    profile: {
      type: Type.OBJECT,
      properties: {
        name: { type: Type.STRING },
        eng_name: { type: Type.STRING },
        birth_date: { type: Type.STRING },
        height_cm: { type: Type.INTEGER },
        debut_date: { type: Type.STRING },
        debut_title: { type: Type.STRING },
        recent_activity_category: { type: Type.STRING },
        recent_activity_name: { type: Type.STRING },
        genre: { type: Type.STRING },
        current_agency_name: { type: Type.STRING },
        nationality: { type: Type.STRING },
        is_korean: { type: Type.BOOLEAN },
        gender: { type: Type.STRING },
        status: { type: Type.STRING },
        social_media_url: { type: Type.STRING },
        profile_photo: { type: Type.STRING },
        wiki_summary: { type: Type.STRING },
      },
      required: ["name"]
    },
    sqlQuery: { type: Type.STRING },
    pythonScript: { type: Type.STRING }
  },
  required: ["searchStatus", "profile", "sqlQuery", "pythonScript"]
};

export const searchArtist = async (artistName: string, isUpdate: boolean = false): Promise<SearchResult> => {
  if (!apiKey) throw new Error("API Key missing.");

  // Using gemini-3-flash-preview for fastest response times
  const modelId = "gemini-3-flash-preview";
  
  const systemPrompt = `You are a high-speed Data Assistant. 
  Target: "${artistName}". 
  1. Use Google Search to find current Korean celebrity info. 
  2. Map info to the provided SQL schema: ${ARTIST_SCHEMA_DEF}.
  3. Generate a SQL ${isUpdate ? 'UPDATE' : 'INSERT'} query and a brief Python script.
  4. If multiple celebrities share this name, pick the most famous K-pop/K-drama star.
  5. Return JSON only. Be fast.`;

  try {
    const response = await ai.models.generateContent({
      model: modelId,
      contents: `Search for Korean artist: ${artistName}`,
      config: {
        systemInstruction: systemPrompt,
        tools: [{ googleSearch: {} }],
        responseMimeType: "application/json",
        responseSchema: responseSchema,
        // Disable thinking for maximum speed
        thinkingConfig: { thinkingBudget: 0 }
      },
    });

    const data = JSON.parse(response.text || "{}");

    if (data.searchStatus !== 'SUCCESS') {
      throw new Error(data.statusMessage || `Artist '${artistName}' not found.`);
    }

    const sources = response.candidates?.[0]?.groundingMetadata?.groundingChunks
      ?.map((chunk: any) => chunk.web ? { title: chunk.web.title, uri: chunk.web.uri } : null)
      .filter((s: any) => s !== null) || [];

    return {
      profile: data.profile,
      sqlQuery: data.sqlQuery,
      pythonScript: data.pythonScript,
      sources: Array.from(new Map(sources.map((s: any) => [s.uri, s])).values()) as any
    };

  } catch (error) {
    console.error("Search Error:", error);
    throw error;
  }
};