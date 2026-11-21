import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@auralis/ui"],
  reactStrictMode: true,
};

export default nextConfig;
