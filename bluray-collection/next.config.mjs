/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    // Les posters proviennent de l'API TMDB.
    remotePatterns: [
      { protocol: "https", hostname: "image.tmdb.org" },
    ],
  },
};

export default nextConfig;
