#!/bin/bash
# Force clean build for Vercel
echo "Cleaning previous build..."
rm -rf dist
rm -rf node_modules/.vite
rm -rf .vercel
rm -rf node_modules

echo "Installing dependencies..."
npm install

echo "Building application..."
npm run build

echo "Build completed successfully!"
